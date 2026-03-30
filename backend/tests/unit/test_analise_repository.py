"""Testes unitários para AnaliseRepository."""
import pytest
from app.repositories.vaga_repository import VagaRepository
from app.repositories.curriculo_repository import CurriculoRepository
from app.repositories.analise_repository import AnaliseRepository
from app.models.domain import VagaCreate, Analise


def setup_curriculo(db):
    vaga = VagaRepository(db).criar(VagaCreate(
        titulo="Dev Python",
        descricao="Descrição",
        requisitos_tecnicos=["Python"],
        experiencia_minima="1 ano",
        competencias_desejadas=["Comunicação"],
    ))
    return CurriculoRepository(db).criar(vaga.id, "cv.pdf", "/uploads/cv.pdf")


def make_analise(curriculo_id: int) -> Analise:
    return Analise(
        id=None,
        curriculo_id=curriculo_id,
        score=85,
        justificativa="Candidato com boa aderência técnica.",
        pontos_fortes=["Python", "FastAPI"],
        gaps=["Docker"],
        tokens_usados=150,
    )


def test_criar_analise(db):
    curriculo = setup_curriculo(db)
    repo = AnaliseRepository(db)
    analise = repo.criar(make_analise(curriculo.id))
    assert analise.id is not None
    assert analise.score == 85
    assert "Python" in analise.pontos_fortes
    assert "Docker" in analise.gaps


def test_obter_por_curriculo(db):
    curriculo = setup_curriculo(db)
    repo = AnaliseRepository(db)
    repo.criar(make_analise(curriculo.id))
    analise = repo.obter_por_curriculo(curriculo.id)
    assert analise is not None
    assert analise.curriculo_id == curriculo.id


def test_obter_por_curriculo_inexistente(db):
    repo = AnaliseRepository(db)
    assert repo.obter_por_curriculo(999) is None


def test_listar_por_vaga_ordenado_por_score(db):
    vaga = VagaRepository(db).criar(VagaCreate(
        titulo="Dev", descricao="Desc",
        requisitos_tecnicos=["Python"], experiencia_minima="1 ano",
        competencias_desejadas=["Comunicação"],
    ))
    curriculo_repo = CurriculoRepository(db)
    analise_repo = AnaliseRepository(db)

    for score, nome in [(60, "cv1.pdf"), (90, "cv2.pdf"), (75, "cv3.pdf")]:
        c = curriculo_repo.criar(vaga.id, nome, f"/uploads/{nome}")
        analise_repo.criar(Analise(
            id=None, curriculo_id=c.id, score=score,
            justificativa="Avaliação", pontos_fortes=[], gaps=[], tokens_usados=100,
        ))

    ranking = analise_repo.listar_por_vaga(vaga.id)
    assert len(ranking) == 3
    assert ranking[0].score == 90
    assert ranking[1].score == 75
    assert ranking[2].score == 60
