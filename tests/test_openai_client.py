"""Testes para o cliente OpenAI."""

from unittest.mock import AsyncMock, Mock, patch

import pytest
from openai import APIError as OpenAIAPIError
from openai import APITimeoutError, RateLimitError

from app.config import Settings
from app.processors.exceptions import (
    LLMAPIError,
    LLMConfigurationError,
    LLMRateLimitError,
    LLMTimeoutError,
)
from app.processors.openai_client import OpenAIClient


@pytest.fixture
def mock_settings():
    """Fixture com configurações mockadas."""
    return Settings(
        openai_api_key="sk-test-key",
        openai_model="gpt-4o-mini",
        openai_max_tokens=2000,
    )


@pytest.fixture
def mock_settings_no_key():
    """Fixture com configurações sem API key."""
    return Settings(openai_api_key="")


class TestOpenAIClientInitialization:
    """Testes de inicialização do cliente."""

    def test_init_with_valid_settings(self, mock_settings):
        """Testa inicialização com configurações válidas."""
        client = OpenAIClient(settings=mock_settings)

        assert client.settings == mock_settings
        assert client.client is not None
        assert client.async_client is not None

    def test_init_without_api_key_raises_error(self, mock_settings_no_key):
        """Testa que inicialização sem API key levanta erro."""
        with pytest.raises(LLMConfigurationError) as exc_info:
            OpenAIClient(settings=mock_settings_no_key)

        assert "OPENAI_API_KEY não configurada" in str(exc_info.value)


class TestChatCompletion:
    """Testes para o método chat_completion."""

    @patch("app.processors.openai_client.OpenAI")
    def test_chat_completion_success(self, mock_openai_class, mock_settings):
        """Testa chamada bem-sucedida de chat completion."""
        # Mock da resposta
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Resposta do modelo"

        mock_client = Mock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai_class.return_value = mock_client

        client = OpenAIClient(settings=mock_settings)
        messages = [{"role": "user", "content": "Olá"}]

        result = client.chat_completion(messages)

        assert result == "Resposta do modelo"
        mock_client.chat.completions.create.assert_called_once()

    @patch("app.processors.openai_client.OpenAI")
    def test_chat_completion_with_custom_params(self, mock_openai_class, mock_settings):
        """Testa chamada com parâmetros customizados."""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Resposta"

        mock_client = Mock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai_class.return_value = mock_client

        client = OpenAIClient(settings=mock_settings)
        messages = [{"role": "user", "content": "Teste"}]

        result = client.chat_completion(
            messages, model="gpt-4", max_tokens=1000, temperature=0.5
        )

        assert result == "Resposta"
        call_args = mock_client.chat.completions.create.call_args
        assert call_args.kwargs["model"] == "gpt-4"
        assert call_args.kwargs["max_tokens"] == 1000
        assert call_args.kwargs["temperature"] == 0.5

    @patch("app.processors.openai_client.OpenAI")
    def test_chat_completion_empty_response(self, mock_openai_class, mock_settings):
        """Testa resposta vazia do modelo."""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = None

        mock_client = Mock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai_class.return_value = mock_client

        client = OpenAIClient(settings=mock_settings)
        messages = [{"role": "user", "content": "Teste"}]

        result = client.chat_completion(messages)

        assert result == ""

    @patch("app.processors.openai_client.OpenAI")
    def test_chat_completion_rate_limit_error(self, mock_openai_class, mock_settings):
        """Testa tratamento de erro de rate limit."""
        mock_client = Mock()
        mock_client.chat.completions.create.side_effect = RateLimitError(
            "Rate limit exceeded", response=Mock(), body=None
        )
        mock_openai_class.return_value = mock_client

        client = OpenAIClient(settings=mock_settings)
        messages = [{"role": "user", "content": "Teste"}]

        with pytest.raises(LLMRateLimitError) as exc_info:
            client.chat_completion(messages)

        assert "Limite de taxa" in str(exc_info.value)

    @patch("app.processors.openai_client.OpenAI")
    def test_chat_completion_timeout_error(self, mock_openai_class, mock_settings):
        """Testa tratamento de erro de timeout."""
        mock_client = Mock()
        mock_client.chat.completions.create.side_effect = APITimeoutError(
            request=Mock()
        )
        mock_openai_class.return_value = mock_client

        client = OpenAIClient(settings=mock_settings)
        messages = [{"role": "user", "content": "Teste"}]

        with pytest.raises(LLMTimeoutError) as exc_info:
            client.chat_completion(messages)

        assert "Timeout" in str(exc_info.value)

    @patch("app.processors.openai_client.OpenAI")
    def test_chat_completion_api_error(self, mock_openai_class, mock_settings):
        """Testa tratamento de erro genérico da API."""
        mock_response = Mock()
        mock_response.status_code = 500

        mock_client = Mock()
        mock_client.chat.completions.create.side_effect = OpenAIAPIError(
            "Internal server error", response=mock_response, body=None
        )
        mock_openai_class.return_value = mock_client

        client = OpenAIClient(settings=mock_settings)
        messages = [{"role": "user", "content": "Teste"}]

        with pytest.raises(LLMAPIError) as exc_info:
            client.chat_completion(messages)

        assert "Erro na API OpenAI" in str(exc_info.value)
        assert exc_info.value.status_code == 500


class TestAsyncChatCompletion:
    """Testes para o método async_chat_completion."""

    @pytest.mark.asyncio
    @patch("app.processors.openai_client.AsyncOpenAI")
    async def test_async_chat_completion_success(
        self, mock_async_openai_class, mock_settings
    ):
        """Testa chamada assíncrona bem-sucedida."""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Resposta assíncrona"

        mock_client = Mock()
        mock_client.chat.completions.create = AsyncMock(return_value=mock_response)
        mock_async_openai_class.return_value = mock_client

        client = OpenAIClient(settings=mock_settings)
        messages = [{"role": "user", "content": "Olá"}]

        result = await client.async_chat_completion(messages)

        assert result == "Resposta assíncrona"
        mock_client.chat.completions.create.assert_called_once()

    @pytest.mark.asyncio
    @patch("app.processors.openai_client.AsyncOpenAI")
    async def test_async_chat_completion_rate_limit_error(
        self, mock_async_openai_class, mock_settings
    ):
        """Testa tratamento assíncrono de erro de rate limit."""
        mock_client = Mock()
        mock_client.chat.completions.create = AsyncMock(
            side_effect=RateLimitError("Rate limit", response=Mock(), body=None)
        )
        mock_async_openai_class.return_value = mock_client

        client = OpenAIClient(settings=mock_settings)
        messages = [{"role": "user", "content": "Teste"}]

        with pytest.raises(LLMRateLimitError):
            await client.async_chat_completion(messages)

    @pytest.mark.asyncio
    @patch("app.processors.openai_client.AsyncOpenAI")
    async def test_async_chat_completion_timeout_error(
        self, mock_async_openai_class, mock_settings
    ):
        """Testa tratamento assíncrono de erro de timeout."""
        mock_client = Mock()
        mock_client.chat.completions.create = AsyncMock(
            side_effect=APITimeoutError(request=Mock())
        )
        mock_async_openai_class.return_value = mock_client

        client = OpenAIClient(settings=mock_settings)
        messages = [{"role": "user", "content": "Teste"}]

        with pytest.raises(LLMTimeoutError):
            await client.async_chat_completion(messages)
