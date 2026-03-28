"""Testes unitários para VagaService."""
import pytest
from app.models.domain import VagaCreate
from app.services.vaga_service import VagaService, VagaNotFoundError


def test_criar_vaga(db_session):
    service = VagaService(db_session)
    data = VagaCreate(
        titulo="Dev Python",
        descricao="Vaga para desenvolvedor Python",
        requisitos_tecnicos=["Python", "FastAPI"],
        experiencia_minima="2 anos",
        competencias_desejadas=["Trabalho em equipe"],
    )
    vaga = service.criar_vaga(data)
    assert vaga.id is not None
    assert vaga.titulo == "Dev Python"
    assert "Python" in vaga.requisitos_tecnicos


def test_listar_vagas_vazio(db_session):
    vagas = VagaService(db_session).listar_vagas()
    assert vagas == []


def test_obter_vaga_inexistente(db_session):
    with pytest.raises(VagaNotFoundError):
        VagaService(db_session).obter_vaga(999)


def test_deletar_vaga(db_session):
    service = VagaService(db_session)
    vaga = service.criar_vaga(VagaCreate(
        titulo="Temp", descricao="Desc", requisitos_tecnicos=[],
        experiencia_minima="1 ano", competencias_desejadas=[],
    ))
    service.deletar_vaga(vaga.id)
    with pytest.raises(VagaNotFoundError):
        service.obter_vaga(vaga.id)
