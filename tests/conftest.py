"""Fixtures compartilhadas para testes."""

import pytest
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.testclient import TestClient

from app.models.orm import Base
from app.database import get_db
from app.controllers import vaga_controller, curriculo_controller, ranking_controller


def _create_test_app(get_db_override):
    """Cria app FastAPI sem lifespan para testes."""
    test_app = FastAPI()
    test_app.mount("/static", StaticFiles(directory="app/static"), name="static")

    from fastapi.templating import Jinja2Templates
    templates = Jinja2Templates(directory="app/templates")

    test_app.include_router(vaga_controller.router, prefix="/vagas")
    test_app.include_router(curriculo_controller.router, prefix="/curriculos")
    test_app.include_router(ranking_controller.router, prefix="/ranking")

    @test_app.get("/")
    async def home(request):
        return templates.TemplateResponse(request, "index.html")

    test_app.dependency_overrides[get_db] = get_db_override
    return test_app


@pytest.fixture()
def db_session():
    """Banco SQLite em memória para testes unitários."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def client():
    """TestClient com banco de teste em memória para integração."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    TestSessionLocal = sessionmaker(bind=engine)

    def _override_get_db():
        session = TestSessionLocal()
        try:
            yield session
        finally:
            session.close()

    test_app = _create_test_app(_override_get_db)

    with TestClient(test_app, raise_server_exceptions=True) as c:
        yield c

    Base.metadata.drop_all(bind=engine)
