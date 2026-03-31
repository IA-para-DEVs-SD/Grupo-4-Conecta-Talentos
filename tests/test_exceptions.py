"""Testes para hierarquia de exceções."""

import pytest

from app.processors.exceptions import (
    AnonimizacaoError,
    ArquivoNaoEncontradoError,
    CampoObrigatorioError,
    ConectaTalentosError,
    DatabaseError,
    LLMAPIError,
    LLMConfigurationError,
    LLMError,
    LLMRateLimitError,
    LLMRespostaInvalidaError,
    LLMTimeoutError,
    ModeloNLPNaoEncontradoError,
    PDFCorromidoError,
    PDFError,
    PDFFormatoInvalidoError,
    PDFMuitoGrandeError,
    PDFVazioError,
    PresidioIndisponivelError,
    ProcessorError,
    RegistroNaoEncontradoError,
    TamanhoArquivoExcedidoError,
    TipoArquivoInvalidoError,
    TokenLimitExceededError,
    UploadError,
    ValidationError,
    ValorInvalidoError,
    ViolacaoIntegridadeError,
)


class TestExceptionHierarchy:
    """Testa hierarquia de exceções."""

    def test_base_exception(self):
        """Testa exceção base do sistema."""
        exc = ConectaTalentosError("Erro base")
        assert str(exc) == "Erro base"
        assert isinstance(exc, Exception)

    def test_processor_error_hierarchy(self):
        """Testa que ProcessorError herda de ConectaTalentosError."""
        exc = ProcessorError("Erro de processamento")
        assert isinstance(exc, ConectaTalentosError)
        assert isinstance(exc, Exception)


class TestPDFExceptions:
    """Testa exceções relacionadas a PDF."""

    def test_pdf_error_base(self):
        """Testa exceção base de PDF."""
        exc = PDFError("Erro no PDF")
        assert isinstance(exc, ProcessorError)
        assert str(exc) == "Erro no PDF"

    def test_pdf_corrompido_error(self):
        """Testa exceção de PDF corrompido."""
        exc = PDFCorromidoError("PDF está corrompido")
        assert isinstance(exc, PDFError)
        assert str(exc) == "PDF está corrompido"

    def test_pdf_muito_grande_error(self):
        """Testa exceção de PDF muito grande."""
        exc = PDFMuitoGrandeError("PDF muito grande", tamanho_mb=15.5, limite_mb=10.0)
        assert isinstance(exc, PDFError)
        assert exc.tamanho_mb == 15.5
        assert exc.limite_mb == 10.0
        assert "PDF muito grande" in str(exc)

    def test_pdf_vazio_error(self):
        """Testa exceção de PDF vazio."""
        exc = PDFVazioError("PDF não contém texto")
        assert isinstance(exc, PDFError)
        assert str(exc) == "PDF não contém texto"

    def test_pdf_formato_invalido_error(self):
        """Testa exceção de formato inválido."""
        exc = PDFFormatoInvalidoError("Não é um PDF válido")
        assert isinstance(exc, PDFError)
        assert str(exc) == "Não é um PDF válido"


class TestUploadExceptions:
    """Testa exceções relacionadas a upload."""

    def test_upload_error_base(self):
        """Testa exceção base de upload."""
        exc = UploadError("Erro no upload")
        assert isinstance(exc, ConectaTalentosError)
        assert str(exc) == "Erro no upload"

    def test_arquivo_nao_encontrado_error(self):
        """Testa exceção de arquivo não encontrado."""
        exc = ArquivoNaoEncontradoError("Arquivo não existe")
        assert isinstance(exc, UploadError)
        assert str(exc) == "Arquivo não existe"

    def test_tipo_arquivo_invalido_error(self):
        """Testa exceção de tipo de arquivo inválido."""
        exc = TipoArquivoInvalidoError(
            "Tipo não permitido",
            tipo_recebido="image/png",
            tipos_permitidos=["application/pdf"],
        )
        assert isinstance(exc, UploadError)
        assert exc.tipo_recebido == "image/png"
        assert exc.tipos_permitidos == ["application/pdf"]
        assert "Tipo não permitido" in str(exc)

    def test_tamanho_arquivo_excedido_error(self):
        """Testa exceção de tamanho excedido."""
        exc = TamanhoArquivoExcedidoError(
            "Arquivo muito grande", tamanho_mb=25.0, limite_mb=20.0
        )
        assert isinstance(exc, UploadError)
        assert exc.tamanho_mb == 25.0
        assert exc.limite_mb == 20.0
        assert "Arquivo muito grande" in str(exc)


class TestAnonimizacaoExceptions:
    """Testa exceções relacionadas a anonimização."""

    def test_anonimizacao_error_base(self):
        """Testa exceção base de anonimização."""
        exc = AnonimizacaoError("Erro na anonimização")
        assert isinstance(exc, ProcessorError)
        assert str(exc) == "Erro na anonimização"

    def test_presidio_indisponivel_error(self):
        """Testa exceção de Presidio indisponível."""
        exc = PresidioIndisponivelError("Presidio não está disponível")
        assert isinstance(exc, AnonimizacaoError)
        assert str(exc) == "Presidio não está disponível"

    def test_modelo_nlp_nao_encontrado_error(self):
        """Testa exceção de modelo NLP não encontrado."""
        exc = ModeloNLPNaoEncontradoError(
            "Modelo não instalado", modelo_requerido="pt_core_news_lg"
        )
        assert isinstance(exc, AnonimizacaoError)
        assert exc.modelo_requerido == "pt_core_news_lg"
        assert "Modelo não instalado" in str(exc)


class TestLLMExceptions:
    """Testa exceções relacionadas a LLM."""

    def test_llm_error_base(self):
        """Testa exceção base de LLM."""
        exc = LLMError("Erro no LLM")
        assert isinstance(exc, ProcessorError)
        assert str(exc) == "Erro no LLM"

    def test_llm_api_error(self):
        """Testa exceção de erro na API."""
        exc = LLMAPIError("Erro na API", status_code=500)
        assert isinstance(exc, LLMError)
        assert exc.status_code == 500
        assert "Erro na API" in str(exc)

    def test_llm_api_error_without_status(self):
        """Testa exceção de erro na API sem status code."""
        exc = LLMAPIError("Erro na API")
        assert isinstance(exc, LLMError)
        assert exc.status_code is None

    def test_llm_configuration_error(self):
        """Testa exceção de configuração."""
        exc = LLMConfigurationError("API key ausente")
        assert isinstance(exc, LLMError)
        assert str(exc) == "API key ausente"

    def test_llm_rate_limit_error(self):
        """Testa exceção de rate limit."""
        exc = LLMRateLimitError("Limite excedido")
        assert isinstance(exc, LLMError)
        assert str(exc) == "Limite excedido"

    def test_llm_timeout_error(self):
        """Testa exceção de timeout."""
        exc = LLMTimeoutError("Timeout na chamada")
        assert isinstance(exc, LLMError)
        assert str(exc) == "Timeout na chamada"

    def test_token_limit_exceeded_error(self):
        """Testa exceção de limite de tokens."""
        exc = TokenLimitExceededError(
            "Tokens excedidos", token_count=5000, max_tokens=4096
        )
        assert isinstance(exc, LLMError)
        assert exc.token_count == 5000
        assert exc.max_tokens == 4096
        assert "Tokens excedidos" in str(exc)

    def test_llm_resposta_invalida_error(self):
        """Testa exceção de resposta inválida."""
        exc = LLMRespostaInvalidaError("JSON malformado")
        assert isinstance(exc, LLMError)
        assert str(exc) == "JSON malformado"


class TestDatabaseExceptions:
    """Testa exceções relacionadas a banco de dados."""

    def test_database_error_base(self):
        """Testa exceção base de banco de dados."""
        exc = DatabaseError("Erro no banco")
        assert isinstance(exc, ConectaTalentosError)
        assert str(exc) == "Erro no banco"

    def test_registro_nao_encontrado_error(self):
        """Testa exceção de registro não encontrado."""
        exc = RegistroNaoEncontradoError("Vaga não encontrada", entidade="Vaga", id_valor=123)
        assert isinstance(exc, DatabaseError)
        assert exc.entidade == "Vaga"
        assert exc.id_valor == 123
        assert "Vaga não encontrada" in str(exc)

    def test_violacao_integridade_error(self):
        """Testa exceção de violação de integridade."""
        exc = ViolacaoIntegridadeError("Chave estrangeira violada")
        assert isinstance(exc, DatabaseError)
        assert str(exc) == "Chave estrangeira violada"


class TestValidationExceptions:
    """Testa exceções relacionadas a validação."""

    def test_validation_error_base(self):
        """Testa exceção base de validação."""
        exc = ValidationError("Erro de validação")
        assert isinstance(exc, ConectaTalentosError)
        assert str(exc) == "Erro de validação"

    def test_campo_obrigatorio_error(self):
        """Testa exceção de campo obrigatório."""
        exc = CampoObrigatorioError("Campo obrigatório", campo="titulo")
        assert isinstance(exc, ValidationError)
        assert exc.campo == "titulo"
        assert "Campo obrigatório" in str(exc)

    def test_valor_invalido_error(self):
        """Testa exceção de valor inválido."""
        exc = ValorInvalidoError("Valor inválido", campo="score", valor="abc")
        assert isinstance(exc, ValidationError)
        assert exc.campo == "score"
        assert exc.valor == "abc"
        assert "Valor inválido" in str(exc)
