from dataclasses import dataclass
from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.domain import Analise, Curriculo
from app.repositories.analise_repository import AnaliseRepository
from app.repositories.curriculo_repository import CurriculoRepository


@dataclass
class ItemRanking:
    posicao: int
    curriculo: Curriculo
    analise: Analise


class RankingService:
    def __init__(self, db: Session):
        self.analise_repo = AnaliseRepository(db)
        self.curriculo_repo = CurriculoRepository(db)

    def obter_ranking(self, vaga_id: int, score_minimo: int = 0) -> List[ItemRanking]:
        analises = self.analise_repo.listar_por_vaga(vaga_id)
        resultado = []
        posicao = 1
        for analise in analises:
            if analise.score < score_minimo:
                continue
            curriculo = self.curriculo_repo.obter(analise.curriculo_id)
            if curriculo:
                resultado.append(ItemRanking(posicao=posicao, curriculo=curriculo, analise=analise))
                posicao += 1
        return resultado
