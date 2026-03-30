"""Testes de conexão e configuração do banco de dados."""
from sqlalchemy import text
from app.database import engine, SessionLocal, init_db
from app.models.orm import Base, VagaORM, CurriculoORM, AnaliseORM


def test_conexao_banco():
    """Verifica que a conexão com o banco está funcionando."""
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        assert result.scalar() == 1


def test_init_db_cria_tabelas():
    """Verifica que init_db cria todas as tabelas esperadas."""
    init_db()
    tabelas = Base.metadata.tables.keys()
    assert "vagas" in tabelas
    assert "curriculos" in tabelas
    assert "analises" in tabelas


def test_session_abre_e_fecha():
    """Verifica que a sessão abre e fecha sem erros."""
    db = SessionLocal()
    try:
        result = db.execute(text("SELECT 1")).scalar()
        assert result == 1
    finally:
        db.close()


def test_tabelas_existem_no_banco():
    """Verifica que as tabelas foram criadas fisicamente no banco."""
    init_db()
    from sqlalchemy import inspect
    inspector = inspect(engine)
    tabelas = inspector.get_table_names()
    assert "vagas" in tabelas
    assert "curriculos" in tabelas
    assert "analises" in tabelas
