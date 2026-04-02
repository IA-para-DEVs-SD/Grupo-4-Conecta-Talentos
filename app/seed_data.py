"""Seed data para popular banco em ambiente DEV."""
from sqlalchemy.orm import Session

from app.models.domain import VagaCreate
from app.repositories.vaga_repository import VagaRepository


def seed_vagas_if_empty(db: Session) -> None:
    """Popula vagas se o banco estiver vazio (apenas em DEV)."""
    repo = VagaRepository(db)
    
    # Verifica se já existem vagas
    vagas_existentes = repo.listar()
    if vagas_existentes:
        print(f"✓ Banco já possui {len(vagas_existentes)} vagas. Seed não executado.")
        return
    
    print("⚙ Banco vazio. Populando com vagas de exemplo...")
    
    # Importa vagas do script
    from popular_vagas import criar_vagas
    criar_vagas()
