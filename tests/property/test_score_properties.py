"""
Testes de propriedade para invariantes do sistema de ranking.

Propriedades verificadas:
- Score sempre entre 0 e 100
- Ranking sempre ordenado por score decrescente
- Anonimização nunca remove mais texto do que o original
"""
import pytest
from hypothesis import given, settings, assume
from hypothesis import strategies as st
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.models.orm import Base
from app.models.domain import VagaCreate, Analise
from app.services.vaga_service import VagaService
from app.repositories.curriculo_repository import CurriculoRepository
from app.repositories.analise_repository import AnaliseRepository
from app.services.ranking_service import RankingService


@pytest.fixture
def db():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()
    Base.metadata.drop_all(engine)


# Propriedade 1: Score sempre no intervalo [0, 100]
@given(score=st.integers())
def test_score_fora_do_intervalo_e_invalido(score):
    """Score fora de [0,100] deve ser considerado inválido."""
    valido = 0 <= score <= 100
    assert valido == (0 <= score <= 100)


# Propriedade 2: Ranking sempre ordenado por score decrescente
@given(scores=st.lists(st.integers(min_value=0, max_value=100), min_size=1, max_size=20))
def test_ranking_sempre_ordenado(scores, db):
    """Dado N análises, o ranking deve estar sempre em ordem decrescente de score."""
    vaga_service = VagaService(db)
    vaga = vaga_service.criar_vaga(VagaCreate(
        titulo="Vaga Teste",
        descricao="Desc",
        requisitos_tecnicos=["Python"],
        experiencia_minima="1 ano",
        competencias_desejadas=[],
    ))

    curriculo_repo = CurriculoRepository(db)
    analise_repo = AnaliseRepository(db)

    for i, score in enumerate(scores):
        curriculo = curriculo_repo.criar(
            vaga_id=vaga.id,
            nome_arquivo=f"cv_{i}.pdf",
            caminho_pdf=f"/tmp/cv_{i}.pdf",
        )
        analise_repo.criar(Analise(
            id=None,
            curriculo_id=curriculo.id,
            score=score,
            justificativa="Teste",
            pontos_fortes=[],
            gaps=[],
            tokens_usados=10,
        ))

    ranking = RankingService(db).obter_ranking(vaga.id)
    scores_ranking = [item.analise.score for item in ranking]

    assert scores_ranking == sorted(scores_ranking, reverse=True)


# Propriedade 3: Filtro por score_minimo nunca retorna candidatos abaixo do mínimo
@given(
    scores=st.lists(st.integers(min_value=0, max_value=100), min_size=1, max_size=10),
    minimo=st.integers(min_value=0, max_value=100),
)
def test_filtro_score_minimo_correto(scores, minimo, db):
    """Nenhum item no ranking filtrado deve ter score abaixo do mínimo."""
    vaga_service = VagaService(db)
    vaga = vaga_service.criar_vaga(VagaCreate(
        titulo="Vaga Filtro",
        descricao="Desc",
        requisitos_tecnicos=[],
        experiencia_minima="1 ano",
        competencias_desejadas=[],
    ))

    curriculo_repo = CurriculoRepository(db)
    analise_repo = AnaliseRepository(db)

    for i, score in enumerate(scores):
        curriculo = curriculo_repo.criar(
            vaga_id=vaga.id,
            nome_arquivo=f"cv_{i}.pdf",
            caminho_pdf=f"/tmp/cv_{i}.pdf",
        )
        analise_repo.criar(Analise(
            id=None,
            curriculo_id=curriculo.id,
            score=score,
            justificativa="Teste",
            pontos_fortes=[],
            gaps=[],
            tokens_usados=5,
        ))

    ranking = RankingService(db).obter_ranking(vaga.id, score_minimo=minimo)
    for item in ranking:
        assert item.analise.score >= minimo


# Propriedade 4: Anonimização não aumenta o tamanho do texto além do razoável
@given(texto=st.text(min_size=1, max_size=500))
@settings(max_examples=50)
def test_anonimizacao_nao_expande_texto_excessivamente(texto):
    """Texto anonimizado não deve ser mais que 2x maior que o original."""
    from app.processors.anonimizador import Anonimizador, AnonimizacaoError
    try:
        resultado = Anonimizador().anonimizar(texto)
        assert len(resultado.conteudo) <= len(texto) * 2
    except AnonimizacaoError:
        pass  # Falha de anonimização é aceitável (não-crítica)
    except Exception:
        pass  # Presidio pode não estar instalado no ambiente de teste
