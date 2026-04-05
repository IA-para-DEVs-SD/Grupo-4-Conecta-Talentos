"""Testes para o serviço de ranking."""

from datetime import datetime
from unittest.mock import AsyncMock, Mock, patch

import pytest

from app.models.domain import Analise, Curriculo, Vaga
from app.processors.exceptions import LLMError
from app.services.ranking_service import RankingService


@pytest.fixture
def mock_db():
    """Fixture com sessão mockada do banco."""
    return Mock()


@pytest.fixture
def vaga_exemplo():
    """Fixture com vaga de exemplo."""
    return Vaga(
        id=1,
        titulo="Desenvolvedor Python Sênior",
        descricao="Vaga para desenvolvedor Python experiente",
        requisitos="Python, FastAPI, PostgreSQL",
        experiencia_minima="5 anos",
        competencias="Liderança, Comunicação",
    )


@pytest.fixture
def curriculos_exemplo():
    """Fixture com currículos de exemplo."""
    return [
        Curriculo(
            id=1,
            vaga_id=1,
            nome_arquivo="curriculo1.pdf",
            caminho_arquivo="/uploads/curriculo1.pdf",
            texto_extraido="João Silva, 6 anos de experiência com Python e FastAPI",
        ),
        Curriculo(
            id=2,
            vaga_id=1,
            nome_arquivo="curriculo2.pdf",
            caminho_arquivo="/uploads/curriculo2.pdf",
            texto_extraido="Maria Santos, 3 anos de experiência com Python",
        ),
        Curriculo(
            id=3,
            vaga_id=1,
            nome_arquivo="curriculo3.pdf",
            caminho_arquivo="/uploads/curriculo3.pdf",
            texto_extraido="Pedro Costa, 8 anos de experiência com Python, FastAPI e PostgreSQL",
        ),
    ]


@pytest.fixture
def analises_exemplo():
    """Fixture com análises de exemplo."""
    return [
        Analise(
            id=1,
            curriculo_id=1,
            score=85,
            justificativa="Ótimo candidato com experiência relevante",
            pontos_fortes=["Experiência com Python", "Conhece FastAPI"],
            gaps=["Falta experiência com PostgreSQL"],
            tokens_usados=500,
            analisado_em=datetime.now(),
        ),
        Analise(
            id=2,
            curriculo_id=2,
            score=60,
            justificativa="Candidato júnior, falta experiência",
            pontos_fortes=["Conhece Python"],
            gaps=["Pouca experiência", "Não conhece FastAPI"],
            tokens_usados=450,
            analisado_em=datetime.now(),
        ),
        Analise(
            id=3,
            curriculo_id=3,
            score=95,
            justificativa="Excelente candidato, atende todos os requisitos",
            pontos_fortes=["Muita experiência", "Domina todas as tecnologias"],
            gaps=["Nenhum gap significativo"],
            tokens_usados=550,
            analisado_em=datetime.now(),
        ),
    ]


class TestRankingServiceInit:
    """Testes de inicialização do serviço."""

    def test_init_cria_repositorios(self, mock_db):
        """Testa que inicialização cria repositórios."""
        service = RankingService(mock_db)

        assert service.db == mock_db
        assert service.vaga_repo is not None
        assert service.curriculo_repo is not None
        assert service.analise_repo is not None
        assert service.analisador is not None


class TestGerarRanking:
    """Testes para geração de ranking."""

    @patch("app.services.ranking_service.VagaRepository")
    @patch("app.services.ranking_service.CurriculoRepository")
    @patch("app.services.ranking_service.AnaliseRepository")
    @patch("app.services.ranking_service.AnalisadorLLM")
    def test_gerar_ranking_vaga_nao_encontrada(
        self,
        mock_analisador_class,
        mock_analise_repo_class,
        mock_curriculo_repo_class,
        mock_vaga_repo_class,
        mock_db,
    ):
        """Testa erro quando vaga não existe."""
        # Mock repositório retornando None
        mock_vaga_repo = Mock()
        mock_vaga_repo.obter_por_id.return_value = None
        mock_vaga_repo_class.return_value = mock_vaga_repo

        service = RankingService(mock_db)

        with pytest.raises(ValueError) as exc_info:
            service.gerar_ranking(999)

        assert "não encontrada" in str(exc_info.value)

    @patch("app.services.ranking_service.VagaRepository")
    @patch("app.services.ranking_service.CurriculoRepository")
    @patch("app.services.ranking_service.AnaliseRepository")
    @patch("app.services.ranking_service.AnalisadorLLM")
    def test_gerar_ranking_sem_curriculos(
        self,
        mock_analisador_class,
        mock_analise_repo_class,
        mock_curriculo_repo_class,
        mock_vaga_repo_class,
        mock_db,
        vaga_exemplo,
    ):
        """Testa ranking vazio quando não há currículos."""
        # Mock repositórios
        mock_vaga_repo = Mock()
        mock_vaga_repo.obter_por_id.return_value = vaga_exemplo
        mock_vaga_repo_class.return_value = mock_vaga_repo

        mock_curriculo_repo = Mock()
        mock_curriculo_repo.listar_por_vaga.return_value = []
        mock_curriculo_repo_class.return_value = mock_curriculo_repo

        service = RankingService(mock_db)
        ranking = service.gerar_ranking(1)

        assert ranking == []

    @patch("app.services.ranking_service.VagaRepository")
    @patch("app.services.ranking_service.CurriculoRepository")
    @patch("app.services.ranking_service.AnaliseRepository")
    @patch("app.services.ranking_service.AnalisadorLLM")
    def test_gerar_ranking_usa_analises_existentes(
        self,
        mock_analisador_class,
        mock_analise_repo_class,
        mock_curriculo_repo_class,
        mock_vaga_repo_class,
        mock_db,
        vaga_exemplo,
        curriculos_exemplo,
        analises_exemplo,
    ):
        """Testa que usa análises existentes quando reprocessar=False."""
        # Mock repositórios
        mock_vaga_repo = Mock()
        mock_vaga_repo.obter_por_id.return_value = vaga_exemplo
        mock_vaga_repo_class.return_value = mock_vaga_repo

        mock_curriculo_repo = Mock()
        mock_curriculo_repo.listar_por_vaga.return_value = curriculos_exemplo
        mock_curriculo_repo_class.return_value = mock_curriculo_repo

        mock_analise_repo = Mock()
        # Retorna análises existentes
        mock_analise_repo.obter_por_curriculo.side_effect = analises_exemplo
        mock_analise_repo_class.return_value = mock_analise_repo

        service = RankingService(mock_db)
        ranking = service.gerar_ranking(1, reprocessar=False)

        # Verifica que não chamou o analisador
        mock_analisador_class.return_value.analisar.assert_not_called()

        # Verifica ordenação (maior score primeiro)
        assert len(ranking) == 3
        assert ranking[0].score == 95
        assert ranking[1].score == 85
        assert ranking[2].score == 60

    @patch("app.services.ranking_service.VagaRepository")
    @patch("app.services.ranking_service.CurriculoRepository")
    @patch("app.services.ranking_service.AnaliseRepository")
    @patch("app.services.ranking_service.AnalisadorLLM")
    def test_gerar_ranking_reprocessa_quando_solicitado(
        self,
        mock_analisador_class,
        mock_analise_repo_class,
        mock_curriculo_repo_class,
        mock_vaga_repo_class,
        mock_db,
        vaga_exemplo,
        curriculos_exemplo,
    ):
        """Testa que reprocessa análises quando reprocessar=True."""
        # Mock repositórios
        mock_vaga_repo = Mock()
        mock_vaga_repo.obter_por_id.return_value = vaga_exemplo
        mock_vaga_repo_class.return_value = mock_vaga_repo

        mock_curriculo_repo = Mock()
        mock_curriculo_repo.listar_por_vaga.return_value = curriculos_exemplo
        mock_curriculo_repo_class.return_value = mock_curriculo_repo

        mock_analise_repo = Mock()
        mock_analise_repo.obter_por_curriculo.return_value = Mock()  # Existe análise
        mock_analise_repo.criar.side_effect = lambda a: a
        mock_analise_repo_class.return_value = mock_analise_repo

        # Mock analisador
        mock_analisador = Mock()
        mock_resultado = Mock()
        mock_resultado.curriculo_id = 1
        mock_resultado.score = 80
        mock_resultado.justificativa = "Bom candidato"
        mock_resultado.pontos_fortes = ["Python"]
        mock_resultado.gaps = ["PostgreSQL"]
        mock_resultado.tokens_usados = 500
        mock_resultado.data_analise = datetime.now()
        mock_analisador.analisar.return_value = mock_resultado
        mock_analisador_class.return_value = mock_analisador

        service = RankingService(mock_db)
        ranking = service.gerar_ranking(1, reprocessar=True)

        # Verifica que chamou o analisador para cada currículo
        assert mock_analisador.analisar.call_count == 3

    @patch("app.services.ranking_service.VagaRepository")
    @patch("app.services.ranking_service.CurriculoRepository")
    @patch("app.services.ranking_service.AnaliseRepository")
    @patch("app.services.ranking_service.AnalisadorLLM")
    def test_gerar_ranking_continua_apos_erro(
        self,
        mock_analisador_class,
        mock_analise_repo_class,
        mock_curriculo_repo_class,
        mock_vaga_repo_class,
        mock_db,
        vaga_exemplo,
        curriculos_exemplo,
    ):
        """Testa que continua processando após erro em um currículo."""
        # Mock repositórios
        mock_vaga_repo = Mock()
        mock_vaga_repo.obter_por_id.return_value = vaga_exemplo
        mock_vaga_repo_class.return_value = mock_vaga_repo

        mock_curriculo_repo = Mock()
        mock_curriculo_repo.listar_por_vaga.return_value = curriculos_exemplo
        mock_curriculo_repo_class.return_value = mock_curriculo_repo

        mock_analise_repo = Mock()
        mock_analise_repo.obter_por_curriculo.return_value = None
        mock_analise_repo.criar.side_effect = lambda a: a
        mock_analise_repo_class.return_value = mock_analise_repo

        # Mock analisador - primeiro falha, depois sucede
        mock_analisador = Mock()
        mock_resultado = Mock()
        mock_resultado.curriculo_id = 2
        mock_resultado.score = 70
        mock_resultado.justificativa = "OK"
        mock_resultado.pontos_fortes = ["Python"]
        mock_resultado.gaps = []
        mock_resultado.tokens_usados = 400
        mock_resultado.data_analise = datetime.now()

        mock_analisador.analisar.side_effect = [
            LLMError("Erro no primeiro"),
            mock_resultado,
            mock_resultado,
        ]
        mock_analisador_class.return_value = mock_analisador

        service = RankingService(mock_db)
        ranking = service.gerar_ranking(1, reprocessar=False)

        # Deve ter processado 2 dos 3 currículos
        assert len(ranking) == 2


class TestGerarRankingAsync:
    """Testes para geração assíncrona de ranking."""

    @pytest.mark.asyncio
    @patch("app.services.ranking_service.VagaRepository")
    @patch("app.services.ranking_service.CurriculoRepository")
    @patch("app.services.ranking_service.AnaliseRepository")
    @patch("app.services.ranking_service.AnalisadorLLM")
    async def test_gerar_ranking_async_sucesso(
        self,
        mock_analisador_class,
        mock_analise_repo_class,
        mock_curriculo_repo_class,
        mock_vaga_repo_class,
        mock_db,
        vaga_exemplo,
        curriculos_exemplo,
    ):
        """Testa geração assíncrona de ranking."""
        # Mock repositórios
        mock_vaga_repo = Mock()
        mock_vaga_repo.obter_por_id.return_value = vaga_exemplo
        mock_vaga_repo_class.return_value = mock_vaga_repo

        mock_curriculo_repo = Mock()
        mock_curriculo_repo.listar_por_vaga.return_value = curriculos_exemplo
        mock_curriculo_repo_class.return_value = mock_curriculo_repo

        mock_analise_repo = Mock()
        mock_analise_repo.obter_por_curriculo.return_value = None
        mock_analise_repo.criar.side_effect = lambda a: a
        mock_analise_repo_class.return_value = mock_analise_repo

        # Mock analisador assíncrono
        mock_analisador = Mock()
        mock_resultado = Mock()
        mock_resultado.curriculo_id = 1
        mock_resultado.score = 80
        mock_resultado.justificativa = "Bom"
        mock_resultado.pontos_fortes = ["Python"]
        mock_resultado.gaps = []
        mock_resultado.tokens_usados = 500
        mock_resultado.data_analise = datetime.now()

        mock_analisador.analisar_async = AsyncMock(return_value=mock_resultado)
        mock_analisador_class.return_value = mock_analisador

        service = RankingService(mock_db)
        ranking = await service.gerar_ranking_async(1)

        assert len(ranking) == 3
        assert mock_analisador.analisar_async.call_count == 3


class TestObterRankingExistente:
    """Testes para obtenção de ranking existente."""

    @patch("app.services.ranking_service.VagaRepository")
    @patch("app.services.ranking_service.CurriculoRepository")
    @patch("app.services.ranking_service.AnaliseRepository")
    @patch("app.services.ranking_service.AnalisadorLLM")
    def test_obter_ranking_existente_sucesso(
        self,
        mock_analisador_class,
        mock_analise_repo_class,
        mock_curriculo_repo_class,
        mock_vaga_repo_class,
        mock_db,
        vaga_exemplo,
        analises_exemplo,
    ):
        """Testa obtenção de ranking existente."""
        # Mock repositórios
        mock_vaga_repo = Mock()
        mock_vaga_repo.obter_por_id.return_value = vaga_exemplo
        mock_vaga_repo_class.return_value = mock_vaga_repo

        mock_analise_repo = Mock()
        mock_analise_repo.listar_por_vaga.return_value = analises_exemplo
        mock_analise_repo_class.return_value = mock_analise_repo

        service = RankingService(mock_db)
        ranking = service.obter_ranking_existente(1)

        assert len(ranking) == 3
        mock_analise_repo.listar_por_vaga.assert_called_once_with(1)


class TestFiltrarPorScoreMinimo:
    """Testes para filtro por score mínimo."""

    def test_filtrar_por_score_minimo(self, mock_db, analises_exemplo):
        """Testa filtro por pontuação mínima."""
        service = RankingService(mock_db)
        filtradas = service.filtrar_por_score_minimo(analises_exemplo, 70)

        assert len(filtradas) == 2
        assert all(a.score >= 70 for a in filtradas)

    def test_filtrar_score_minimo_zero(self, mock_db, analises_exemplo):
        """Testa que score mínimo 0 retorna todos."""
        service = RankingService(mock_db)
        filtradas = service.filtrar_por_score_minimo(analises_exemplo, 0)

        assert len(filtradas) == 3

    def test_filtrar_score_minimo_alto(self, mock_db, analises_exemplo):
        """Testa filtro com score muito alto."""
        service = RankingService(mock_db)
        filtradas = service.filtrar_por_score_minimo(analises_exemplo, 100)

        assert len(filtradas) == 0


class TestObterTopCandidatos:
    """Testes para obtenção de top candidatos."""

    @patch("app.services.ranking_service.VagaRepository")
    @patch("app.services.ranking_service.CurriculoRepository")
    @patch("app.services.ranking_service.AnaliseRepository")
    @patch("app.services.ranking_service.AnalisadorLLM")
    def test_obter_top_candidatos(
        self,
        mock_analisador_class,
        mock_analise_repo_class,
        mock_curriculo_repo_class,
        mock_vaga_repo_class,
        mock_db,
        vaga_exemplo,
        analises_exemplo,
    ):
        """Testa obtenção dos top N candidatos."""
        # Mock repositórios
        mock_vaga_repo = Mock()
        mock_vaga_repo.obter_por_id.return_value = vaga_exemplo
        mock_vaga_repo_class.return_value = mock_vaga_repo

        mock_analise_repo = Mock()
        # Retorna ordenado por score
        analises_ordenadas = sorted(
            analises_exemplo, key=lambda a: a.score, reverse=True
        )
        mock_analise_repo.listar_por_vaga.return_value = analises_ordenadas
        mock_analise_repo_class.return_value = mock_analise_repo

        service = RankingService(mock_db)
        top_2 = service.obter_top_candidatos(1, limite=2)

        assert len(top_2) == 2
        assert top_2[0].score == 95
        assert top_2[1].score == 85


class TestFormatarTextoVaga:
    """Testes para formatação de texto da vaga."""

    def test_formatar_texto_vaga_completo(self, mock_db, vaga_exemplo):
        """Testa formatação com todos os campos."""
        service = RankingService(mock_db)
        texto = service._formatar_texto_vaga(vaga_exemplo)

        assert "Desenvolvedor Python Sênior" in texto
        assert "Python, FastAPI, PostgreSQL" in texto
        assert "5 anos" in texto
        assert "Liderança, Comunicação" in texto

    def test_formatar_texto_vaga_sem_opcionais(self, mock_db):
        """Testa formatação sem campos opcionais."""
        vaga = Vaga(
            id=1,
            titulo="Dev Python",
            descricao="Descrição",
            requisitos="Python",
            experiencia_minima=None,
            competencias=None,
        )

        service = RankingService(mock_db)
        texto = service._formatar_texto_vaga(vaga)

        assert "Dev Python" in texto
        assert "Python" in texto
        assert "Experiência Mínima" not in texto
        assert "Competências" not in texto
