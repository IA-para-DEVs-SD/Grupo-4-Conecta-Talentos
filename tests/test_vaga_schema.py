
import pytest
from pydantic import ValidationError
from app.schemas.vaga_schema import VagaCreateSchema


class TestVagaCreateSchema:

    def test_schema_valido(self):
        schema = VagaCreateSchema(
            titulo="Dev Python Sênior",
            descricao="Desenvolvimento de APIs REST com FastAPI",
            requisitos_tecnicos=["Python", "FastAPI"],
            experiencia_minima="3 anos",
            competencias_desejadas=["Trabalho em equipe"],
        )
        assert schema.titulo == "Dev Python Sênior"
        assert len(schema.requisitos_tecnicos) == 2

    def test_titulo_vazio_falha(self):
        with pytest.raises(ValidationError):
            VagaCreateSchema(
                titulo="",
                descricao="Descrição válida com mais de 10 chars",
                requisitos_tecnicos=["Python"],
                experiencia_minima="1 ano",
                competencias_desejadas=["Comunicação"],
            )

    def test_titulo_curto_falha(self):
        with pytest.raises(ValidationError):
            VagaCreateSchema(
                titulo="AB",
                descricao="Descrição válida com mais de 10 chars",
                requisitos_tecnicos=["Python"],
                experiencia_minima="1 ano",
                competencias_desejadas=["Comunicação"],
            )

    def test_descricao_curta_falha(self):
        with pytest.raises(ValidationError):
            VagaCreateSchema(
                titulo="Dev Python",
                descricao="Curta",
                requisitos_tecnicos=["Python"],
                experiencia_minima="1 ano",
                competencias_desejadas=["Comunicação"],
            )

    def test_requisitos_vazios_falha(self):
        with pytest.raises(ValidationError):
            VagaCreateSchema(
                titulo="Dev Python",
                descricao="Descrição válida com mais de 10 chars",
                requisitos_tecnicos=[],
                experiencia_minima="1 ano",
                competencias_desejadas=["Comunicação"],
            )

    def test_requisitos_so_espacos_falha(self):
        with pytest.raises(ValidationError):
            VagaCreateSchema(
                titulo="Dev Python",
                descricao="Descrição válida com mais de 10 chars",
                requisitos_tecnicos=["  ", ""],
                experiencia_minima="1 ano",
                competencias_desejadas=["Comunicação"],
            )

    def test_competencias_vazias_falha(self):
        with pytest.raises(ValidationError):
            VagaCreateSchema(
                titulo="Dev Python",
                descricao="Descrição válida com mais de 10 chars",
                requisitos_tecnicos=["Python"],
                experiencia_minima="1 ano",
                competencias_desejadas=[],
            )

    def test_experiencia_vazia_falha(self):
        with pytest.raises(ValidationError):
            VagaCreateSchema(
                titulo="Dev Python",
                descricao="Descrição válida com mais de 10 chars",
                requisitos_tecnicos=["Python"],
                experiencia_minima="",
                competencias_desejadas=["Comunicação"],
            )

    def test_strip_em_campos_texto(self):
        schema = VagaCreateSchema(
            titulo="  Dev Python  ",
            descricao="  Descrição válida com mais de 10 chars  ",
            requisitos_tecnicos=["  Python  ", "  FastAPI  "],
            experiencia_minima="  3 anos  ",
            competencias_desejadas=["  Comunicação  "],
        )
        assert schema.titulo == "Dev Python"
        assert schema.experiencia_minima == "3 anos"
        assert schema.requisitos_tecnicos == ["Python", "FastAPI"]
        assert schema.competencias_desejadas == ["Comunicação"]
