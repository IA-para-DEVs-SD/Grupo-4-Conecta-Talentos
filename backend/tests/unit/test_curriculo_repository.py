import pytest
from app.repositories.vaga_repository import VagaRepository
from app.repositories.curriculo_repository import CurriculoRepository
from app.models.domain import VagaCreate, Curriculo


def criar_vaga(db):
    return VagaRepository(db).criar(VagaCreate(
        titulo="Dev Python",
        descricao="Descrição",
        requisitos_tecnicos=["Python"],
        experiencia_minima="1 ano",
        competencias_desejadas=["Comunicação"],
    ))


def test_criar_curriculo(db):
    vaga = criar_vaga(db)
    repo = CurriculoRepository(db)
    curriculo = repo.criar(vaga.id, "cv.pdf", "/uploads/cv.pdf")
    assert curriculo.id is not None
    assert curriculo.status == "pendente"
    assert curriculo.vaga_id == vaga.id


def test_listar_por_vaga(db):
    vaga = criar_vaga(db)
    repo = CurriculoRepository(db)
    repo.criar(vaga.id, "cv1.pdf", "/uploads/cv1.pdf")
    repo.criar(vaga.id, "cv2.pdf", "/uploads/cv2.pdf")
    curriculos = repo.listar_por_vaga(vaga.id)
    assert len(curriculos) == 2


def test_atualizar_curriculo(db):
    vaga = criar_vaga(db)
    repo = CurriculoRepository(db)
    curriculo = repo.criar(vaga.id, "cv.pdf", "/uploads/cv.pdf")
    curriculo.status = "extraido"
    curriculo.texto_extraido = "Texto do currículo"
    atualizado = repo.atualizar(curriculo)
    assert atualizado.status == "extraido"
    assert atualizado.texto_extraido == "Texto do currículo"


def test_deletar_curriculo(db):
    vaga = criar_vaga(db)
    repo = CurriculoRepository(db)
    curriculo = repo.criar(vaga.id, "cv.pdf", "/uploads/cv_inexistente.pdf")
    assert repo.deletar(curriculo.id) is True
    assert repo.obter(curriculo.id) is None
