"""Testes de integração: ExtratorPDF integrado ao pipeline de upload de currículos."""

from unittest.mock import MagicMock, patch

import pytest

from app.models.domain import VagaCreate
from app.repositories.curriculo_repository import CurriculoRepository
from app.repositories.vaga_repository import VagaRepository
from app.services.curriculo_service import CurriculoService

# Conteúdo mínimo de PDF válido para testes
PDF_BYTES = b"%PDF-1.4 fake content"


def _criar_vaga(db_session) -> int:
    return VagaRepository(db_session).criar(
        VagaCreate(
            titulo="Dev Python",
            descricao="Vaga de teste",
            requisitos_tecnicos=["Python"],
            experiencia_minima="1 ano",
            competencias_desejadas=["Comunicação"],
        )
    ).id


# ---------------------------------------------------------------------------
# Testes unitários do serviço (mock do ExtratorPDF)
# ---------------------------------------------------------------------------


class TestUploadComExtracao:
    def test_upload_extrai_texto_e_persiste(self, db_session, tmp_path):
        """Após upload, texto_extraido deve ser preenchido e status = 'extraido'."""
        vaga_id = _criar_vaga(db_session)
        service = CurriculoService(db_session)
        service.settings.upload_dir = str(tmp_path)

        texto_esperado = "Experiência em Python e FastAPI"

        with patch("app.services.curriculo_service.extrair_texto_pdf") as mock_extrai:
            mock_extrai.return_value = MagicMock(conteudo=texto_esperado)
            curriculo = service.upload(vaga_id, "cv.pdf", PDF_BYTES)

        assert curriculo.texto_extraido == texto_esperado
        assert curriculo.status == "extraido"

    def test_upload_erro_extracao_nao_interrompe_fluxo(self, db_session, tmp_path):
        """Falha na extração deve marcar status como 'erro_extracao', sem lançar exceção."""
        from backend.src.services.extrator_pdf import PDFCorromidoError

        vaga_id = _criar_vaga(db_session)
        service = CurriculoService(db_session)
        service.settings.upload_dir = str(tmp_path)

        with patch("app.services.curriculo_service.extrair_texto_pdf") as mock_extrai:
            mock_extrai.side_effect = PDFCorromidoError("PDF corrompido")
            curriculo = service.upload(vaga_id, "cv.pdf", PDF_BYTES)

        assert curriculo.texto_extraido is None
        assert curriculo.status == "erro_extracao"

    def test_upload_multiplos_extrai_todos(self, db_session, tmp_path):
        """upload_multiplos deve extrair texto de cada arquivo com sucesso."""
        vaga_id = _criar_vaga(db_session)
        service = CurriculoService(db_session)
        service.settings.upload_dir = str(tmp_path)

        arquivos = [("cv1.pdf", PDF_BYTES), ("cv2.pdf", PDF_BYTES)]

        with patch("app.services.curriculo_service.extrair_texto_pdf") as mock_extrai:
            mock_extrai.return_value = MagicMock(conteudo="Texto extraído")
            sucessos, erros = service.upload_multiplos(vaga_id, arquivos)

        assert len(sucessos) == 2
        assert len(erros) == 0
        assert all(c.status == "extraido" for c in sucessos)
        assert all(c.texto_extraido == "Texto extraído" for c in sucessos)

    def test_upload_multiplos_erro_parcial(self, db_session, tmp_path):
        """Erro em um arquivo não deve impedir o processamento dos demais."""
        from backend.src.services.extrator_pdf import PDFMuitoGrandeError

        vaga_id = _criar_vaga(db_session)
        service = CurriculoService(db_session)
        service.settings.upload_dir = str(tmp_path)

        arquivos = [("cv1.pdf", PDF_BYTES), ("cv2.pdf", PDF_BYTES)]

        with patch("app.services.curriculo_service.extrair_texto_pdf") as mock_extrai:
            mock_extrai.side_effect = [
                MagicMock(conteudo="Texto ok"),
                PDFMuitoGrandeError("Muitas páginas"),
            ]
            sucessos, erros = service.upload_multiplos(vaga_id, arquivos)

        assert len(sucessos) == 2
        assert sucessos[0].status == "extraido"
        assert sucessos[1].status == "erro_extracao"

    def test_texto_extraido_persistido_no_banco(self, db_session, tmp_path):
        """Texto extraído deve ser recuperável via repositório após upload."""
        vaga_id = _criar_vaga(db_session)
        service = CurriculoService(db_session)
        service.settings.upload_dir = str(tmp_path)

        with patch("app.services.curriculo_service.extrair_texto_pdf") as mock_extrai:
            mock_extrai.return_value = MagicMock(conteudo="Conteúdo persistido")
            curriculo = service.upload(vaga_id, "cv.pdf", PDF_BYTES)

        repo = CurriculoRepository(db_session)
        salvo = repo.obter(curriculo.id)
        assert salvo.texto_extraido == "Conteúdo persistido"
        assert salvo.status == "extraido"


# ---------------------------------------------------------------------------
# Teste de integração real com PDF em disco (requer pymupdf)
# ---------------------------------------------------------------------------


class TestExtracaoRealPDF:
    def test_extracao_pdf_real(self, db_session, tmp_path):
        """Cria um PDF real com pymupdf e verifica extração end-to-end."""
        pymupdf = pytest.importorskip("pymupdf")

        # Cria PDF real com texto
        pdf_path = tmp_path / "curriculo_real.pdf"
        doc = pymupdf.open()
        page = doc.new_page()
        page.insert_text((72, 72), "Desenvolvedor Python com 5 anos de experiência.")
        doc.save(str(pdf_path))
        doc.close()

        vaga_id = _criar_vaga(db_session)
        service = CurriculoService(db_session)
        service.settings.upload_dir = str(tmp_path / "uploads")

        curriculo = service.upload(vaga_id, "curriculo_real.pdf", pdf_path.read_bytes())

        assert curriculo.status == "extraido"
        assert curriculo.texto_extraido is not None
        assert "Python" in curriculo.texto_extraido
