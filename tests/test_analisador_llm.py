"""Testes para o analisador LLM."""

from datetime import datetime
from unittest.mock import AsyncMock, Mock, patch

import pytest

from app.config import Settings
from app.models.analise import ResultadoAnalise
from app.processors.analisador_llm import AnalisadorLLM
from app.processors.exceptions import LLMError


@pytest.fixture
def mock_settings():
    """Fixture com configurações mockadas."""
    return Settings(
        openai_api_key="sk-test-key",
        openai_model="gpt-4o-mini",
        openai_max_tokens=2000,
    )


@pytest.fixture
def analisador(mock_settings):
    """Fixture com analisador inicializado."""
    return AnalisadorLLM(settings=mock_settings)


@pytest.fixture
def texto_vaga():
    """Fixture com texto de vaga de exemplo."""
    return """Desenvolvedor Python Sênior

Requisitos:
- 5+ anos de experiência com Python
- Experiência com FastAPI e Django
- Conhecimento em bancos de dados SQL
- Experiência com Docker e Kubernetes
- Inglês avançado"""


@pytest.fixture
def texto_curriculo():
    """Fixture com texto de currículo de exemplo."""
    return """João Silva
Desenvolvedor Python

Experiência:
- 6 anos desenvolvendo em Python
- Trabalhou com FastAPI em projetos recentes
- Experiência com PostgreSQL e MySQL
- Conhecimento básico de Docker

Formação:
- Bacharelado em Ciência da Computação

Idiomas:
- Inglês intermediário"""


@pytest.fixture
def resposta_llm_valida():
    """Fixture com resposta válida do LLM."""
    return """{
    "score": 75,
    "justificativa": "Candidato possui experiência sólida em Python e FastAPI, atendendo os requisitos principais. Porém, falta experiência com Kubernetes e o nível de inglês está abaixo do esperado.",
    "pontos_fortes": [
        "6 anos de experiência com Python, superando o requisito mínimo",
        "Experiência prática com FastAPI",
        "Conhecimento em bancos de dados SQL"
    ],
    "gaps": [
        "Falta experiência com Kubernetes",
        "Inglês intermediário, quando o requisito é avançado",
        "Conhecimento básico de Docker, quando é esperado experiência mais sólida"
    ]
}"""


class TestConstruirPrompt:
    """Testes para construção de prompt."""

    def test_construir_prompt_estrutura(self, analisador, texto_vaga, texto_curriculo):
        """Testa que o prompt é construído com estrutura correta."""
        prompt = analisador._construir_prompt(texto_vaga, texto_curriculo)

        assert prompt.sistema is not None
        assert prompt.usuario is not None
        assert prompt.formato_resposta is not None
        assert "especialista em recrutamento" in prompt.sistema.lower()
        assert "VAGA:" in prompt.usuario
        assert "CURRÍCULO:" in prompt.usuario

    def test_construir_prompt_to_messages(self, analisador, texto_vaga, texto_curriculo):
        """Testa conversão do prompt para mensagens OpenAI."""
        prompt = analisador._construir_prompt(texto_vaga, texto_curriculo)
        mensagens = prompt.to_messages()

        assert len(mensagens) == 2
        assert mensagens[0]["role"] == "system"
        assert mensagens[1]["role"] == "user"
        assert isinstance(mensagens[0]["content"], str)
        assert isinstance(mensagens[1]["content"], str)


class TestExtrairJsonResposta:
    """Testes para extração de JSON da resposta."""

    def test_extrair_json_resposta_valida(self, analisador, resposta_llm_valida):
        """Testa extração de JSON válido."""
        dados = analisador._extrair_json_resposta(resposta_llm_valida)

        assert isinstance(dados, dict)
        assert "score" in dados
        assert "justificativa" in dados
        assert "pontos_fortes" in dados
        assert "gaps" in dados

    def test_extrair_json_com_texto_extra(self, analisador):
        """Testa extração de JSON com texto adicional."""
        resposta = """Aqui está a análise:

{"score": 80, "justificativa": "Bom candidato", "pontos_fortes": ["Python"], "gaps": ["Kubernetes"]}

Espero que ajude!"""

        dados = analisador._extrair_json_resposta(resposta)

        assert dados["score"] == 80
        assert dados["justificativa"] == "Bom candidato"

    def test_extrair_json_invalido_levanta_erro(self, analisador):
        """Testa que JSON inválido levanta erro."""
        resposta = "Isso não é um JSON válido"

        with pytest.raises(LLMError) as exc_info:
            analisador._extrair_json_resposta(resposta)

        assert "JSON válido" in str(exc_info.value)


class TestValidarResposta:
    """Testes para validação da resposta."""

    def test_validar_resposta_valida(self, analisador):
        """Testa validação de resposta válida."""
        dados = {
            "score": 75,
            "justificativa": "Bom candidato",
            "pontos_fortes": ["Python", "FastAPI"],
            "gaps": ["Kubernetes"],
        }

        # Não deve levantar exceção
        analisador._validar_resposta(dados)

    def test_validar_resposta_campo_ausente(self, analisador):
        """Testa erro quando campo obrigatório está ausente."""
        dados = {
            "score": 75,
            "justificativa": "Bom candidato",
            # Falta pontos_fortes e gaps
        }

        with pytest.raises(LLMError) as exc_info:
            analisador._validar_resposta(dados)

        assert "ausente" in str(exc_info.value)

    def test_validar_resposta_score_invalido(self, analisador):
        """Testa erro quando score está fora do intervalo."""
        dados = {
            "score": 150,  # Inválido
            "justificativa": "Bom candidato",
            "pontos_fortes": ["Python"],
            "gaps": ["Kubernetes"],
        }

        with pytest.raises(LLMError) as exc_info:
            analisador._validar_resposta(dados)

        assert "0-100" in str(exc_info.value)

    def test_validar_resposta_tipo_incorreto(self, analisador):
        """Testa erro quando tipo de campo está incorreto."""
        dados = {
            "score": "75",  # Deveria ser int
            "justificativa": "Bom candidato",
            "pontos_fortes": ["Python"],
            "gaps": ["Kubernetes"],
        }

        with pytest.raises(LLMError) as exc_info:
            analisador._validar_resposta(dados)

        assert "inteiro" in str(exc_info.value)

    def test_validar_resposta_justificativa_vazia(self, analisador):
        """Testa erro quando justificativa está vazia."""
        dados = {
            "score": 75,
            "justificativa": "   ",  # Vazia
            "pontos_fortes": ["Python"],
            "gaps": ["Kubernetes"],
        }

        with pytest.raises(LLMError) as exc_info:
            analisador._validar_resposta(dados)

        assert "vazia" in str(exc_info.value)


class TestAnalisar:
    """Testes para o método analisar."""

    @patch("app.processors.analisador_llm.OpenAIClient")
    @patch("app.processors.analisador_llm.OtimizadorPrompt")
    def test_analisar_sucesso(
        self,
        mock_otimizador_class,
        mock_openai_class,
        mock_settings,
        texto_vaga,
        texto_curriculo,
        resposta_llm_valida,
    ):
        """Testa análise bem-sucedida."""
        # Mock do otimizador
        mock_otimizador = Mock()
        mock_otimizador.otimizar_prompt_analise.return_value = (
            texto_vaga,
            texto_curriculo,
        )
        mock_otimizador.validar_limite.return_value = True
        mock_otimizador.contar_tokens_mensagens.return_value = 500
        mock_otimizador.contar_tokens.return_value = 200
        mock_otimizador_class.return_value = mock_otimizador

        # Mock do cliente OpenAI
        mock_client = Mock()
        mock_client.chat_completion.return_value = resposta_llm_valida
        mock_openai_class.return_value = mock_client

        # Cria analisador e executa análise
        analisador = AnalisadorLLM(settings=mock_settings)
        resultado = analisador.analisar(texto_vaga, texto_curriculo, curriculo_id=1, vaga_id=1)

        # Verifica resultado
        assert isinstance(resultado, ResultadoAnalise)
        assert resultado.score == 75
        assert "experiência sólida" in resultado.justificativa.lower()
        assert len(resultado.pontos_fortes) == 3
        assert len(resultado.gaps) == 3
        assert resultado.curriculo_id == 1
        assert resultado.vaga_id == 1
        assert isinstance(resultado.data_analise, datetime)
        assert resultado.tokens_usados > 0

    @patch("app.processors.analisador_llm.OpenAIClient")
    @patch("app.processors.analisador_llm.OtimizadorPrompt")
    def test_analisar_excede_limite_tokens(
        self,
        mock_otimizador_class,
        mock_openai_class,
        mock_settings,
        texto_vaga,
        texto_curriculo,
    ):
        """Testa erro quando prompt excede limite de tokens."""
        # Mock do otimizador retornando que excedeu limite
        mock_otimizador = Mock()
        mock_otimizador.otimizar_prompt_analise.return_value = (
            texto_vaga,
            texto_curriculo,
        )
        mock_otimizador.validar_limite.return_value = False
        mock_otimizador.contar_tokens_mensagens.return_value = 3000
        mock_otimizador_class.return_value = mock_otimizador

        mock_openai_class.return_value = Mock()

        analisador = AnalisadorLLM(settings=mock_settings)

        with pytest.raises(LLMError) as exc_info:
            analisador.analisar(texto_vaga, texto_curriculo, curriculo_id=1, vaga_id=1)

        assert "excede limite" in str(exc_info.value)

    @patch("app.processors.analisador_llm.OpenAIClient")
    @patch("app.processors.analisador_llm.OtimizadorPrompt")
    def test_analisar_resposta_invalida(
        self,
        mock_otimizador_class,
        mock_openai_class,
        mock_settings,
        texto_vaga,
        texto_curriculo,
    ):
        """Testa erro quando LLM retorna resposta inválida."""
        # Mock do otimizador
        mock_otimizador = Mock()
        mock_otimizador.otimizar_prompt_analise.return_value = (
            texto_vaga,
            texto_curriculo,
        )
        mock_otimizador.validar_limite.return_value = True
        mock_otimizador_class.return_value = mock_otimizador

        # Mock do cliente retornando resposta inválida
        mock_client = Mock()
        mock_client.chat_completion.return_value = "Resposta sem JSON válido"
        mock_openai_class.return_value = mock_client

        analisador = AnalisadorLLM(settings=mock_settings)

        with pytest.raises(LLMError):
            analisador.analisar(texto_vaga, texto_curriculo, curriculo_id=1, vaga_id=1)


class TestAnalisarAsync:
    """Testes para o método analisar_async."""

    @pytest.mark.asyncio
    @patch("app.processors.analisador_llm.OpenAIClient")
    @patch("app.processors.analisador_llm.OtimizadorPrompt")
    async def test_analisar_async_sucesso(
        self,
        mock_otimizador_class,
        mock_openai_class,
        mock_settings,
        texto_vaga,
        texto_curriculo,
        resposta_llm_valida,
    ):
        """Testa análise assíncrona bem-sucedida."""
        # Mock do otimizador
        mock_otimizador = Mock()
        mock_otimizador.otimizar_prompt_analise.return_value = (
            texto_vaga,
            texto_curriculo,
        )
        mock_otimizador.validar_limite.return_value = True
        mock_otimizador.contar_tokens_mensagens.return_value = 500
        mock_otimizador.contar_tokens.return_value = 200
        mock_otimizador_class.return_value = mock_otimizador

        # Mock do cliente OpenAI com método assíncrono
        mock_client = Mock()
        mock_client.async_chat_completion = AsyncMock(return_value=resposta_llm_valida)
        mock_openai_class.return_value = mock_client

        # Cria analisador e executa análise assíncrona
        analisador = AnalisadorLLM(settings=mock_settings)
        resultado = await analisador.analisar_async(
            texto_vaga, texto_curriculo, curriculo_id=1, vaga_id=1
        )

        # Verifica resultado
        assert isinstance(resultado, ResultadoAnalise)
        assert resultado.score == 75
        assert resultado.curriculo_id == 1
        assert resultado.vaga_id == 1
        mock_client.async_chat_completion.assert_called_once()
