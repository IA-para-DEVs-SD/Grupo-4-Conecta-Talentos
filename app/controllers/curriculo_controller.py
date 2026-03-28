import logging
from fastapi import APIRouter, Depends, Request, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.config import get_settings
from app.database import get_db
from app.services.curriculo_service import CurriculoService
from app.services.vaga_service import VagaService, VagaNotFoundError

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")
settings = get_settings()
logger = logging.getLogger(__name__)


@router.get("/upload/{vaga_id}", response_class=HTMLResponse)
async def form_upload(request: Request, vaga_id: int, db: Session = Depends(get_db)):
    try:
        vaga = VagaService(db).obter_vaga(vaga_id)
    except VagaNotFoundError:
        raise HTTPException(status_code=404, detail="Vaga não encontrada")
    return templates.TemplateResponse(
        "curriculos/upload.html", {"request": request, "vaga": vaga}
    )


@router.post("/upload/{vaga_id}")
async def upload_curriculo(
    vaga_id: int,
    arquivo: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    if not arquivo.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Apenas arquivos PDF são aceitos")

    conteudo = await arquivo.read()
    tamanho_mb = len(conteudo) / (1024 * 1024)
    if tamanho_mb > settings.max_file_size_mb:
        raise HTTPException(
            status_code=400,
            detail=f"Arquivo muito grande. Máximo: {settings.max_file_size_mb}MB",
        )

    try:
        service = CurriculoService(db)
        service.salvar_e_processar(vaga_id, arquivo.filename, conteudo)
    except Exception as e:
        logger.error("Erro ao processar currículo: %s", e)
        raise HTTPException(status_code=500, detail=f"Erro ao processar currículo: {e}")

    return RedirectResponse(url=f"/ranking/{vaga_id}", status_code=303)
