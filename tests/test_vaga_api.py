
import pytest


VAGA_VALIDA = {
    "titulo": "Dev Python Sênior",
    "descricao": "Desenvolvimento de APIs REST com FastAPI e SQLAlchemy",
    "requisitos_tecnicos": ["Python", "FastAPI"],
    "experiencia_minima": "3 anos",
    "competencias_desejadas": ["Trabalho em equipe"],
}


class TestCriarVagaAPI:
    def test_criar_vaga_sucesso(self, client):
        resp = client.post("/vagas/api", json=VAGA_VALIDA)
        assert resp.status_code == 201
        data = resp.json()
        assert data["titulo"] == "Dev Python Sênior"
        assert data["id"] is not None

    def test_criar_vaga_sem_titulo(self, client):
        dados = {**VAGA_VALIDA, "titulo": ""}
        resp = client.post("/vagas/api", json=dados)
        assert resp.status_code == 422

    def test_criar_vaga_descricao_curta(self, client):
        dados = {**VAGA_VALIDA, "descricao": "Curta"}
        resp = client.post("/vagas/api", json=dados)
        assert resp.status_code == 422

    def test_criar_vaga_requisitos_vazios(self, client):
        dados = {**VAGA_VALIDA, "requisitos_tecnicos": []}
        resp = client.post("/vagas/api", json=dados)
        assert resp.status_code == 422


class TestAtualizarVagaAPI:
    def test_atualizar_vaga_sucesso(self, client):
        resp = client.post("/vagas/api", json=VAGA_VALIDA)
        vaga_id = resp.json()["id"]
        dados_atualizados = {**VAGA_VALIDA, "titulo": "Dev Java Pleno"}
        resp = client.put(f"/vagas/api/{vaga_id}", json=dados_atualizados)
        assert resp.status_code == 200
        assert resp.json()["titulo"] == "Dev Java Pleno"

    def test_atualizar_vaga_404(self, client):
        resp = client.put("/vagas/api/999", json=VAGA_VALIDA)
        assert resp.status_code == 404

    def test_atualizar_vaga_validacao(self, client):
        resp = client.post("/vagas/api", json=VAGA_VALIDA)
        vaga_id = resp.json()["id"]
        dados = {**VAGA_VALIDA, "titulo": ""}
        resp = client.put(f"/vagas/api/{vaga_id}", json=dados)
        assert resp.status_code == 422


class TestListarVagasAPI:
    def test_listar_vazio(self, client):
        resp = client.get("/vagas/api")
        assert resp.status_code == 200
        data = resp.json()
        assert data["vagas"] == []
        assert data["total"] == 0

    def test_listar_com_paginacao(self, client):
        for i in range(12):
            client.post("/vagas/api", json={**VAGA_VALIDA, "titulo": f"Vaga {i}"})
        resp = client.get("/vagas/api?pagina=1&por_pagina=5")
        data = resp.json()
        assert len(data["vagas"]) == 5
        assert data["total"] == 12
        assert data["total_paginas"] == 3
        assert data["pagina"] == 1

    def test_listar_segunda_pagina(self, client):
        for i in range(12):
            client.post("/vagas/api", json={**VAGA_VALIDA, "titulo": f"Vaga {i}"})
        resp = client.get("/vagas/api?pagina=3&por_pagina=5")
        data = resp.json()
        assert len(data["vagas"]) == 2


class TestObterVagaAPI:
    def test_obter_vaga_sucesso(self, client):
        resp = client.post("/vagas/api", json=VAGA_VALIDA)
        vaga_id = resp.json()["id"]
        resp = client.get(f"/vagas/api/{vaga_id}")
        assert resp.status_code == 200
        assert resp.json()["titulo"] == "Dev Python Sênior"

    def test_obter_vaga_404(self, client):
        resp = client.get("/vagas/api/999")
        assert resp.status_code == 404


class TestDeletarVagaAPI:
    def test_deletar_vaga_sucesso(self, client):
        resp = client.post("/vagas/api", json=VAGA_VALIDA)
        vaga_id = resp.json()["id"]
        resp = client.delete(f"/vagas/api/{vaga_id}")
        assert resp.status_code == 204
        resp = client.get(f"/vagas/api/{vaga_id}")
        assert resp.status_code == 404

    def test_deletar_vaga_404(self, client):
        resp = client.delete("/vagas/api/999")
        assert resp.status_code == 404


class TestPaginasHTML:
    def test_pagina_lista_vagas(self, client):
        resp = client.get("/vagas")
        assert resp.status_code == 200
        assert "Vagas" in resp.text

    def test_pagina_criar_vaga(self, client):
        resp = client.get("/vagas/criar")
        assert resp.status_code == 200
        assert "Nova Vaga" in resp.text

    def test_criar_vaga_via_form(self, client):
        resp = client.post("/vagas/criar", data={
            "titulo": "Dev Python Sênior",
            "descricao": "Desenvolvimento de APIs REST com FastAPI e SQLAlchemy",
            "requisitos_tecnicos": "Python, FastAPI",
            "experiencia_minima": "3 anos",
            "competencias_desejadas": "Trabalho em equipe, Comunicação",
        }, follow_redirects=False)
        assert resp.status_code == 303

    def test_criar_vaga_form_invalido(self, client):
        resp = client.post("/vagas/criar", data={
            "titulo": "",
            "descricao": "",
            "requisitos_tecnicos": "",
            "experiencia_minima": "",
            "competencias_desejadas": "",
        })
        assert resp.status_code == 200
        assert "alert-danger" in resp.text

    def test_detalhes_vaga_html(self, client):
        resp = client.post("/vagas/api", json=VAGA_VALIDA)
        vaga_id = resp.json()["id"]
        resp = client.get(f"/vagas/{vaga_id}")
        assert resp.status_code == 200
        assert "Dev Python Sênior" in resp.text

    def test_detalhes_vaga_404_html(self, client):
        resp = client.get("/vagas/999")
        assert resp.status_code == 404
