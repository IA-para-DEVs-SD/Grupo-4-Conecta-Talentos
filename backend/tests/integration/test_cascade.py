"""Testes de integração para exclusão em cascata: vaga → currículos → análises → PDFs."""
import os
import tempfile
import pytest
from app.repositories.vaga_repository import VagaRepository
from app.repositories.curriculo_repository import CurriculoRepository
from app.repositories.analise_repository import AnaliseRepository
from app.models.domain import VagaCreate, Analise
from app.models.orm import CurriculoORM, AnaliseORM


def test_cascade_delete_vaga_remove_curriculos_e_analises(db):
    """Deletar vaga deve remover currículos e análises em cascata."""
    vaga = VagaRepository(db).criar(VagaCreate(
        titulo="Dev", descricao="Desc",
        requisitos_tecnicos=["Python"], experiencia_minima="1 ano",
        competencias_desejadas=["Comunicação"],
    ))

    curriculo_repo = CurriculoRepository(db)
    curriculo = curriculo_repo.criar(vaga.id, "cv.pdf", "/tmp/cv.pdf")

    analise_repo = AnaliseRepository(db)
    analise_repo.criar(Analise(
        id=None, curriculo_id=curriculo.id, score=80,
        justificativa="Bom candidato", pontos_fortes=["Python"],
        gaps=["Docker"], tokens_usados=100,
    ))

    # Confirma que existem antes de deletar
    assert len(curriculo_repo.listar_por_vaga(vaga.id)) == 1
    assert analise_repo.obter_por_curriculo(curriculo.id) is not None

    # Deleta a vaga
    VagaRepository(db).deletar(vaga.id)

    # Tudo deve ter sido removido em cascata
    assert curriculo_repo.listar_por_vaga(vaga.id) == []
    assert analise_repo.obter_por_curriculo(curriculo.id) is None


def test_cascade_delete_curriculo_remove_pdf_do_disco(db):
    """Deletar currículo deve remover o arquivo PDF do disco."""
    vaga = VagaRepository(db).criar(VagaCreate(
        titulo="Dev", descricao="Desc",
        requisitos_tecnicos=["Python"], experiencia_minima="1 ano",
        competencias_desejadas=["Comunicação"],
    ))

    # Cria arquivo temporário simulando PDF
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
        caminho_pdf = f.name

    assert os.path.exists(caminho_pdf)

    curriculo_repo = CurriculoRepository(db)
    curriculo = curriculo_repo.criar(vaga.id, "cv.pdf", caminho_pdf)

    curriculo_repo.deletar(curriculo.id)

    assert not os.path.exists(caminho_pdf)


def test_cascade_delete_vaga_remove_pdfs_do_disco(db):
    """Deletar vaga deve remover todos os PDFs dos currículos do disco."""
    vaga = VagaRepository(db).criar(VagaCreate(
        titulo="Dev", descricao="Desc",
        requisitos_tecnicos=["Python"], experiencia_minima="1 ano",
        competencias_desejadas=["Comunicação"],
    ))

    curriculo_repo = CurriculoRepository(db)

    # Cria dois arquivos temporários
    arquivos = []
    for i in range(2):
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
            arquivos.append(f.name)
        curriculo_repo.criar(vaga.id, f"cv{i}.pdf", arquivos[-1])

    for arq in arquivos:
        assert os.path.exists(arq)

    VagaRepository(db).deletar(vaga.id)

    for arq in arquivos:
        assert not os.path.exists(arq)
