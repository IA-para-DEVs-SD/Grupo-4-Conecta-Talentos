from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.domain import Vaga, VagaCreate
from app.repositories.vaga_repository import VagaRepository


class VagaNotFoundError(Exception):
    pass


class VagaService:
    def __init__(self, db: Session):
        self.repo = VagaRepository(db)

    def criar_vaga(self, data: VagaCreate) -> Vaga:
        return self.repo.criar(data)

    def listar_vagas(self) -> List[Vaga]:
        return self.repo.listar()

    def obter_vaga(self, vaga_id: int) -> Vaga:
        vaga = self.repo.obter(vaga_id)
        if not vaga:
            raise VagaNotFoundError(f"Vaga {vaga_id} não encontrada")
        return vaga

    def atualizar_vaga(self, vaga_id: int, data: VagaCreate) -> Vaga:
        vaga = self.repo.atualizar(vaga_id, data)
        if not vaga:
            raise VagaNotFoundError(f"Vaga {vaga_id} não encontrada")
        return vaga

    def deletar_vaga(self, vaga_id: int) -> None:
        if not self.repo.deletar(vaga_id):
            raise VagaNotFoundError(f"Vaga {vaga_id} não encontrada")
