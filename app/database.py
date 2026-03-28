from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.config import get_settings
from app.models.orm import Base

settings = get_settings()

engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False} if "sqlite" in settings.database_url else {},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db() -> None:
    """Cria todas as tabelas no banco de dados."""
    import os
    os.makedirs("data", exist_ok=True)
    Base.metadata.create_all(bind=engine)


def get_db() -> Session:
    """Dependency para injeção de sessão do banco."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
