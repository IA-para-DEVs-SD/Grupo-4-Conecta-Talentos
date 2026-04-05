"""Testes para middleware de tratamento de erros."""

import pytest
from fastapi import FastAPI, Request
from fastapi.testclient import TestClient

from app.middleware.error_handler import ErrorHandlerMiddleware, handle_exception
from app.processors.exceptions import (
    AnonimizacaoError,
    ArquivoNaoEncontradoError,
    CampoObrigatorioError,
    LLMAPIError,
    LLMConfigurationError,
    LLMRateLimitError,
    LLMTimeoutError,
    PDFCorromidoError,
    PDFFormatoInvalidoError,
    PDFMuitoGrandeError,
    PDFVazioError,
    RegistroNaoEncontradoError,
    TamanhoArquivoExcedidoError,
    TipoArquivoInvalidoError,
    TokenLimitExceededError,
)


@pytest.fixture
def app():
    """Cria aplicação FastAPI para testes."""
    app = FastAPI()
    app.add_middleware(ErrorHandlerMiddleware)
    return app


@pytest.fixture
def client(app):
    """Cria cliente de teste."""
    return TestClient(app)


@pytest.fixture
def mock_request():
    """Cria request mock."""
    class MockRequest:
        class URL:
            path = "/test"
        
        url = URL()
        method = "GET"
    
    return MockRequest()


class TestPDFErrorHandling:
    """Testa tratamento de erros de PDF."""

    def test_pdf_corrompido_error(self, app, client, mock_request):
        """Testa tratamento de PDF corrompido."""
        @app.get("/test")
        def test_route():
            raise PDFCorromidoError("PDF corrompido")
        
        response = client.get("/test")
        
        assert response.status_code == 422
        data = response.json()
        assert data["error"] == "pdf_corrompido"
        assert "corrompido" in data["message"].lower()

    def test_pdf_muito_grande_error(self, app, client):
        """Testa tratamento de PDF muito grande."""
        @app.get("/test")
        def test_route():
            raise PDFMuitoGrandeError("PDF grande", tamanho_mb=15.0, limite_mb=10.0)
        
        response = client.get("/test")
        
        assert response.status_code == 413
        data = response.json()
        assert data["error"] == "pdf_muito_grande"
        assert data["tamanho_mb"] == 15.0
        assert data["limite_mb"] == 10.0

    def test_pdf_vazio_error(self, app, client):
        """Testa tratamento de PDF vazio."""
        @app.get("/test")
        def test_route():
            raise PDFVazioError("PDF vazio")
        
        response = client.get("/test")
        
        assert response.status_code == 422
        data = response.json()
        assert data["error"] == "pdf_vazio"

    def test_pdf_formato_invalido_error(self, app, client):
        """Testa tratamento de formato inválido."""
        @app.get("/test")
        def test_route():
            raise PDFFormatoInvalidoError("Não é PDF")
        
        response = client.get("/test")
        
        assert response.status_code == 415
        data = response.json()
        assert data["error"] == "formato_invalido"


class TestUploadErrorHandling:
    """Testa tratamento de erros de upload."""

    def test_tipo_arquivo_invalido_error(self, app, client):
        """Testa tratamento de tipo inválido."""
        @app.get("/test")
        def test_route():
            raise TipoArquivoInvalidoError(
                "Tipo inválido",
                tipo_recebido="image/png",
                tipos_permitidos=["application/pdf"],
            )
        
        response = client.get("/test")
        
        assert response.status_code == 415
        data = response.json()
        assert data["error"] == "tipo_arquivo_invalido"
        assert data["tipo_recebido"] == "image/png"
        assert data["tipos_permitidos"] == ["application/pdf"]

    def test_tamanho_arquivo_excedido_error(self, app, client):
        """Testa tratamento de tamanho excedido."""
        @app.get("/test")
        def test_route():
            raise TamanhoArquivoExcedidoError(
                "Arquivo grande", tamanho_mb=25.0, limite_mb=20.0
            )
        
        response = client.get("/test")
        
        assert response.status_code == 413
        data = response.json()
        assert data["error"] == "arquivo_muito_grande"
        assert data["tamanho_mb"] == 25.0
        assert data["limite_mb"] == 20.0

    def test_arquivo_nao_encontrado_error(self, app, client):
        """Testa tratamento de arquivo não encontrado."""
        @app.get("/test")
        def test_route():
            raise ArquivoNaoEncontradoError("Arquivo não existe")
        
        response = client.get("/test")
        
        assert response.status_code == 404
        data = response.json()
        assert data["error"] == "arquivo_nao_encontrado"


class TestAnonimizacaoErrorHandling:
    """Testa tratamento de erros de anonimização."""

    def test_anonimizacao_error_non_critical(self, app, client):
        """Testa que erro de anonimização não é crítico."""
        @app.get("/test")
        def test_route():
            raise AnonimizacaoError("Erro na anonimização")
        
        response = client.get("/test")
        
        # Deve retornar 200 com warning
        assert response.status_code == 200
        data = response.json()
        assert data["warning"] == "anonimizacao_falhou"
        assert "continuar" in data["message"].lower()


class TestLLMErrorHandling:
    """Testa tratamento de erros de LLM."""

    def test_llm_configuration_error(self, app, client):
        """Testa tratamento de erro de configuração."""
        @app.get("/test")
        def test_route():
            raise LLMConfigurationError("API key ausente")
        
        response = client.get("/test")
        
        assert response.status_code == 500
        data = response.json()
        assert data["error"] == "llm_configuracao"

    def test_llm_rate_limit_error(self, app, client):
        """Testa tratamento de rate limit."""
        @app.get("/test")
        def test_route():
            raise LLMRateLimitError("Limite excedido")
        
        response = client.get("/test")
        
        assert response.status_code == 429
        data = response.json()
        assert data["error"] == "llm_limite_taxa"
        assert "retry_after" in data

    def test_llm_timeout_error(self, app, client):
        """Testa tratamento de timeout."""
        @app.get("/test")
        def test_route():
            raise LLMTimeoutError("Timeout")
        
        response = client.get("/test")
        
        assert response.status_code == 504
        data = response.json()
        assert data["error"] == "llm_timeout"

    def test_token_limit_exceeded_error(self, app, client):
        """Testa tratamento de limite de tokens."""
        @app.get("/test")
        def test_route():
            raise TokenLimitExceededError("Tokens excedidos", token_count=5000, max_tokens=4096)
        
        response = client.get("/test")
        
        assert response.status_code == 422
        data = response.json()
        assert data["error"] == "tokens_excedidos"
        assert data["token_count"] == 5000
        assert data["max_tokens"] == 4096

    def test_llm_api_error(self, app, client):
        """Testa tratamento de erro da API."""
        @app.get("/test")
        def test_route():
            raise LLMAPIError("Erro na API", status_code=502)
        
        response = client.get("/test")
        
        assert response.status_code == 502
        data = response.json()
        assert data["error"] == "llm_api_erro"
        assert data["status_code"] == 502


class TestDatabaseErrorHandling:
    """Testa tratamento de erros de banco de dados."""

    def test_registro_nao_encontrado_error(self, app, client):
        """Testa tratamento de registro não encontrado."""
        @app.get("/test")
        def test_route():
            raise RegistroNaoEncontradoError("Vaga não encontrada", entidade="Vaga", id_valor=123)
        
        response = client.get("/test")
        
        assert response.status_code == 404
        data = response.json()
        assert data["error"] == "registro_nao_encontrado"
        assert data["entidade"] == "Vaga"
        assert data["id"] == 123


class TestValidationErrorHandling:
    """Testa tratamento de erros de validação."""

    def test_campo_obrigatorio_error(self, app, client):
        """Testa tratamento de campo obrigatório."""
        @app.get("/test")
        def test_route():
            raise CampoObrigatorioError("Campo obrigatório", campo="titulo")
        
        response = client.get("/test")
        
        assert response.status_code == 400
        data = response.json()
        assert data["error"] == "campo_obrigatorio"
        assert data["campo"] == "titulo"


class TestGenericErrorHandling:
    """Testa tratamento de erros genéricos."""

    def test_unexpected_error(self, app, client):
        """Testa tratamento de erro inesperado."""
        @app.get("/test")
        def test_route():
            raise RuntimeError("Erro inesperado")
        
        response = client.get("/test")
        
        assert response.status_code == 500
        data = response.json()
        assert data["error"] == "erro_inesperado"

    def test_handle_exception_function(self, mock_request):
        """Testa função handle_exception diretamente."""
        exc = ValueError("Erro de teste")
        response = handle_exception(exc, mock_request)
        
        assert response.status_code == 500
        data = response.body.decode()
        assert "erro_inesperado" in data


class TestMiddlewareIntegration:
    """Testa integração do middleware."""

    def test_middleware_catches_all_exceptions(self, app, client):
        """Testa que middleware captura todas as exceções."""
        @app.get("/test")
        def test_route():
            raise Exception("Qualquer exceção")
        
        response = client.get("/test")
        
        # Não deve retornar 500 sem tratamento
        assert response.status_code == 500
        assert response.json()["error"] == "erro_inesperado"

    def test_middleware_allows_successful_requests(self, app, client):
        """Testa que middleware não interfere em requisições bem-sucedidas."""
        @app.get("/test")
        def test_route():
            return {"status": "ok"}
        
        response = client.get("/test")
        
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}

    def test_error_response_structure(self, app, client):
        """Testa estrutura da resposta de erro."""
        @app.get("/test")
        def test_route():
            raise PDFCorromidoError("Teste")
        
        response = client.get("/test")
        data = response.json()
        
        # Toda resposta de erro deve ter 'error' e 'message'
        assert "error" in data
        assert "message" in data
        assert isinstance(data["error"], str)
        assert isinstance(data["message"], str)
