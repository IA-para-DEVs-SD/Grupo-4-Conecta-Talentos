"""Testes para o controller de ranking."""

from datetime import datetime
from unittest.mock import Mock, patch

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.models.domain import Analise, Curriculo, Vaga


@pytest.fixture
def client():
    """Fixture com cliente de teste."""
    return TestClient(app)


@pytest.fixture
def vaga_exemplo():
    """Fixture com vaga de exemplo."""
    return Vaga(
        id=1,
        titulo="Desenvolvedor Python",
        descricao="Vaga para dev Python",
        requisitos="Python, FastAPI",
        experiencia_minima="3 anos",
        competencias="Comunicação",
    )


@pytest.fixture
def curriculo_exemplo():
    """Fixture com currículo de exemplo."""
    return Curriculo(
        id=1,
        vaga_id=1,
        nome_arquivo="curriculo.pdf",
        caminho_arquivo="/uploads/curriculo.pdf",
        texto_extraido="João Silva, desenvolvedor Python",
        enviado_em=datetime.now(),
    )


@pytest.fixture
def analise_exemplo():
    """Fixture com análise de exemplo."""
    return Analise(
        id=1,
        curriculo_id=1,
        score=85,
        justificativa="Ótimo candidato",
        pontos_fortes=["Python", "FastAPI"],
        gaps=["Experiência com testes"],
        tokens_usados=500,
        analisado_em=datetime.now(),
    )


class TestObterDetalhesCandidato:
    """Testes para o endpoint de detalhes do candidato."""

    @patch("app.controllers.ranking_controller.RankingService")
    def test_obter_detalhes_candidato_sucesso(
        self,
        mock_ranking_service_class,
        client,
        vaga_exemplo,
        curriculo_exemplo,
        analise_exemplo,
    ):
        """Testa obtenção de detalhes com sucesso."""
        # Mock do serviço
        mock_service = Mock()
        mock_service.analise_repo.obter_por_curriculo.return_value = analise_exemplo
        mock_service.curriculo_repo.obter_por_id.return_value = curriculo_exemplo
        mock_service.vaga_repo.obter_por_id.return_value = vaga_exemplo
        mock_ranking_service_class.return_value = mock_service

        # Faz requisição
        response = client.get("/ranking/1/candidato/1")

        # Verifica resposta
        assert response.status_code == 200
        data = response.json()

        assert "vaga" in data
        assert data["vaga"]["id"] == 1
        assert data["vaga"]["titulo"] == "Desenvolvedor Python"

        assert "curriculo" in data
        assert data["curriculo"]["id"] == 1
        assert data["curriculo"]["nome_arquivo"] == "curriculo.pdf"

        assert "analise" in data
        assert data["analise"]["score"] == 85
        assert data["analise"]["justificativa"] == "Ótimo candidato"
        assert len(data["analise"]["pontos_fortes"]) == 2
        assert len(data["analise"]["gaps"]) == 1

    @patch("app.controllers.ranking_controller.RankingService")
    def test_obter_detalhes_analise_nao_encontrada(
        self, mock_ranking_service_class, client
    ):
        """Testa erro quando análise não existe."""
        # Mock do serviço retornando None
        mock_service = Mock()
        mock_service.analise_repo.obter_por_curriculo.return_value = None
        mock_ranking_service_class.return_value = mock_service

        # Faz requisição
        response = client.get("/ranking/1/candidato/999")

        # Verifica erro 404
        assert response.status_code == 404
        assert "não encontrada" in response.json()["detail"]

    @patch("app.controllers.ranking_controller.RankingService")
    def test_obter_detalhes_curriculo_nao_encontrado(
        self, mock_ranking_service_class, client, analise_exemplo
    ):
        """Testa erro quando currículo não existe."""
        # Mock do serviço
        mock_service = Mock()
        mock_service.analise_repo.obter_por_curriculo.return_value = analise_exemplo
        mock_service.curriculo_repo.obter_por_id.return_value = None
        mock_ranking_service_class.return_value = mock_service

        # Faz requisição
        response = client.get("/ranking/1/candidato/1")

        # Verifica erro 404
        assert response.status_code == 404
        assert "não encontrado" in response.json()["detail"]

    @patch("app.controllers.ranking_controller.RankingService")
    def test_obter_detalhes_curriculo_vaga_diferente(
        self,
        mock_ranking_service_class,
        client,
        analise_exemplo,
        curriculo_exemplo,
    ):
        """Testa erro quando currículo pertence a outra vaga."""
        # Mock do serviço
        curriculo_exemplo.vaga_id = 2  # Vaga diferente
        mock_service = Mock()
        mock_service.analise_repo.obter_por_curriculo.return_value = analise_exemplo
        mock_service.curriculo_repo.obter_por_id.return_value = curriculo_exemplo
        mock_ranking_service_class.return_value = mock_service

        # Faz requisição para vaga 1
        response = client.get("/ranking/1/candidato/1")

        # Verifica erro 404
        assert response.status_code == 404
        assert "não encontrado para a vaga" in response.json()["detail"]


class TestVisualizarRanking:
    """Testes para o endpoint de visualização de ranking."""

    @patch("app.controllers.ranking_controller.RankingService")
    def test_visualizar_ranking_com_filtro_score(
        self, mock_ranking_service_class, client, analise_exemplo
    ):
        """Testa visualização com filtro de score mínimo."""
        # Mock do serviço
        mock_service = Mock()
        mock_service.obter_ranking_existente.return_value = [analise_exemplo]
        mock_service.filtrar_por_score_minimo.return_value = [analise_exemplo]
        mock_ranking_service_class.return_value = mock_service

        # Faz requisição com filtro
        response = client.get("/ranking/1?score_minimo=70")

        # Verifica que chamou o filtro
        assert response.status_code == 200
        mock_service.filtrar_por_score_minimo.assert_called_once()

    @patch("app.controllers.ranking_controller.RankingService")
    def test_visualizar_ranking_reprocessar(
        self, mock_ranking_service_class, client, analise_exemplo
    ):
        """Testa visualização com reprocessamento."""
        # Mock do serviço
        mock_service = Mock()
        mock_service.gerar_ranking_async.return_value = [analise_exemplo]
        mock_ranking_service_class.return_value = mock_service

        # Faz requisição com reprocessar
        response = client.get("/ranking/1?reprocessar=true")

        # Verifica que chamou gerar_ranking_async
        assert response.status_code == 200
        mock_service.gerar_ranking_async.assert_called_once()


class TestGerarRanking:
    """Testes para o endpoint de geração de ranking."""

    @patch("app.controllers.ranking_controller.RankingService")
    def test_gerar_ranking_sucesso(
        self, mock_ranking_service_class, client, analise_exemplo
    ):
        """Testa geração de ranking com sucesso."""
        # Mock do serviço
        mock_service = Mock()
        mock_service.gerar_ranking_async.return_value = [analise_exemplo]
        mock_ranking_service_class.return_value = mock_service

        # Faz requisição POST
        response = client.post("/ranking/1/gerar")

        # Verifica resposta
        assert response.status_code == 200
        data = response.json()

        assert data["vaga_id"] == 1
        assert data["total_candidatos"] == 1
        assert len(data["ranking"]) == 1
        assert data["ranking"][0]["score"] == 85


class TestObterTopCandidatos:
    """Testes para o endpoint de top candidatos."""

    @patch("app.controllers.ranking_controller.RankingService")
    def test_obter_top_candidatos_sucesso(
        self, mock_ranking_service_class, client, analise_exemplo
    ):
        """Testa obtenção de top candidatos."""
        # Mock do serviço
        mock_service = Mock()
        mock_service.obter_top_candidatos.return_value = [analise_exemplo]
        mock_ranking_service_class.return_value = mock_service

        # Faz requisição
        response = client.get("/ranking/1/top/5")

        # Verifica resposta
        assert response.status_code == 200
        data = response.json()

        assert data["vaga_id"] == 1
        assert data["limite"] == 5
        assert data["total_retornado"] == 1
        assert len(data["candidatos"]) == 1
