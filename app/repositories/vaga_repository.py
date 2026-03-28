import json
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.orm import VagaORM
from app.models.domain import Vaga, VagaCreate


def _orm_to_domain(orm: VagaORM) -> Vaga:
    return Vaga(
        id=orm.id,
        titulo=orm.titulo,
        descricao=orm.descricao,
        requisitos_tecnicos=json.loads(orm.requisitos_tecnicos),
        experiencia_minima=orm.experiencia_minima,
        competencias_desejadas=json.loads(orm.competencias_desejadas),
        criado_em=orm.criado_em,
        atualizado_em=orm.atualizado_em,
    )


class VagaRepository:
    def __init__(self, db: Session):
        self.db = db

    def criar(self, data: VagaCreate) -> Vaga:
        orm = VagaORM(
            titulo=data.titulo,
            descricao=data.descricao,
            requisitos_tecnicos=json.dumps(data.requisitos_tecnicos, ensure_ascii=False),
            experiencia_minima=data.experiencia_minima,
            competencias_desejadas=json.dumps(data.competencias_desejadas, ensure_ascii=False),
        )
        self.db.add(orm)
        self.db.commit()
        self.db.refresh(orm)
        return _orm_to_domain(orm)

    def listar(self) -> List[Vaga]:
        return [_orm_to_domain(v) for v in self.db.query(VagaORM).all()]

    def obter(self, vaga_id: int) -> Optional[Vaga]:
        orm = self.db.query(VagaORM).filter(VagaORM.id == vaga_id).first()
        return _orm_to_domain(orm) if orm else None

    def atualizar(self, vaga_id: int, data: VagaCreate) -> Optional[Vaga]:
        orm = self.db.query(VagaORM).filter(VagaORM.id == vaga_id).first()
        if not orm:
            return None
        orm.titulo = data.titulo
        orm.descricao = data.descricao
        orm.requisitos_tecnicos = json.dumps(data.requisitos_tecnicos, ensure_ascii=False)
        orm.experiencia_minima = data.experiencia_minima
        orm.competencias_desejadas = json.dumps(data.competencias_desejadas, ensure_ascii=False)
        self.db.commit()
        self.db.refresh(orm)
        return _orm_to_domain(orm)

    def deletar(self, vaga_id: int) -> bool:
        orm = self.db.query(VagaORM).filter(VagaORM.id == vaga_id).first()
        if not orm:
            return False
        self.db.delete(orm)
        self.db.commit()
        return True
