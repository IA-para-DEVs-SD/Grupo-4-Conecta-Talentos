"""Testes de conexão e configuração do banco de dados."""
from sqlalchemy import text, inspect
from app.database import engine, init_db
from app.models.orm import Base


def test_database_setup():
    """Verifica que o banco de dados está configurado corretamente com todas as tabelas."""
    init_db()

    # Verifica conexão
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        assert result.scalar() == 1

    # Verifica que as tabelas foram criadas
    inspector = inspect(engine)
    tabelas = inspector.get_table_names()
    assert "vagas" in tabelas
    assert "curriculos" in tabelas
    assert "analises" in tabelas

    # Verifica metadados
    tabelas_metadata = Base.metadata.tables.keys()
    assert "vagas" in tabelas_metadata
    assert "curriculos" in tabelas_metadata
    assert "analises" in tabelas_metadata
