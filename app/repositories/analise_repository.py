import json
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.orm import AnaliseORM
from app.models.domain import Analise


def _orm_to_domain(orm: AnaliseORM) -> Analise:
    return Analise(
        id=orm.id,
        curriculo_id=orm.curriculo_id,
        score=orm.score,
        justificativa=orm.justificativa,
        pontos_fortes=json.loads(orm.pontos_fortes),
        gaps=json.loads(orm.gaps),
        tokens_usados=orm.tokens_usados,
        analisado_em=orm.analisado_em,
    )


class AnaliseRepository:
    def __init__(self, db: Session):
        self.db = db

    def criar(self, analise: Analise) -> Analise:
        orm = AnaliseORM(
            curriculo_id=analise.curriculo_id,
            score=analise.score,
            justificativa=analise.justificativa,
            pontos_fortes=json.dumps(analise.pontos_fortes, ensure_ascii=False),
            gaps=json.dumps(analise.gaps, ensure_ascii=False),
            tokens_usados=analise.tokens_usados,
        )
        self.db.add(orm)
        self.db.commit()
        self.db.refresh(orm)
        return _orm_to_domain(orm)

    def obter_por_curriculo(self, curriculo_id: int) -> Optional[Analise]:
        orm = (
            self.db.query(AnaliseORM)
            .filter(AnaliseORM.curriculo_id == curriculo_id)
            .first()
        )
        return _orm_to_domain(orm) if orm else None

    def listar_por_vaga(self, vaga_id: int) -> List[Analise]:
        """Retorna análises ordenadas por score desc para uma vaga."""
        from app.models.orm import CurriculoORM
        rows = (
            self.db.query(AnaliseORM)
            .join(CurriculoORM, AnaliseORM.curriculo_id == CurriculoORM.id)
            .filter(CurriculoORM.vaga_id == vaga_id)
            .order_by(AnaliseORM.score.desc())
            .all()
        )
        return [_orm_to_domain(r) for r in rows]
