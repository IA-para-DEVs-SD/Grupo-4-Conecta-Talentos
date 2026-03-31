"""Configuração centralizada de logging para o sistema."""

import logging
import sys
from pathlib import Path
from typing import Any

from app.config import Settings, get_settings


class LoggerConfig:
    """Configuração centralizada de logging.

    Configura logs para arquivo e console com formatação estruturada.
    """

    def __init__(self, settings: Settings | None = None):
        """Inicializa configuração de logging.

        Args:
            settings: Configurações da aplicação
        """
        self.settings = settings or get_settings()
        self._configured = False

    def setup(self) -> None:
        """Configura o sistema de logging."""
        if self._configured:
            return

        # Cria diretório de logs se não existir
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)

        # Configuração do logger raiz
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.INFO)

        # Remove handlers existentes
        root_logger.handlers.clear()

        # Formato detalhado para logs
        formatter = logging.Formatter(
            fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(funcName)s:%(lineno)d | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        # Handler para arquivo (todos os logs)
        file_handler = logging.FileHandler(
            log_dir / "conecta_talentos.log", encoding="utf-8"
        )
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)

        # Handler para arquivo de erros (apenas erros)
        error_handler = logging.FileHandler(
            log_dir / "errors.log", encoding="utf-8"
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(formatter)
        root_logger.addHandler(error_handler)

        # Handler para console (INFO e acima)
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter(
            fmt="%(asctime)s | %(levelname)-8s | %(message)s",
            datefmt="%H:%M:%S",
        )
        console_handler.setFormatter(console_formatter)
        root_logger.addHandler(console_handler)

        # Silencia logs verbosos de bibliotecas externas
        logging.getLogger("urllib3").setLevel(logging.WARNING)
        logging.getLogger("httpx").setLevel(logging.WARNING)
        logging.getLogger("openai").setLevel(logging.WARNING)

        self._configured = True
        logging.info("Sistema de logging configurado com sucesso")


def get_logger(name: str) -> logging.Logger:
    """Obtém um logger configurado.

    Args:
        name: Nome do logger (geralmente __name__ do módulo)

    Returns:
        Logger configurado

    Example:
        >>> logger = get_logger(__name__)
        >>> logger.info("Mensagem de log")
    """
    return logging.getLogger(name)


def log_exception(
    logger: logging.Logger,
    exception: Exception,
    context: dict[str, Any] | None = None,
) -> None:
    """Registra uma exceção com contexto adicional.

    Args:
        logger: Logger a ser usado
        exception: Exceção a ser registrada
        context: Dicionário com informações de contexto
    """
    context_str = ""
    if context:
        context_items = [f"{k}={v}" for k, v in context.items()]
        context_str = f" | Contexto: {', '.join(context_items)}"

    logger.error(
        f"{exception.__class__.__name__}: {exception}{context_str}",
        exc_info=True,
    )


# Instância global de configuração
_logger_config = LoggerConfig()


def setup_logging() -> None:
    """Configura o sistema de logging (função de conveniência)."""
    _logger_config.setup()
