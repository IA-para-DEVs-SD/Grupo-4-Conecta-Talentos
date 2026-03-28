
import pytest
from app.services.curriculo_service import (
    validar_pdf,
    ArquivoInvalidoError,
    ArquivoMuitoGrandeError,
    CurriculoService,
    VagaNaoEncontradaError,
)
from app.schemas.vaga_schema import VagaCreateSchema
from app.services.vaga_service import VagaService

PDF_VALIDO = b"%PDF-1.4 fake content for testing purposes"
PDF_INVALIDO = b"Este nao e um PDF"


class TestValidarPdf:
    def test_pdf_valido(self):
        validar_pdf(PDF_VALIDO, "curriculo.pdf")

    def test_extensao_invalida(self):
        with pytest.raises(ArquivoInvalidoError, match="Apenas arquivos PDF"):
            validar_pdf(PDF_VALIDO, "curriculo.docx")

    def test_magic_number_invalido(self):
        with pytest.raises(ArquivoInvalidoError, match="não é um PDF válido"):
            validar_pdf(PDF_INVALIDO, "curriculo.pdf")

    def test_arquivo_vazio(self):
        with pytest.raises(ArquivoInvalidoError, match="está vazio"):
            validar_pdf(b"", "curriculo.pdf")

    def test_arquivo_muito_grande(self):
        grande = b"%PDF" + b"x" * (11 * 1024 * 1024)
        with pytest.raises(ArquivoMuitoGrandeError, match="excede o limite"):
            validar_pdf(grande, "curriculo.pdf", max_size_mb=10)

    def test_extensao_case_insensitive(self):
        validar_pdf(PDF_VALIDO, "Curriculo.PDF")

    def test_extensao_txt_com_conteudo_pdf(self):
        with pytest.raises(ArquivoInvalidoError, match="Apenas arquivos PDF"):
            validar_pdf(PDF_VALIDO, "curriculo.txt")


def _criar_vaga(db_session) -> int:
    service = VagaService(db_session)
    vaga = service.criar(VagaCreateSchema(
        titulo="Dev Python",
        descricao="Desenvolvimento de APIs REST com FastAPI",
        requisitos_tecnicos=["Python"],
        experiencia_minima="3 anos",
        competencias_desejadas=["Comunicação"],
    ))
    return vaga.id


class TestCurriculoServiceUpload:
    def test_upload_vaga_inexistente(self, db_session):
        service = CurriculoService(db_session)
        with pytest.raises(VagaNaoEncontradaError):
            service.upload(999, "cv.pdf", PDF_VALIDO)

    def test_upload_sucesso(self, db_session, tmp_path, monkeypatch):
        monkeypatch.setattr(
            "app.services.curriculo_service.get_settings",
            lambda: type("S", (), {"upload_dir": str(tmp_path), "max_file_size_mb": 10})(),
        )
        vaga_id = _criar_vaga(db_session)
        service = CurriculoService(db_session)
        curriculo = service.upload(vaga_id, "curriculo.pdf", PDF_VALIDO)
        assert curriculo.id is not None
        assert curriculo.nome_arquivo == "curriculo.pdf"
        assert curriculo.vaga_id == vaga_id
        assert curriculo.status == "pendente"

    def test_upload_arquivo_invalido(self, db_session, tmp_path, monkeypatch):
        monkeypatch.setattr(
            "app.services.curriculo_service.get_settings",
            lambda: type("S", (), {"upload_dir": str(tmp_path), "max_file_size_mb": 10})(),
        )
        vaga_id = _criar_vaga(db_session)
        service = CurriculoService(db_session)
        with pytest.raises(ArquivoInvalidoError):
            service.upload(vaga_id, "curriculo.pdf", PDF_INVALIDO)


class TestCurriculoServiceMultiplos:
    def test_upload_multiplos_sucesso(self, db_session, tmp_path, monkeypatch):
        monkeypatch.setattr(
            "app.services.curriculo_service.get_settings",
            lambda: type("S", (), {"upload_dir": str(tmp_path), "max_file_size_mb": 10})(),
        )
        vaga_id = _criar_vaga(db_session)
        service = CurriculoService(db_session)
        arquivos = [
            ("cv1.pdf", PDF_VALIDO),
            ("cv2.pdf", PDF_VALIDO),
        ]
        sucessos, erros = service.upload_multiplos(vaga_id, arquivos)
        assert len(sucessos) == 2
        assert len(erros) == 0

    def test_upload_multiplos_com_erros(self, db_session, tmp_path, monkeypatch):
        monkeypatch.setattr(
            "app.services.curriculo_service.get_settings",
            lambda: type("S", (), {"upload_dir": str(tmp_path), "max_file_size_mb": 10})(),
        )
        vaga_id = _criar_vaga(db_session)
        service = CurriculoService(db_session)
        arquivos = [
            ("cv1.pdf", PDF_VALIDO),
            ("cv2.docx", PDF_VALIDO),  # extensão errada
            ("cv3.pdf", PDF_INVALIDO),  # conteúdo errado
        ]
        sucessos, erros = service.upload_multiplos(vaga_id, arquivos)
        assert len(sucessos) == 1
        assert len(erros) == 2


class TestCurriculoServiceListar:
    def test_listar_vazio(self, db_session):
        vaga_id = _criar_vaga(db_session)
        service = CurriculoService(db_session)
        assert service.listar_por_vaga(vaga_id) == []

    def test_listar_com_curriculos(self, db_session, tmp_path, monkeypatch):
        monkeypatch.setattr(
            "app.services.curriculo_service.get_settings",
            lambda: type("S", (), {"upload_dir": str(tmp_path), "max_file_size_mb": 10})(),
        )
        vaga_id = _criar_vaga(db_session)
        service = CurriculoService(db_session)
        service.upload(vaga_id, "cv1.pdf", PDF_VALIDO)
        service.upload(vaga_id, "cv2.pdf", PDF_VALIDO)
        assert len(service.listar_por_vaga(vaga_id)) == 2
