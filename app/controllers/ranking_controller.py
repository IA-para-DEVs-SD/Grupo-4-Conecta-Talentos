from fastapi import APIRouter, Depends, HTTPException, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.ranking_service import RankingService

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/{vaga_id}", response_class=HTMLResponse)
async def visualizar_ranking(
    request: Request,
    vaga_id: int,
    reprocessar: bool = Query(False, description="Reprocessar análises existentes"),
    score_minimo: int = Query(0, ge=0, le=100, description="Pontuação mínima"),
    db: Session = Depends(get_db),
):
    """Visualiza ranking de candidatos para uma vaga.

    Args:
        request: Request do FastAPI
        vaga_id: ID da vaga
        reprocessar: Se True, reanalisa todos os currículos
        score_minimo: Filtro de pontuação mínima (0-100)
        db: Sessão do banco de dados

    Returns:
        Template HTML com o ranking
    """
    try:
        ranking_service = RankingService(db)

        # Gera ou obtém ranking
        if reprocessar:
            ranking = await ranking_service.gerar_ranking_async(
                vaga_id, reprocessar=True
            )
        else:
            # Tenta obter ranking existente
            ranking = ranking_service.obter_ranking_existente(vaga_id)

            # Se não houver análises, gera novo ranking
            if not ranking:
                ranking = await ranking_service.gerar_ranking_async(vaga_id)

        # Aplica filtro de score mínimo se especificado
        if score_minimo > 0:
            ranking = ranking_service.filtrar_por_score_minimo(ranking, score_minimo)

        return templates.TemplateResponse(
            request,
            "ranking/visualizar.html",
            {"vaga_id": vaga_id, "ranking": ranking, "score_minimo": score_minimo},
        )

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar ranking: {e}") from e


@router.post("/{vaga_id}/gerar")
async def gerar_ranking(
    vaga_id: int,
    reprocessar: bool = Query(False, description="Reprocessar análises existentes"),
    db: Session = Depends(get_db),
):
    """Endpoint para gerar ranking de forma explícita.

    Args:
        vaga_id: ID da vaga
        reprocessar: Se True, reanalisa todos os currículos
        db: Sessão do banco de dados

    Returns:
        JSON com o ranking gerado
    """
    try:
        ranking_service = RankingService(db)
        ranking = await ranking_service.gerar_ranking_async(vaga_id, reprocessar)

        return {
            "vaga_id": vaga_id,
            "total_candidatos": len(ranking),
            "ranking": [
                {
                    "curriculo_id": a.curriculo_id,
                    "score": a.score,
                    "justificativa": a.justificativa,
                    "pontos_fortes": a.pontos_fortes,
                    "gaps": a.gaps,
                    "tokens_usados": a.tokens_usados,
                    "analisado_em": a.analisado_em.isoformat(),
                }
                for a in ranking
            ],
        }

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar ranking: {e}") from e


@router.get("/{vaga_id}/top/{limite}")
async def obter_top_candidatos(
    vaga_id: int, limite: int, db: Session = Depends(get_db)
):
    """Obtém os N melhores candidatos de uma vaga.

    Args:
        vaga_id: ID da vaga
        limite: Número de candidatos a retornar
        db: Sessão do banco de dados

    Returns:
        JSON com os top N candidatos
    """
    try:
        ranking_service = RankingService(db)
        top_candidatos = ranking_service.obter_top_candidatos(vaga_id, limite)

        return {
            "vaga_id": vaga_id,
            "limite": limite,
            "total_retornado": len(top_candidatos),
            "candidatos": [
                {
                    "curriculo_id": a.curriculo_id,
                    "score": a.score,
                    "justificativa": a.justificativa,
                    "pontos_fortes": a.pontos_fortes,
                    "gaps": a.gaps,
                }
                for a in top_candidatos
            ],
        }

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro ao obter top candidatos: {e}"
        ) from e


@router.get("/{vaga_id}/candidato/{curriculo_id}")
async def obter_detalhes_candidato(
    vaga_id: int, curriculo_id: int, db: Session = Depends(get_db)
):
    """Obtém detalhes completos da análise de um candidato específico.

    Args:
        vaga_id: ID da vaga
        curriculo_id: ID do currículo do candidato
        db: Sessão do banco de dados

    Returns:
        JSON com detalhes completos do candidato
    """
    try:
        ranking_service = RankingService(db)

        # Busca análise do candidato
        analise = ranking_service.analise_repo.obter_por_curriculo(curriculo_id)

        if not analise:
            raise HTTPException(
                status_code=404,
                detail=f"Análise não encontrada para o currículo {curriculo_id}",
            )

        # Busca dados do currículo
        curriculo = ranking_service.curriculo_repo.obter_por_id(curriculo_id)

        if not curriculo or curriculo.vaga_id != vaga_id:
            raise HTTPException(
                status_code=404,
                detail=f"Currículo {curriculo_id} não encontrado para a vaga {vaga_id}",
            )

        # Busca dados da vaga
        vaga = ranking_service.vaga_repo.obter_por_id(vaga_id)

        return {
            "vaga": {
                "id": vaga.id,
                "titulo": vaga.titulo,
                "descricao": vaga.descricao,
                "requisitos": vaga.requisitos,
            },
            "curriculo": {
                "id": curriculo.id,
                "nome_arquivo": curriculo.nome_arquivo,
                "enviado_em": curriculo.enviado_em.isoformat(),
            },
            "analise": {
                "score": analise.score,
                "justificativa": analise.justificativa,
                "pontos_fortes": analise.pontos_fortes,
                "gaps": analise.gaps,
                "tokens_usados": analise.tokens_usados,
                "analisado_em": analise.analisado_em.isoformat(),
            },
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro ao obter detalhes do candidato: {e}"
        ) from e
