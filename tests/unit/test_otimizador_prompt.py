"""Testes unitários para OtimizadorPrompt."""
from unittest.mock import patch, MagicMock
from app.models.domain import Vaga
from app.processors.otimizador_prompt import OtimizadorPrompt


def _vaga_fixture() -> Vaga:
    return Vaga(
        id=1,
        titulo="Dev Python",
        descricao="Vaga backend",
        requisitos_tecnicos=["Python", "FastAPI"],
        experiencia_minima="2 anos",
        competencias_desejadas=["Comunicação"],
    )


def test_otimizar_retorna_prompt_otimizado():
    with patch("tiktoken.encoding_for_model") as mock_enc:
        enc = MagicMock()
        enc.encode.return_value = list(range(100))
        mock_enc.return_value = enc

        otimizador = OtimizadorPrompt()
        resultado = otimizador.otimizar(_vaga_fixture(), "Experiência: Python 3 anos")

        assert resultado.conteudo
        assert resultado.tokens_estimados == 100


def test_otimizar_resume_quando_excede_limite():
    with patch("tiktoken.encoding_for_model") as mock_enc:
        enc = MagicMock()
        # Primeira chamada excede, segunda dentro do limite
        enc.encode.side_effect = [list(range(3000)), list(range(500))]
        mock_enc.return_value = enc

        otimizador = OtimizadorPrompt(max_tokens=2000)
        texto_longo = "experiência " + ("x " * 300)
        resultado = otimizador.otimizar(_vaga_fixture(), texto_longo)

        assert resultado.tokens_estimados == 500
