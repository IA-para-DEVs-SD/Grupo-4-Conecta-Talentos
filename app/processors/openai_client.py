"""Cliente para integração com a API da OpenAI."""

import os
from typing import Any

from openai import APIError as OpenAIAPIError
from openai import APITimeoutError, AsyncOpenAI, OpenAI, RateLimitError

from app.config import Settings, get_settings
from app.processors.exceptions import (
    LLMAPIError,
    LLMConfigurationError,
    LLMRateLimitError,
    LLMTimeoutError,
)


class OpenAIClient:
    """Cliente para interação com a API da OpenAI.

    Encapsula a lógica de comunicação com a API, tratamento de erros
    e configuração de parâmetros. Fallback automático para Groq se OpenAI falhar.

    Attributes:
        settings: Configurações da aplicação
        client: Cliente síncrono da OpenAI
        async_client: Cliente assíncrono da OpenAI
        groq_client: Cliente Groq como fallback
    """

    def __init__(self, settings: Settings | None = None):
        """Inicializa o cliente OpenAI.

        Args:
            settings: Configurações da aplicação. Se None, usa get_settings()

        Raises:
            LLMConfigurationError: Se a API key não estiver configurada
        """
        self.settings = settings or get_settings()

        if not self.settings.openai_api_key:
            raise LLMConfigurationError(
                "OPENAI_API_KEY não configurada. "
                "Configure a variável de ambiente OPENAI_API_KEY."
            )

        # Remove variáveis de proxy do ambiente para evitar conflitos
        proxy_vars = ['HTTP_PROXY', 'HTTPS_PROXY', 'http_proxy', 'https_proxy', 
                      'ALL_PROXY', 'all_proxy', 'NO_PROXY', 'no_proxy']
        for var in proxy_vars:
            os.environ.pop(var, None)

        self.client = OpenAI(api_key=self.settings.openai_api_key)
        self.async_client = AsyncOpenAI(api_key=self.settings.openai_api_key)
        
        # Inicializa Groq como fallback
        self.groq_client = None
        try:
            from app.processors.groq_client import GroqClient
            self.groq_client = GroqClient(settings=self.settings)
            print("✓ Groq configurado como fallback")
        except Exception as e:
            print(f"⚠ Groq não disponível como fallback: {e}")

    def chat_completion(
        self,
        messages: list[dict[str, str]],
        model: str | None = None,
        max_tokens: int | None = None,
        temperature: float = 0.7,
        **kwargs: Any,
    ) -> str:
        """Realiza uma chamada síncrona para chat completion.

        Args:
            messages: Lista de mensagens no formato OpenAI
            model: Modelo a ser usado (padrão: configuração)
            max_tokens: Máximo de tokens na resposta
            temperature: Temperatura para geração (0-2)
            **kwargs: Parâmetros adicionais para a API

        Returns:
            Conteúdo da resposta do modelo

        Raises:
            LLMAPIError: Erro na chamada da API
            LLMRateLimitError: Limite de taxa excedido
            LLMTimeoutError: Timeout na chamada
        """
        try:
            response = self.client.chat.completions.create(
                model=model or self.settings.openai_model,
                messages=messages,
                max_tokens=max_tokens or self.settings.openai_max_tokens,
                temperature=temperature,
                **kwargs,
            )
            return response.choices[0].message.content or ""

        except RateLimitError as e:
            error_msg = str(e)
            print(f"DEBUG: RateLimitError capturado: {error_msg[:100]}")
            print(f"DEBUG: Groq disponível? {self.groq_client is not None}")
            print(f"DEBUG: 'insufficient_quota' in error_msg? {'insufficient_quota' in error_msg}")
            
            # Se for erro de quota e Groq disponível, usa fallback
            if ("insufficient_quota" in error_msg or "quota" in error_msg.lower()) and self.groq_client:
                print("⚠ OpenAI sem créditos, usando Groq como fallback...")
                try:
                    result = self.groq_client.chat_completion(
                        messages, max_tokens=max_tokens, temperature=temperature
                    )
                    print(f"✓ Groq retornou resposta com {len(result)} caracteres")
                    return result
                except Exception as groq_error:
                    print(f"❌ Erro no Groq: {groq_error}")
                    # Se Groq também falhar, lança o erro original
            
            raise LLMRateLimitError(
                f"Limite de taxa da API OpenAI excedido: {e}"
            ) from e

        except APITimeoutError as e:
            raise LLMTimeoutError(f"Timeout na chamada da API OpenAI: {e}") from e

        except OpenAIAPIError as e:
            raise LLMAPIError(
                f"Erro na API OpenAI: {e}", status_code=e.status_code
            ) from e

    async def async_chat_completion(
        self,
        messages: list[dict[str, str]],
        model: str | None = None,
        max_tokens: int | None = None,
        temperature: float = 0.7,
        **kwargs: Any,
    ) -> str:
        """Realiza uma chamada assíncrona para chat completion.

        Args:
            messages: Lista de mensagens no formato OpenAI
            model: Modelo a ser usado (padrão: configuração)
            max_tokens: Máximo de tokens na resposta
            temperature: Temperatura para geração (0-2)
            **kwargs: Parâmetros adicionais para a API

        Returns:
            Conteúdo da resposta do modelo

        Raises:
            LLMAPIError: Erro na chamada da API
            LLMRateLimitError: Limite de taxa excedido
            LLMTimeoutError: Timeout na chamada
        """
        try:
            response = await self.async_client.chat.completions.create(
                model=model or self.settings.openai_model,
                messages=messages,
                max_tokens=max_tokens or self.settings.openai_max_tokens,
                temperature=temperature,
                **kwargs,
            )
            return response.choices[0].message.content or ""

        except RateLimitError as e:
            raise LLMRateLimitError(
                f"Limite de taxa da API OpenAI excedido: {e}"
            ) from e

        except APITimeoutError as e:
            raise LLMTimeoutError(f"Timeout na chamada da API OpenAI: {e}") from e

        except OpenAIAPIError as e:
            raise LLMAPIError(
                f"Erro na API OpenAI: {e}", status_code=e.status_code
            ) from e
