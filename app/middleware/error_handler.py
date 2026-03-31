"""Middleware para tratamento global de erros."""

from fastapi import Request, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.logging_config import get_logger, log_exception
from app.processors.exceptions import (
    AnonimizacaoError,
    ArquivoNaoEncontradoError,
    CampoObrigatorioError,
    ConectaTalentosError,
    DatabaseError,
    LLMAPIError,
    LLMConfigurationError,
    LLMRateLimitError,
    LLMTimeoutError,
    PDFCorromidoError,
    PDFError,
    PDFFormatoInvalidoError,
    PDFMuitoGrandeError,
    PDFVazioError,
    RegistroNaoEncontradoError,
    TamanhoArquivoExcedidoError,
    TipoArquivoInvalidoError,
    TokenLimitExceededError,
    UploadError,
    ValidationError,
)

logger = get_logger(__name__)


class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    """Middleware para capturar e tratar exceções globalmente."""

    async def dispatch(self, request: Request, call_next):
        """Processa requisição e captura exceções.

        Args:
            request: Requisição HTTP
            call_next: Próximo handler na cadeia

        Returns:
            Response HTTP
        """
        try:
            response = await call_next(request)
            return response

        except Exception as exc:
            return handle_exception(exc, request)


def handle_exception(exc: Exception, request: Request) -> JSONResponse:
    """Trata exceção e retorna resposta apropriada.

    Args:
        exc: Exceção capturada
        request: Requisição HTTP

    Returns:
        JSONResponse com detalhes do erro
    """
    # Contexto para logging
    context = {
        "path": request.url.path,
        "method": request.method,
    }

    # ========================================================================
    # Erros de PDF
    # ========================================================================

    if isinstance(exc, PDFCorromidoError):
        log_exception(logger, exc, context)
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "error": "pdf_corrompido",
                "message": "O arquivo PDF está corrompido ou ilegível. Por favor, verifique o arquivo e tente novamente.",
                "details": str(exc),
            },
        )

    if isinstance(exc, PDFMuitoGrandeError):
        log_exception(logger, exc, context)
        return JSONResponse(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            content={
                "error": "pdf_muito_grande",
                "message": f"O PDF excede o tamanho máximo permitido de {exc.limite_mb}MB.",
                "tamanho_mb": exc.tamanho_mb,
                "limite_mb": exc.limite_mb,
            },
        )

    if isinstance(exc, PDFVazioError):
        log_exception(logger, exc, context)
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "error": "pdf_vazio",
                "message": "O PDF não contém texto extraível. Verifique se o arquivo não está vazio ou se é uma imagem escaneada.",
                "details": str(exc),
            },
        )

    if isinstance(exc, PDFFormatoInvalidoError):
        log_exception(logger, exc, context)
        return JSONResponse(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            content={
                "error": "formato_invalido",
                "message": "O arquivo não é um PDF válido.",
                "details": str(exc),
            },
        )

    if isinstance(exc, PDFError):
        log_exception(logger, exc, context)
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "error": "erro_pdf",
                "message": "Erro ao processar o arquivo PDF.",
                "details": str(exc),
            },
        )

    # ========================================================================
    # Erros de Upload
    # ========================================================================

    if isinstance(exc, TipoArquivoInvalidoError):
        log_exception(logger, exc, context)
        return JSONResponse(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            content={
                "error": "tipo_arquivo_invalido",
                "message": f"Tipo de arquivo não permitido. Tipos aceitos: {', '.join(exc.tipos_permitidos)}",
                "tipo_recebido": exc.tipo_recebido,
                "tipos_permitidos": exc.tipos_permitidos,
            },
        )

    if isinstance(exc, TamanhoArquivoExcedidoError):
        log_exception(logger, exc, context)
        return JSONResponse(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            content={
                "error": "arquivo_muito_grande",
                "message": f"O arquivo excede o tamanho máximo de {exc.limite_mb}MB.",
                "tamanho_mb": exc.tamanho_mb,
                "limite_mb": exc.limite_mb,
            },
        )

    if isinstance(exc, ArquivoNaoEncontradoError):
        log_exception(logger, exc, context)
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "error": "arquivo_nao_encontrado",
                "message": "Arquivo não encontrado.",
                "details": str(exc),
            },
        )

    if isinstance(exc, UploadError):
        log_exception(logger, exc, context)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "error": "erro_upload",
                "message": "Erro ao fazer upload do arquivo.",
                "details": str(exc),
            },
        )

    # ========================================================================
    # Erros de Anonimização (não-críticos, apenas log)
    # ========================================================================

    if isinstance(exc, AnonimizacaoError):
        logger.warning(
            f"Erro de anonimização (não-crítico): {exc}",
            extra=context,
        )
        # Não retorna erro para o usuário, continua processamento
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "warning": "anonimizacao_falhou",
                "message": "Anonimização de dados não pôde ser realizada, mas o processamento continuará.",
            },
        )

    # ========================================================================
    # Erros de LLM
    # ========================================================================

    if isinstance(exc, LLMConfigurationError):
        log_exception(logger, exc, context)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": "llm_configuracao",
                "message": "Erro de configuração da IA. Entre em contato com o suporte.",
                "details": "Configuração da API de IA está incorreta.",
            },
        )

    if isinstance(exc, LLMRateLimitError):
        log_exception(logger, exc, context)
        return JSONResponse(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            content={
                "error": "llm_limite_taxa",
                "message": "Limite de requisições à IA excedido. Por favor, tente novamente em alguns minutos.",
                "retry_after": 60,
            },
        )

    if isinstance(exc, LLMTimeoutError):
        log_exception(logger, exc, context)
        return JSONResponse(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            content={
                "error": "llm_timeout",
                "message": "A análise está demorando mais que o esperado. Por favor, tente novamente.",
            },
        )

    if isinstance(exc, TokenLimitExceededError):
        log_exception(logger, exc, context)
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "error": "tokens_excedidos",
                "message": "O currículo ou vaga são muito longos para análise.",
                "token_count": exc.token_count,
                "max_tokens": exc.max_tokens,
            },
        )

    if isinstance(exc, LLMAPIError):
        log_exception(logger, exc, context)
        return JSONResponse(
            status_code=status.HTTP_502_BAD_GATEWAY,
            content={
                "error": "llm_api_erro",
                "message": "Erro ao comunicar com o serviço de IA. Por favor, tente novamente.",
                "status_code": exc.status_code,
            },
        )

    # ========================================================================
    # Erros de Banco de Dados
    # ========================================================================

    if isinstance(exc, RegistroNaoEncontradoError):
        log_exception(logger, exc, context)
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "error": "registro_nao_encontrado",
                "message": f"{exc.entidade} não encontrado(a).",
                "entidade": exc.entidade,
                "id": exc.id_valor,
            },
        )

    if isinstance(exc, DatabaseError):
        log_exception(logger, exc, context)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": "erro_banco_dados",
                "message": "Erro ao acessar o banco de dados.",
                "details": str(exc),
            },
        )

    # ========================================================================
    # Erros de Validação
    # ========================================================================

    if isinstance(exc, CampoObrigatorioError):
        log_exception(logger, exc, context)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "error": "campo_obrigatorio",
                "message": f"O campo '{exc.campo}' é obrigatório.",
                "campo": exc.campo,
            },
        )

    if isinstance(exc, ValidationError):
        log_exception(logger, exc, context)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "error": "validacao",
                "message": "Erro de validação.",
                "details": str(exc),
            },
        )

    # ========================================================================
    # Erro genérico do sistema
    # ========================================================================

    if isinstance(exc, ConectaTalentosError):
        log_exception(logger, exc, context)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": "erro_sistema",
                "message": "Erro interno do sistema.",
                "details": str(exc),
            },
        )

    # ========================================================================
    # Erro não tratado
    # ========================================================================

    log_exception(logger, exc, context)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "erro_inesperado",
            "message": "Ocorreu um erro inesperado. Por favor, tente novamente.",
        },
    )
