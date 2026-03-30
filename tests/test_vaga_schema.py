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

    def test_titulo_invalido_falha(self):
        """Testa título vazio e muito curto."""
        with pytest.raises(ValidationError):
            VagaCreateSchema(
                titulo="",
                descricao="Descrição válida com mais de 10 chars",
                requisitos_tecnicos=["Python"],
                experiencia_minima="1 ano",
                competencias_desejadas=["Comunicação"],
            )
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

    def test_requisitos_invalidos_falha(self):
        """Testa requisitos vazios e com apenas espaços."""
        with pytest.raises(ValidationError):
            VagaCreateSchema(
                titulo="Dev Python",
                descricao="Descrição válida com mais de 10 chars",
                requisitos_tecnicos=[],
                experiencia_minima="1 ano",
                competencias_desejadas=["Comunicação"],
            )
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
