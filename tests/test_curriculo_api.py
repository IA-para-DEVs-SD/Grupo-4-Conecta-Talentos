
import io
import pytest

PDF_VALIDO = b"%PDF-1.4 fake content for testing purposes"
PDF_INVALIDO = b"Este nao e um PDF"

VAGA_VALIDA = {
    "titulo": "Dev Python Sênior",
    "descricao": "Desenvolvimento de APIs REST com FastAPI e SQLAlchemy",
    "requisitos_tecnicos": ["Python", "FastAPI"],
    "experiencia_minima": "3 anos",
    "competencias_desejadas": ["Trabalho em equipe"],
}


def _criar_vaga(client) -> int:
    resp = client.post("/vagas/api", json=VAGA_VALIDA)
    return resp.json()["id"]


class TestUploadCurriculoAPI:
    def test_upload_sucesso(self, client, tmp_path, monkeypatch):
        monkeypatch.setattr(
            "app.services.curriculo_service.get_settings",
            lambda: type("S", (), {"upload_dir": str(tmp_path), "max_file_size_mb": 10})(),
        )
        vaga_id = _criar_vaga(client)
        resp = client.post(
            f"/curriculos/api/{vaga_id}",
            files=[("arquivos", ("cv.pdf", io.BytesIO(PDF_VALIDO), "application/pdf"))],
        )
        assert resp.status_code == 201
        data = resp.json()
        assert data["enviados"] == 1
        assert len(data["erros"]) == 0

    def test_upload_multiplos(self, client, tmp_path, monkeypatch):
        monkeypatch.setattr(
            "app.services.curriculo_service.get_settings",
            lambda: type("S", (), {"upload_dir": str(tmp_path), "max_file_size_mb": 10})(),
        )
        vaga_id = _criar_vaga(client)
        resp = client.post(
            f"/curriculos/api/{vaga_id}",
            files=[
                ("arquivos", ("cv1.pdf", io.BytesIO(PDF_VALIDO), "application/pdf")),
                ("arquivos", ("cv2.pdf", io.BytesIO(PDF_VALIDO), "application/pdf")),
            ],
        )
        assert resp.status_code == 201
        assert resp.json()["enviados"] == 2

    def test_upload_arquivo_invalido(self, client, tmp_path, monkeypatch):
        monkeypatch.setattr(
            "app.services.curriculo_service.get_settings",
            lambda: type("S", (), {"upload_dir": str(tmp_path), "max_file_size_mb": 10})(),
        )
        vaga_id = _criar_vaga(client)
        resp = client.post(
            f"/curriculos/api/{vaga_id}",
            files=[("arquivos", ("cv.pdf", io.BytesIO(PDF_INVALIDO), "application/pdf"))],
        )
        assert resp.status_code == 400
        assert len(resp.json()["erros"]) == 1

    def test_upload_extensao_invalida(self, client, tmp_path, monkeypatch):
        monkeypatch.setattr(
            "app.services.curriculo_service.get_settings",
            lambda: type("S", (), {"upload_dir": str(tmp_path), "max_file_size_mb": 10})(),
        )
        vaga_id = _criar_vaga(client)
        resp = client.post(
            f"/curriculos/api/{vaga_id}",
            files=[("arquivos", ("cv.docx", io.BytesIO(PDF_VALIDO), "application/pdf"))],
        )
        assert resp.status_code == 400
        assert "Apenas arquivos PDF" in resp.json()["erros"][0]

    def test_upload_vaga_inexistente(self, client, tmp_path, monkeypatch):
        monkeypatch.setattr(
            "app.services.curriculo_service.get_settings",
            lambda: type("S", (), {"upload_dir": str(tmp_path), "max_file_size_mb": 10})(),
        )
        resp = client.post(
            "/curriculos/api/999",
            files=[("arquivos", ("cv.pdf", io.BytesIO(PDF_VALIDO), "application/pdf"))],
        )
        assert resp.status_code == 404

    def test_upload_misto_sucesso_e_erro(self, client, tmp_path, monkeypatch):
        monkeypatch.setattr(
            "app.services.curriculo_service.get_settings",
            lambda: type("S", (), {"upload_dir": str(tmp_path), "max_file_size_mb": 10})(),
        )
        vaga_id = _criar_vaga(client)
        resp = client.post(
            f"/curriculos/api/{vaga_id}",
            files=[
                ("arquivos", ("cv1.pdf", io.BytesIO(PDF_VALIDO), "application/pdf")),
                ("arquivos", ("cv2.docx", io.BytesIO(PDF_VALIDO), "application/pdf")),
            ],
        )
        data = resp.json()
        assert data["enviados"] == 1
        assert len(data["erros"]) == 1


class TestListarCurriculosAPI:
    def test_listar_vazio(self, client):
        vaga_id = _criar_vaga(client)
        resp = client.get(f"/curriculos/api/{vaga_id}")
        assert resp.status_code == 200
        assert resp.json()["total"] == 0

    def test_listar_com_curriculos(self, client, tmp_path, monkeypatch):
        monkeypatch.setattr(
            "app.services.curriculo_service.get_settings",
            lambda: type("S", (), {"upload_dir": str(tmp_path), "max_file_size_mb": 10})(),
        )
        vaga_id = _criar_vaga(client)
        client.post(
            f"/curriculos/api/{vaga_id}",
            files=[
                ("arquivos", ("cv1.pdf", io.BytesIO(PDF_VALIDO), "application/pdf")),
                ("arquivos", ("cv2.pdf", io.BytesIO(PDF_VALIDO), "application/pdf")),
            ],
        )
        resp = client.get(f"/curriculos/api/{vaga_id}")
        assert resp.json()["total"] == 2


class TestDeletarCurriculoAPI:
    def test_deletar_sucesso(self, client, tmp_path, monkeypatch):
        monkeypatch.setattr(
            "app.services.curriculo_service.get_settings",
            lambda: type("S", (), {"upload_dir": str(tmp_path), "max_file_size_mb": 10})(),
        )
        vaga_id = _criar_vaga(client)
        resp = client.post(
            f"/curriculos/api/{vaga_id}",
            files=[("arquivos", ("cv.pdf", io.BytesIO(PDF_VALIDO), "application/pdf"))],
        )
        curriculo_id = resp.json()["curriculos"][0]["id"]
        resp = client.delete(f"/curriculos/api/{curriculo_id}")
        assert resp.status_code == 204

    def test_deletar_inexistente(self, client):
        resp = client.delete("/curriculos/api/999")
        assert resp.status_code == 404


class TestPaginasHTMLCurriculo:
    def test_pagina_upload(self, client):
        vaga_id = _criar_vaga(client)
        resp = client.get(f"/curriculos/upload/{vaga_id}")
        assert resp.status_code == 200
        assert "Enviar" in resp.text

    def test_pagina_upload_vaga_inexistente(self, client):
        resp = client.get("/curriculos/upload/999", follow_redirects=False)
        assert resp.status_code == 303
