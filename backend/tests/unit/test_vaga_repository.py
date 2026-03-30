import pytest
from app.repositories.vaga_repository import VagaRepository
from app.models.domain import VagaCreate


def make_vaga():
    return VagaCreate(
        titulo="Dev Python",
        descricao="Vaga para desenvolvedor Python",
        requisitos_tecnicos=["Python", "FastAPI"],
        experiencia_minima="2 anos",
        competencias_desejadas=["Trabalho em equipe"],
    )


def test_criar_vaga(db):
    repo = VagaRepository(db)
    vaga = repo.criar(make_vaga())
    assert vaga.id is not None
    assert vaga.titulo == "Dev Python"
    assert "Python" in vaga.requisitos_tecnicos


def test_listar_vagas(db):
    repo = VagaRepository(db)
    repo.criar(make_vaga())
    repo.criar(make_vaga())
    vagas = repo.listar()
    assert len(vagas) == 2


def test_obter_vaga(db):
    repo = VagaRepository(db)
    criada = repo.criar(make_vaga())
    obtida = repo.obter(criada.id)
    assert obtida.id == criada.id
    assert obtida.titulo == criada.titulo


def test_obter_vaga_inexistente(db):
    repo = VagaRepository(db)
    assert repo.obter(999) is None


def test_atualizar_vaga(db):
    repo = VagaRepository(db)
    criada = repo.criar(make_vaga())
    dados = make_vaga()
    dados.titulo = "Dev Sênior"
    atualizada = repo.atualizar(criada.id, dados)
    assert atualizada.titulo == "Dev Sênior"


def test_deletar_vaga(db):
    repo = VagaRepository(db)
    criada = repo.criar(make_vaga())
    assert repo.deletar(criada.id) is True
    assert repo.obter(criada.id) is None


def test_deletar_vaga_inexistente(db):
    repo = VagaRepository(db)
    assert repo.deletar(999) is False
