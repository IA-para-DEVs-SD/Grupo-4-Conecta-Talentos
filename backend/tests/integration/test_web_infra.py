"""Testes de integração para infraestrutura web FastAPI."""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_home_retorna_200():
    response = client.get("/")
    assert response.status_code == 200
    assert "ConectaTalentos" in response.text


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_swagger_docs_disponivel():
    response = client.get("/docs")
    assert response.status_code == 200


def test_redoc_disponivel():
    response = client.get("/redoc")
    assert response.status_code == 200


def test_cors_middleware_configurado():
    """Verifica que o middleware CORS está presente na stack da aplicação."""
    from fastapi.middleware.cors import CORSMiddleware
    middlewares = [m.cls for m in app.user_middleware]
    assert CORSMiddleware in middlewares


def test_rota_vagas_retorna_200():
    response = client.get("/vagas/")
    assert response.status_code == 200


def test_rota_vagas_criar_retorna_200():
    response = client.get("/vagas/criar")
    assert response.status_code == 200


def test_rota_curriculo_upload_retorna_200():
    response = client.get("/curriculos/upload/1")
    assert response.status_code == 200


def test_rota_ranking_retorna_200():
    response = client.get("/ranking/1")
    assert response.status_code == 200


def test_rota_inexistente_retorna_404():
    response = client.get("/pagina-que-nao-existe")
    assert response.status_code == 404
