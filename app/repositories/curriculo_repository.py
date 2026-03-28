from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.orm import CurriculoORM
from app.models.domain import Curriculo


def _orm_to_domain(orm: CurriculoORM) -> Curriculo:
    return Curriculo(
        id=orm.id,
        vaga_id=orm.vaga_id,
        nome_arquivo=orm.nome_arquivo,
        caminho_pdf=orm.caminho_pdf,
        texto_extraido=orm.texto_extraido,
        texto_anonimizado=orm.texto_anonimizado,
        status=orm.status,
        enviado_em=orm.enviado_em,
    )


class CurriculoRepository:
    def __init__(self, db: Session):
        self.db = db

    def criar(self, vaga_id: int, nome_arquivo: str, caminho_pdf: str) -> Curriculo:
        orm = CurriculoORM(
            vaga_id=vaga_id,
            nome_arquivo=nome_arquivo,
            caminho_pdf=caminho_pdf,
        )
        self.db.add(orm)
        self.db.commit()
        self.db.refresh(orm)
        return _orm_to_domain(orm)

    def atualizar(self, curriculo: Curriculo) -> Curriculo:
        orm = self.db.query(CurriculoORM).filter(CurriculoORM.id == curriculo.id).first()
        if not orm:
            raise ValueError(f"Currículo {curriculo.id} não encontrado")
        orm.texto_extraido = curriculo.texto_extraido
        orm.texto_anonimizado = curriculo.texto_anonimizado
        orm.status = curriculo.status
        self.db.commit()
        self.db.refresh(orm)
        return _orm_to_domain(orm)

    def listar_por_vaga(self, vaga_id: int) -> List[Curriculo]:
        return [
            _orm_to_domain(c)
            for c in self.db.query(CurriculoORM).filter(CurriculoORM.vaga_id == vaga_id).all()
        ]

    def obter(self, curriculo_id: int) -> Optional[Curriculo]:
        orm = self.db.query(CurriculoORM).filter(CurriculoORM.id == curriculo_id).first()
        return _orm_to_domain(orm) if orm else None
