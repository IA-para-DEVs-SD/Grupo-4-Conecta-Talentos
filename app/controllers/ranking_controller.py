from fastapi import APIRouter, Depends, Request, Query, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.ranking_service import RankingService
from app.services.vaga_service import VagaService, VagaNotFoundError

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/{vaga_id}", response_class=HTMLResponse)
async def visualizar_ranking(
    request: Request,
    vaga_id: int,
    score_minimo: int = Query(default=0, ge=0, le=100),
    db: Session = Depends(get_db),
):
    try:
        vaga = VagaService(db).obter_vaga(vaga_id)
    except VagaNotFoundError:
        raise HTTPException(status_code=404, detail="Vaga não encontrada")

    ranking = RankingService(db).obter_ranking(vaga_id, score_minimo=score_minimo)

    return templates.TemplateResponse(
        "ranking/visualizar.html",
        {
            "request": request,
            "vaga": vaga,
            "ranking": ranking,
            "score_minimo": score_minimo,
        },
    )
