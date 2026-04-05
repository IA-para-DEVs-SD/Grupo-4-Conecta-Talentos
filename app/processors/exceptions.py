"""Exceções customizadas para o sistema ConectaTalentos."""


# ============================================================================
# Exceções Base
# ============================================================================


class ConectaTalentosError(Exception):
    """Exceção base para todos os erros do sistema."""

    pass


class ProcessorError(ConectaTalentosError):
    """Exceção base para erros de processamento."""

    pass


# ============================================================================
# Exceções de PDF
# ============================================================================


class PDFError(ProcessorError):
    """Exceção base para erros relacionados a PDF."""

    pass


class PDFCorromidoError(PDFError):
    """Erro quando o PDF está corrompido ou ilegível."""

    pass


class PDFMuitoGrandeError(PDFError):
    """Erro quando o PDF excede o tamanho máximo permitido."""

    def __init__(self, message: str, tamanho_mb: float, limite_mb: float):
        self.tamanho_mb = tamanho_mb
        self.limite_mb = limite_mb
        super().__init__(message)


class PDFVazioError(PDFError):
    """Erro quando o PDF não contém texto extraível."""

    pass


class PDFFormatoInvalidoError(PDFError):
    """Erro quando o arquivo não é um PDF válido."""

    pass


# ============================================================================
# Exceções de Upload
# ============================================================================


class UploadError(ConectaTalentosError):
    """Exceção base para erros de upload."""

    pass


class ArquivoNaoEncontradoError(UploadError):
    """Erro quando o arquivo não é encontrado."""

    pass


class TipoArquivoInvalidoError(UploadError):
    """Erro quando o tipo de arquivo não é permitido."""

    def __init__(self, message: str, tipo_recebido: str, tipos_permitidos: list[str]):
        self.tipo_recebido = tipo_recebido
        self.tipos_permitidos = tipos_permitidos
        super().__init__(message)


class TamanhoArquivoExcedidoError(UploadError):
    """Erro quando o arquivo excede o tamanho máximo."""

    def __init__(self, message: str, tamanho_mb: float, limite_mb: float):
        self.tamanho_mb = tamanho_mb
        self.limite_mb = limite_mb
        super().__init__(message)


# ============================================================================
# Exceções de Anonimização
# ============================================================================


class AnonimizacaoError(ProcessorError):
    """Exceção base para erros de anonimização (não-crítico)."""

    pass


class PresidioIndisponivelError(AnonimizacaoError):
    """Erro quando o serviço Presidio está indisponível."""

    pass


class ModeloNLPNaoEncontradoError(AnonimizacaoError):
    """Erro quando o modelo NLP não está instalado."""

    def __init__(self, message: str, modelo_requerido: str):
        self.modelo_requerido = modelo_requerido
        super().__init__(message)


# ============================================================================
# Exceções de LLM
# ============================================================================


class LLMError(ProcessorError):
    """Exceção base para erros relacionados ao LLM."""

    pass


class LLMAPIError(LLMError):
    """Erro ao chamar a API do LLM."""

    def __init__(self, message: str, status_code: int | None = None):
        self.status_code = status_code
        super().__init__(message)


class LLMConfigurationError(LLMError):
    """Erro de configuração do LLM (ex: API key ausente)."""

    pass


class LLMRateLimitError(LLMError):
    """Erro de limite de taxa da API."""

    pass


class LLMTimeoutError(LLMError):
    """Timeout ao chamar a API do LLM."""

    pass


class TokenLimitExceededError(LLMError):
    """Erro quando o prompt excede o limite de tokens."""

    def __init__(self, message: str, token_count: int, max_tokens: int):
        self.token_count = token_count
        self.max_tokens = max_tokens
        super().__init__(message)


class LLMRespostaInvalidaError(LLMError):
    """Erro quando a resposta do LLM não está no formato esperado."""

    pass


# ============================================================================
# Exceções de Banco de Dados
# ============================================================================


class DatabaseError(ConectaTalentosError):
    """Exceção base para erros de banco de dados."""

    pass


class RegistroNaoEncontradoError(DatabaseError):
    """Erro quando um registro não é encontrado."""

    def __init__(self, message: str, entidade: str, id_valor: int | str):
        self.entidade = entidade
        self.id_valor = id_valor
        super().__init__(message)


class ViolacaoIntegridadeError(DatabaseError):
    """Erro de violação de integridade referencial."""

    pass


# ============================================================================
# Exceções de Validação
# ============================================================================


class ValidationError(ConectaTalentosError):
    """Exceção base para erros de validação."""

    pass


class CampoObrigatorioError(ValidationError):
    """Erro quando um campo obrigatório está ausente."""

    def __init__(self, message: str, campo: str):
        self.campo = campo
        super().__init__(message)


class ValorInvalidoError(ValidationError):
    """Erro quando um valor não atende aos critérios de validação."""

    def __init__(self, message: str, campo: str, valor: str):
        self.campo = campo
        self.valor = valor
        super().__init__(message)
