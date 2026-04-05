"""Testes para o otimizador de prompts."""

import pytest

from app.config import Settings
from app.processors.exceptions import TokenLimitExceededError
from app.processors.otimizador_prompt import OtimizadorPrompt


@pytest.fixture
def mock_settings():
    """Fixture com configurações mockadas."""
    return Settings(
        openai_api_key="sk-test-key",
        openai_model="gpt-4o-mini",
        openai_max_tokens=2000,
    )


@pytest.fixture
def otimizador(mock_settings):
    """Fixture com otimizador inicializado."""
    return OtimizadorPrompt(settings=mock_settings)


class TestContarTokens:
    """Testes para contagem de tokens."""

    def test_contar_tokens_texto_simples(self, otimizador):
        """Testa contagem de tokens em texto simples."""
        texto = "Olá, mundo!"
        tokens = otimizador.contar_tokens(texto)
        assert tokens > 0
        assert isinstance(tokens, int)

    def test_contar_tokens_texto_vazio(self, otimizador):
        """Testa contagem de tokens em texto vazio."""
        tokens = otimizador.contar_tokens("")
        assert tokens == 0

    def test_contar_tokens_texto_longo(self, otimizador):
        """Testa que texto longo tem mais tokens."""
        texto_curto = "Python"
        texto_longo = "Python é uma linguagem de programação de alto nível"

        tokens_curto = otimizador.contar_tokens(texto_curto)
        tokens_longo = otimizador.contar_tokens(texto_longo)

        assert tokens_longo > tokens_curto

    def test_contar_tokens_mensagens(self, otimizador):
        """Testa contagem de tokens em mensagens."""
        mensagens = [
            {"role": "system", "content": "Você é um assistente útil"},
            {"role": "user", "content": "Olá!"},
        ]

        tokens = otimizador.contar_tokens_mensagens(mensagens)
        assert tokens > 0
        # Deve incluir overhead
        assert tokens > otimizador.contar_tokens("Você é um assistente útilOlá!")


class TestTruncarTexto:
    """Testes para truncamento de texto."""

    def test_truncar_texto_dentro_do_limite(self, otimizador):
        """Testa que texto dentro do limite não é truncado."""
        texto = "Texto curto"
        max_tokens = 100

        resultado = otimizador.truncar_texto(texto, max_tokens)
        assert resultado == texto

    def test_truncar_texto_preservando_inicio(self, otimizador):
        """Testa truncamento preservando o início."""
        texto = "Este é um texto muito longo que precisa ser truncado para caber no limite de tokens especificado."
        max_tokens = 10

        resultado = otimizador.truncar_texto(texto, max_tokens, preservar_inicio=True)

        assert len(resultado) < len(texto)
        assert otimizador.contar_tokens(resultado) <= max_tokens
        # Deve começar com o início do texto original
        assert texto.startswith(resultado[:10])

    def test_truncar_texto_preservando_final(self, otimizador):
        """Testa truncamento preservando o final."""
        texto = "Este é um texto muito longo que precisa ser truncado para caber no limite de tokens especificado."
        max_tokens = 10

        resultado = otimizador.truncar_texto(texto, max_tokens, preservar_inicio=False)

        assert len(resultado) < len(texto)
        assert otimizador.contar_tokens(resultado) <= max_tokens


class TestRemoverEspacosExtras:
    """Testes para remoção de espaços extras."""

    def test_remover_espacos_multiplos(self, otimizador):
        """Testa remoção de espaços múltiplos."""
        texto = "Texto  com   espaços    extras"
        resultado = otimizador.remover_espacos_extras(texto)
        assert resultado == "Texto com espaços extras"

    def test_remover_quebras_linha_multiplas(self, otimizador):
        """Testa remoção de quebras de linha múltiplas."""
        texto = "Linha 1\n\n\n\nLinha 2"
        resultado = otimizador.remover_espacos_extras(texto)
        assert resultado == "Linha 1\n\nLinha 2"

    def test_remover_espacos_inicio_fim_linhas(self, otimizador):
        """Testa remoção de espaços no início e fim de linhas."""
        texto = "  Linha 1  \n  Linha 2  "
        resultado = otimizador.remover_espacos_extras(texto)
        assert resultado == "Linha 1\nLinha 2"


class TestComprimirCurriculo:
    """Testes para compressão de currículo."""

    def test_comprimir_curriculo_dentro_limite(self, otimizador):
        """Testa que currículo dentro do limite não é alterado."""
        curriculo = "Experiência: Desenvolvedor Python\nFormação: Ciência da Computação"
        max_tokens = 1000

        resultado = otimizador.comprimir_curriculo(curriculo, max_tokens)
        # Remove espaços extras mas mantém conteúdo
        assert "Desenvolvedor Python" in resultado
        assert "Ciência da Computação" in resultado

    def test_comprimir_curriculo_acima_limite(self, otimizador):
        """Testa compressão de currículo acima do limite."""
        curriculo = "Experiência: " + "Desenvolvedor Python. " * 100
        max_tokens = 50

        resultado = otimizador.comprimir_curriculo(curriculo, max_tokens)

        assert len(resultado) < len(curriculo)
        assert otimizador.contar_tokens(resultado) <= max_tokens
        # Deve preservar o início
        assert resultado.startswith("Experiência:")


class TestComprimirVaga:
    """Testes para compressão de vaga."""

    def test_comprimir_vaga_dentro_limite(self, otimizador):
        """Testa que vaga dentro do limite não é alterada."""
        vaga = "Requisitos: Python, FastAPI\nDiferenciais: Docker"
        max_tokens = 1000

        resultado = otimizador.comprimir_vaga(vaga, max_tokens)
        assert "Python" in resultado
        assert "FastAPI" in resultado

    def test_comprimir_vaga_acima_limite(self, otimizador):
        """Testa compressão de vaga acima do limite."""
        vaga = "Requisitos: " + "Python, FastAPI, Docker. " * 50
        max_tokens = 30

        resultado = otimizador.comprimir_vaga(vaga, max_tokens)

        assert len(resultado) < len(vaga)
        assert otimizador.contar_tokens(resultado) <= max_tokens
        assert resultado.startswith("Requisitos:")


class TestOtimizarPromptAnalise:
    """Testes para otimização de prompt de análise."""

    def test_otimizar_prompt_textos_pequenos(self, otimizador):
        """Testa otimização com textos pequenos."""
        vaga = "Desenvolvedor Python"
        curriculo = "5 anos de experiência com Python"

        vaga_otim, curriculo_otim = otimizador.otimizar_prompt_analise(vaga, curriculo)

        assert "Python" in vaga_otim
        assert "Python" in curriculo_otim

    def test_otimizar_prompt_textos_grandes(self, otimizador):
        """Testa otimização com textos grandes."""
        vaga = "Requisitos: " + "Python, FastAPI, Docker. " * 100
        curriculo = "Experiência: " + "Desenvolvedor Python. " * 200

        vaga_otim, curriculo_otim = otimizador.otimizar_prompt_analise(
            vaga, curriculo, max_tokens_total=1000
        )

        # Ambos devem ser comprimidos
        assert len(vaga_otim) < len(vaga)
        assert len(curriculo_otim) < len(curriculo)

        # Currículo deve ter mais tokens (70% vs 30%)
        tokens_vaga = otimizador.contar_tokens(vaga_otim)
        tokens_curriculo = otimizador.contar_tokens(curriculo_otim)
        assert tokens_curriculo > tokens_vaga

    def test_otimizar_prompt_limite_muito_baixo(self, otimizador):
        """Testa erro quando limite é muito baixo."""
        vaga = "Desenvolvedor Python"
        curriculo = "Experiência com Python"

        with pytest.raises(TokenLimitExceededError):
            otimizador.otimizar_prompt_analise(vaga, curriculo, max_tokens_total=100)


class TestValidarLimite:
    """Testes para validação de limite."""

    def test_validar_limite_dentro(self, otimizador):
        """Testa validação com mensagens dentro do limite."""
        mensagens = [{"role": "user", "content": "Olá"}]
        assert otimizador.validar_limite(mensagens, max_tokens=1000) is True

    def test_validar_limite_fora(self, otimizador):
        """Testa validação com mensagens fora do limite."""
        mensagens = [{"role": "user", "content": "Texto " * 1000}]
        assert otimizador.validar_limite(mensagens, max_tokens=10) is False


class TestObterEstatisticas:
    """Testes para obtenção de estatísticas."""

    def test_obter_estatisticas_texto_simples(self, otimizador):
        """Testa estatísticas de texto simples."""
        texto = "Python é incrível"
        stats = otimizador.obter_estatisticas(texto)

        assert stats["tokens"] > 0
        assert stats["caracteres"] == len(texto)
        assert stats["palavras"] == 3
        assert stats["linhas"] == 1
        assert stats["razao_tokens_palavras"] > 0

    def test_obter_estatisticas_texto_vazio(self, otimizador):
        """Testa estatísticas de texto vazio."""
        stats = otimizador.obter_estatisticas("")

        assert stats["tokens"] == 0
        assert stats["caracteres"] == 0
        assert stats["palavras"] == 0
        assert stats["razao_tokens_palavras"] == 0

    def test_obter_estatisticas_texto_multilinhas(self, otimizador):
        """Testa estatísticas de texto com múltiplas linhas."""
        texto = "Linha 1\nLinha 2\nLinha 3"
        stats = otimizador.obter_estatisticas(texto)

        assert stats["linhas"] == 3
        assert stats["palavras"] == 6
