"""Cliente para integração com a API do Groq (alternativa gratuita)."""

from typing import Any

from groq import Groq

from app.config import Settings, get_settings
from app.processors.exceptions import (
    LLMAPIError,
    LLMConfigurationError,
    LLMRateLimitError,
    LLMTimeoutError,
)


class GroqClient:
    """Cliente para interação com a API do Groq.

    Groq oferece API gratuita com modelos rápidos como llama3-70b.

    Attributes:
        settings: Configurações da aplicação
        client: Cliente do Groq
    """

    def __init__(self, settings: Settings | None = None):
        """Inicializa o cliente Groq.

        Args:
            settings: Configurações da aplicação. Se None, usa get_settings()

        Raises:
            LLMConfigurationError: Se a API key não estiver configurada
        """
        self.settings = settings or get_settings()

        # Usa GROQ_API_KEY se disponível, senão tenta OPENAI_API_KEY
        api_key = self.settings.groq_api_key or self.settings.openai_api_key

        if not api_key:
            raise LLMConfigurationError(
                "GROQ_API_KEY ou OPENAI_API_KEY não configurada. "
                "Configure a variável de ambiente."
            )

        print(f"Inicializando Groq com chave: {api_key[:10]}...")
        
        self.client = Groq(api_key=api_key)
        
        # Modelo padrão do Groq (rápido e gratuito)
        self.model = self.settings.groq_model if hasattr(self.settings, 'groq_model') else 'llama-3.3-70b-versatile'
        
        print(f"Groq inicializado com modelo: {self.model}")

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
            model: Modelo a ser usado (padrão: llama-3.1-70b-versatile)
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
                model=model or self.model,
                messages=messages,
                max_tokens=max_tokens or self.settings.openai_max_tokens,
                temperature=temperature,
                **kwargs,
            )
            return response.choices[0].message.content or ""

        except Exception as e:
            error_msg = str(e).lower()
            
            if "rate" in error_msg or "limit" in error_msg:
                raise LLMRateLimitError(
                    f"Limite de taxa da API Groq excedido: {e}"
                ) from e
            
            if "timeout" in error_msg:
                raise LLMTimeoutError(f"Timeout na chamada da API Groq: {e}") from e
            
            raise LLMAPIError(f"Erro na API Groq: {e}") from e

    async def async_chat_completion(
        self,
        messages: list[dict[str, str]],
        model: str | None = None,
        max_tokens: int | None = None,
        temperature: float = 0.7,
        **kwargs: Any,
    ) -> str:
        """Versão assíncrona (Groq não tem cliente async nativo, usa sync).

        Args:
            messages: Lista de mensagens no formato OpenAI
            model: Modelo a ser usado
            max_tokens: Máximo de tokens na resposta
            temperature: Temperatura para geração (0-2)
            **kwargs: Parâmetros adicionais para a API

        Returns:
            Conteúdo da resposta do modelo
        """
        # Groq é muito rápido, então usar sync não é problema
        return self.chat_completion(messages, model, max_tokens, temperature, **kwargs)
