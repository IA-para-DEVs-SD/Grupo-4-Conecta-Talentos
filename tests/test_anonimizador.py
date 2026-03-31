"""Testes unitários e de integração do módulo Anonimizador."""

from unittest.mock import MagicMock, patch

import pytest

from app.processors.anonimizador import (
    Anonimizador,
    AnonimizadorError,
    PresidioIndisponivelError,
    ResultadoAnonimizacao,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _anonimizador_regex() -> Anonimizador:
    """Retorna Anonimizador forçado a usar fallback regex (sem Presidio)."""
    with patch(
        "app.processors.anonimizador._criar_engine_presidio",
        side_effect=PresidioIndisponivelError("Presidio não instalado"),
    ):
        return Anonimizador(usar_fallback_regex=True)


# ---------------------------------------------------------------------------
# Testes do ResultadoAnonimizacao
# ---------------------------------------------------------------------------


class TestResultadoAnonimizacao:
    def test_defaults(self):
        r = ResultadoAnonimizacao(texto_anonimizado="texto")
        assert r.sucesso is True
        assert r.total_substituicoes == 0
        assert r.entidades_encontradas == []
        assert r.erro is None


# ---------------------------------------------------------------------------
# Testes do fallback regex
# ---------------------------------------------------------------------------


class TestAnonimizadorRegex:
    def test_anonimiza_cpf_com_pontuacao(self):
        anon = _anonimizador_regex()
        resultado = anon.anonimizar("Meu CPF é 123.456.789-09")
        assert "[CPF]" in resultado.texto_anonimizado
        assert "123.456.789-09" not in resultado.texto_anonimizado

    def test_anonimiza_cpf_sem_pontuacao(self):
        anon = _anonimizador_regex()
        resultado = anon.anonimizar("CPF: 12345678909")
        assert "[CPF]" in resultado.texto_anonimizado

    def test_anonimiza_email(self):
        anon = _anonimizador_regex()
        resultado = anon.anonimizar("Contato: joao.silva@empresa.com.br")
        assert "[EMAIL]" in resultado.texto_anonimizado
        assert "joao.silva@empresa.com.br" not in resultado.texto_anonimizado

    def test_anonimiza_telefone(self):
        anon = _anonimizador_regex()
        resultado = anon.anonimizar("Telefone: (51) 99999-8888")
        assert "[TELEFONE]" in resultado.texto_anonimizado

    def test_anonimiza_cep(self):
        anon = _anonimizador_regex()
        resultado = anon.anonimizar("Endereço: Rua X, CEP 90000-000")
        assert "[CEP]" in resultado.texto_anonimizado

    def test_preserva_informacoes_profissionais(self):
        anon = _anonimizador_regex()
        texto = "Desenvolvedor Python com 5 anos de experiência em FastAPI e SQLAlchemy."
        resultado = anon.anonimizar(texto)
        assert "Python" in resultado.texto_anonimizado
        assert "FastAPI" in resultado.texto_anonimizado
        assert "SQLAlchemy" in resultado.texto_anonimizado

    def test_texto_vazio_retorna_sem_erro(self):
        anon = _anonimizador_regex()
        resultado = anon.anonimizar("")
        assert resultado.texto_anonimizado == ""
        assert resultado.sucesso is True

    def test_texto_sem_pii_nao_altera(self):
        anon = _anonimizador_regex()
        texto = "Experiência em Python, Docker e Kubernetes."
        resultado = anon.anonimizar(texto)
        assert resultado.texto_anonimizado == texto
        assert resultado.total_substituicoes == 0

    def test_multiplos_pii_no_mesmo_texto(self):
        anon = _anonimizador_regex()
        texto = "João, CPF 111.222.333-44, email: joao@test.com, tel: (11) 91234-5678"
        resultado = anon.anonimizar(texto)
        assert "[CPF]" in resultado.texto_anonimizado
        assert "[EMAIL]" in resultado.texto_anonimizado
        assert "[TELEFONE]" in resultado.texto_anonimizado
        assert resultado.total_substituicoes >= 3

    def test_modo_retorna_regex(self):
        anon = _anonimizador_regex()
        assert anon.modo == "regex"

    def test_contagem_entidades_encontradas(self):
        anon = _anonimizador_regex()
        resultado = anon.anonimizar("email@test.com e 123.456.789-09")
        assert "EMAIL_ADDRESS" in resultado.entidades_encontradas
        assert "BR_CPF" in resultado.entidades_encontradas


# ---------------------------------------------------------------------------
# Testes com Presidio mockado
# ---------------------------------------------------------------------------


class TestAnonimizadorPresidio:
    def test_usa_presidio_quando_disponivel(self):
        mock_result = MagicMock()
        mock_result.entity_type = "PERSON"

        mock_analyzer = MagicMock()
        mock_analyzer.analyze.return_value = [mock_result]

        mock_anon_result = MagicMock()
        mock_anon_result.text = "Olá [NOME], bem-vindo."

        mock_anonymizer = MagicMock()
        mock_anonymizer.anonymize.return_value = mock_anon_result

        with patch(
            "app.processors.anonimizador._criar_engine_presidio",
            return_value=(mock_analyzer, mock_anonymizer, {}),
        ):
            anon = Anonimizador()
            resultado = anon.anonimizar("Olá João Silva, bem-vindo.")

        assert resultado.texto_anonimizado == "Olá [NOME], bem-vindo."
        assert resultado.total_substituicoes == 1
        assert "PERSON" in resultado.entidades_encontradas
        assert anon.modo == "presidio"

    def test_fallback_regex_quando_presidio_falha_em_runtime(self):
        """Se Presidio lançar exceção durante análise, deve usar fallback regex."""
        mock_analyzer = MagicMock()
        mock_analyzer.analyze.side_effect = RuntimeError("Erro interno")

        with patch(
            "app.processors.anonimizador._criar_engine_presidio",
            return_value=(mock_analyzer, MagicMock(), {}),
        ):
            anon = Anonimizador(usar_fallback_regex=True)
            resultado = anon.anonimizar("email@test.com")

        assert "[EMAIL]" in resultado.texto_anonimizado

    def test_texto_sem_entidades_retorna_original(self):
        mock_analyzer = MagicMock()
        mock_analyzer.analyze.return_value = []

        with patch(
            "app.processors.anonimizador._criar_engine_presidio",
            return_value=(mock_analyzer, MagicMock(), {}),
        ):
            anon = Anonimizador()
            texto = "Experiência em Python e Docker."
            resultado = anon.anonimizar(texto)

        assert resultado.texto_anonimizado == texto
        assert resultado.total_substituicoes == 0


# ---------------------------------------------------------------------------
# Testes de configuração
# ---------------------------------------------------------------------------


class TestAnonimizadorConfig:
    def test_presidio_indisponivel_sem_fallback_lanca_erro(self):
        with patch(
            "app.processors.anonimizador._criar_engine_presidio",
            side_effect=PresidioIndisponivelError("Não instalado"),
        ):
            with pytest.raises(PresidioIndisponivelError):
                Anonimizador(usar_fallback_regex=False)

    def test_presidio_indisponivel_com_fallback_nao_lanca_erro(self):
        with patch(
            "app.processors.anonimizador._criar_engine_presidio",
            side_effect=PresidioIndisponivelError("Não instalado"),
        ):
            anon = Anonimizador(usar_fallback_regex=True)
            assert anon.modo == "regex"


# ---------------------------------------------------------------------------
# Testes de integração no pipeline (CurriculoService)
# ---------------------------------------------------------------------------


class TestAnonimizacaoPipeline:
    def test_pipeline_anonimiza_apos_extracao(self, db_session, tmp_path):
        """Após upload, texto_anonimizado deve ser preenchido e status = 'anonimizado'."""
        from app.models.domain import VagaCreate
        from app.repositories.vaga_repository import VagaRepository
        from app.services.curriculo_service import CurriculoService

        vaga_id = VagaRepository(db_session).criar(
            VagaCreate(
                titulo="Dev",
                descricao="Desc",
                requisitos_tecnicos=["Python"],
                experiencia_minima="1 ano",
                competencias_desejadas=["Comunicação"],
            )
        ).id

        texto_extraido = "João Silva, CPF 111.222.333-44, joao@email.com"
        service = CurriculoService(db_session)
        service.settings.upload_dir = str(tmp_path)

        with patch("app.services.curriculo_service.extrair_texto_pdf") as mock_ext:
            mock_ext.return_value = MagicMock(conteudo=texto_extraido)
            with patch(
                "app.processors.anonimizador._criar_engine_presidio",
                side_effect=PresidioIndisponivelError("sem presidio"),
            ):
                curriculo = service.upload(vaga_id, "cv.pdf", b"%PDF-fake")

        assert curriculo.status == "anonimizado"
        assert curriculo.texto_extraido == texto_extraido
        assert curriculo.texto_anonimizado is not None
        assert "[CPF]" in curriculo.texto_anonimizado

    def test_pipeline_preserva_texto_extraido_se_anonimizacao_falhar(
        self, db_session, tmp_path
    ):
        """Se anonimização falhar, texto_extraido deve ser preservado com status 'extraido'."""
        from app.models.domain import VagaCreate
        from app.repositories.vaga_repository import VagaRepository
        from app.services.curriculo_service import CurriculoService

        vaga_id = VagaRepository(db_session).criar(
            VagaCreate(
                titulo="Dev",
                descricao="Desc",
                requisitos_tecnicos=["Python"],
                experiencia_minima="1 ano",
                competencias_desejadas=["Comunicação"],
            )
        ).id

        service = CurriculoService(db_session)
        service.settings.upload_dir = str(tmp_path)

        with patch("app.services.curriculo_service.extrair_texto_pdf") as mock_ext:
            mock_ext.return_value = MagicMock(conteudo="texto extraído")
            with patch("app.services.curriculo_service.Anonimizador") as mock_anon_cls:
                mock_anon_cls.side_effect = AnonimizadorError("Falha total")
                curriculo = service.upload(vaga_id, "cv.pdf", b"%PDF-fake")

        assert curriculo.texto_extraido == "texto extraído"
        assert curriculo.status == "extraido"

    def test_texto_anonimizado_persistido_no_banco(self, db_session, tmp_path):
        """Texto anonimizado deve ser recuperável via repositório."""
        from app.models.domain import VagaCreate
        from app.repositories.curriculo_repository import CurriculoRepository
        from app.repositories.vaga_repository import VagaRepository
        from app.services.curriculo_service import CurriculoService

        vaga_id = VagaRepository(db_session).criar(
            VagaCreate(
                titulo="Dev",
                descricao="Desc",
                requisitos_tecnicos=["Python"],
                experiencia_minima="1 ano",
                competencias_desejadas=["Comunicação"],
            )
        ).id

        service = CurriculoService(db_session)
        service.settings.upload_dir = str(tmp_path)

        with patch("app.services.curriculo_service.extrair_texto_pdf") as mock_ext:
            mock_ext.return_value = MagicMock(conteudo="texto com cpf 111.222.333-44")
            with patch(
                "app.processors.anonimizador._criar_engine_presidio",
                side_effect=PresidioIndisponivelError("sem presidio"),
            ):
                curriculo = service.upload(vaga_id, "cv.pdf", b"%PDF-fake")

        salvo = CurriculoRepository(db_session).obter(curriculo.id)
        assert salvo.texto_anonimizado is not None
        assert "[CPF]" in salvo.texto_anonimizado
        assert "111.222.333-44" not in salvo.texto_anonimizado
