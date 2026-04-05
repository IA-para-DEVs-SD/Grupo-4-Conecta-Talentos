"""Cliente para integração com a API da OpenAI."""

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
    e configuração de parâmetros.

    Attributes:
        settings: Configurações da aplicação
        client: Cliente síncrono da OpenAI
        async_client: Cliente assíncrono da OpenAI
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

        self.client = OpenAI(api_key=self.settings.openai_api_key)
        self.async_client = AsyncOpenAI(api_key=self.settings.openai_api_key)

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
