import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.orm import Base


@pytest.fixture
def db():
    """Banco em memória isolado para cada teste."""
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)
