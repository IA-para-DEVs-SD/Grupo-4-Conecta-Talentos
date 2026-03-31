"""Testes para configuração de logging."""

import logging
from pathlib import Path

import pytest

from app.logging_config import LoggerConfig, get_logger, log_exception, setup_logging


class TestLoggerConfig:
    """Testa configuração de logging."""

    def test_logger_config_initialization(self):
        """Testa inicialização da configuração."""
        config = LoggerConfig()
        assert config.settings is not None
        assert config._configured is False

    def test_setup_creates_log_directory(self, tmp_path, monkeypatch):
        """Testa que setup cria diretório de logs."""
        # Muda para diretório temporário
        monkeypatch.chdir(tmp_path)
        
        config = LoggerConfig()
        config.setup()
        
        log_dir = Path("logs")
        assert log_dir.exists()
        assert log_dir.is_dir()

    def test_setup_configures_handlers(self):
        """Testa que setup configura handlers."""
        config = LoggerConfig()
        config.setup()
        
        root_logger = logging.getLogger()
        
        # Deve ter 3 handlers: arquivo, erros, console
        assert len(root_logger.handlers) >= 3
        
        # Verifica tipos de handlers
        handler_types = [type(h).__name__ for h in root_logger.handlers]
        assert "FileHandler" in handler_types
        assert "StreamHandler" in handler_types

    def test_setup_only_runs_once(self):
        """Testa que setup só executa uma vez."""
        config = LoggerConfig()
        
        config.setup()
        assert config._configured is True
        
        # Segunda chamada não deve fazer nada
        handlers_count = len(logging.getLogger().handlers)
        config.setup()
        assert len(logging.getLogger().handlers) == handlers_count

    def test_setup_logging_function(self):
        """Testa função de conveniência setup_logging."""
        setup_logging()
        
        root_logger = logging.getLogger()
        assert len(root_logger.handlers) > 0


class TestGetLogger:
    """Testa função get_logger."""

    def test_get_logger_returns_logger(self):
        """Testa que get_logger retorna um logger."""
        logger = get_logger("test_module")
        assert isinstance(logger, logging.Logger)
        assert logger.name == "test_module"

    def test_get_logger_with_name(self):
        """Testa get_logger com __name__."""
        logger = get_logger(__name__)
        assert isinstance(logger, logging.Logger)
        assert logger.name == __name__

    def test_different_names_return_different_loggers(self):
        """Testa que nomes diferentes retornam loggers diferentes."""
        logger1 = get_logger("module1")
        logger2 = get_logger("module2")
        
        assert logger1 is not logger2
        assert logger1.name != logger2.name


class TestLogException:
    """Testa função log_exception."""

    def test_log_exception_basic(self, caplog):
        """Testa logging básico de exceção."""
        logger = get_logger(__name__)
        
        try:
            raise ValueError("Erro de teste")
        except ValueError as e:
            with caplog.at_level(logging.ERROR):
                log_exception(logger, e)
        
        assert "ValueError: Erro de teste" in caplog.text
        assert len(caplog.records) == 1
        assert caplog.records[0].levelname == "ERROR"

    def test_log_exception_with_context(self, caplog):
        """Testa logging de exceção com contexto."""
        logger = get_logger(__name__)
        context = {"user_id": 123, "action": "upload"}
        
        try:
            raise RuntimeError("Erro com contexto")
        except RuntimeError as e:
            with caplog.at_level(logging.ERROR):
                log_exception(logger, e, context)
        
        assert "RuntimeError: Erro com contexto" in caplog.text
        assert "user_id=123" in caplog.text
        assert "action=upload" in caplog.text

    def test_log_exception_includes_traceback(self, caplog):
        """Testa que exceção inclui traceback."""
        logger = get_logger(__name__)
        
        try:
            # Cria uma exceção com traceback
            def inner_function():
                raise KeyError("Chave não encontrada")
            
            inner_function()
        except KeyError as e:
            with caplog.at_level(logging.ERROR):
                log_exception(logger, e)
        
        # Verifica que o traceback está presente
        assert "KeyError: Chave não encontrada" in caplog.text
        assert "inner_function" in caplog.text

    def test_log_exception_without_context(self, caplog):
        """Testa logging sem contexto."""
        logger = get_logger(__name__)
        
        try:
            raise TypeError("Tipo inválido")
        except TypeError as e:
            with caplog.at_level(logging.ERROR):
                log_exception(logger, e, context=None)
        
        assert "TypeError: Tipo inválido" in caplog.text
        assert "Contexto:" not in caplog.text


class TestLoggingIntegration:
    """Testa integração do sistema de logging."""

    def test_logger_levels(self):
        """Testa níveis de log."""
        logger = get_logger("test_levels")
        
        assert logger.isEnabledFor(logging.DEBUG)
        assert logger.isEnabledFor(logging.INFO)
        assert logger.isEnabledFor(logging.WARNING)
        assert logger.isEnabledFor(logging.ERROR)
        assert logger.isEnabledFor(logging.CRITICAL)

    def test_logger_propagation(self):
        """Testa propagação de logs."""
        parent_logger = get_logger("parent")
        child_logger = get_logger("parent.child")
        
        # Child deve propagar para parent
        assert child_logger.parent == parent_logger

    def test_multiple_loggers_independent(self, caplog):
        """Testa que múltiplos loggers são independentes."""
        logger1 = get_logger("module1")
        logger2 = get_logger("module2")
        
        with caplog.at_level(logging.INFO):
            logger1.info("Mensagem do módulo 1")
            logger2.info("Mensagem do módulo 2")
        
        assert "Mensagem do módulo 1" in caplog.text
        assert "Mensagem do módulo 2" in caplog.text
        assert len(caplog.records) == 2
