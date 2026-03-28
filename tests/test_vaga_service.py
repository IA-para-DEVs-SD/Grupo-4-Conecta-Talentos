
import pytest
from app.schemas.vaga_schema import VagaCreateSchema
from app.services.vaga_service import VagaService, VagaNotFoundError


def _dados_vaga(**kwargs):
    defaults = dict(
        titulo="Dev Python Sênior",
        descricao="Desenvolvimento de APIs REST com FastAPI e SQLAlchemy",
        requisitos_tecnicos=["Python", "FastAPI"],
        experiencia_minima="3 anos",
        competencias_desejadas=["Trabalho em equipe"],
    )
    defaults.update(kwargs)
    return VagaCreateSchema(**defaults)


class TestVagaServiceCriar:
    def test_criar_vaga(self, db_session):
        service = VagaService(db_session)
        vaga = service.criar(_dados_vaga())
        assert vaga.id is not None
        assert vaga.titulo == "Dev Python Sênior"

    def test_criar_vaga_persiste(self, db_session):
        service = VagaService(db_session)
        vaga = service.criar(_dados_vaga())
        obtida = service.obter(vaga.id)
        assert obtida.titulo == vaga.titulo


class TestVagaServiceObter:
    def test_obter_inexistente_levanta_erro(self, db_session):
        service = VagaService(db_session)
        with pytest.raises(VagaNotFoundError):
            service.obter(999)


class TestVagaServiceAtualizar:
    def test_atualizar_vaga(self, db_session):
        service = VagaService(db_session)
        vaga = service.criar(_dados_vaga())
        atualizada = service.atualizar(vaga.id, _dados_vaga(titulo="Dev Java Pleno"))
        assert atualizada.titulo == "Dev Java Pleno"

    def test_atualizar_inexistente_levanta_erro(self, db_session):
        service = VagaService(db_session)
        with pytest.raises(VagaNotFoundError):
            service.atualizar(999, _dados_vaga())


class TestVagaServiceDeletar:
    def test_deletar_vaga(self, db_session):
        service = VagaService(db_session)
        vaga = service.criar(_dados_vaga())
        service.deletar(vaga.id)
        with pytest.raises(VagaNotFoundError):
            service.obter(vaga.id)

    def test_deletar_inexistente_levanta_erro(self, db_session):
        service = VagaService(db_session)
        with pytest.raises(VagaNotFoundError):
            service.deletar(999)


class TestVagaServicePaginacao:
    def test_listar_paginado_vazio(self, db_session):
        service = VagaService(db_session)
        vagas, total, total_paginas = service.listar_paginado()
        assert vagas == []
        assert total == 0
        assert total_paginas == 1

    def test_listar_paginado_com_dados(self, db_session):
        service = VagaService(db_session)
        for i in range(15):
            service.criar(_dados_vaga(titulo=f"Vaga {i}"))
        vagas, total, total_paginas = service.listar_paginado(pagina=1, por_pagina=10)
        assert len(vagas) == 10
        assert total == 15
        assert total_paginas == 2

    def test_listar_segunda_pagina(self, db_session):
        service = VagaService(db_session)
        for i in range(15):
            service.criar(_dados_vaga(titulo=f"Vaga {i}"))
        vagas, total, total_paginas = service.listar_paginado(pagina=2, por_pagina=10)
        assert len(vagas) == 5
