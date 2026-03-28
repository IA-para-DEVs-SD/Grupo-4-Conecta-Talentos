from fastapi import APIRouter, Depends, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.domain import VagaCreate
from app.services.vaga_service import VagaService, VagaNotFoundError

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
async def listar_vagas(request: Request, db: Session = Depends(get_db)):
    vagas = VagaService(db).listar_vagas()
    return templates.TemplateResponse("vagas/lista.html", {"request": request, "vagas": vagas})


@router.get("/criar", response_class=HTMLResponse)
async def form_criar(request: Request):
    return templates.TemplateResponse("vagas/criar.html", {"request": request})


@router.post("/criar")
async def criar_vaga(
    titulo: str = Form(...),
    descricao: str = Form(...),
    requisitos_tecnicos: str = Form(...),
    experiencia_minima: str = Form(...),
    competencias_desejadas: str = Form(...),
    db: Session = Depends(get_db),
):
    data = VagaCreate(
        titulo=titulo,
        descricao=descricao,
        requisitos_tecnicos=[r.strip() for r in requisitos_tecnicos.split(",") if r.strip()],
        experiencia_minima=experiencia_minima,
        competencias_desejadas=[c.strip() for c in competencias_desejadas.split(",") if c.strip()],
    )
    vaga = VagaService(db).criar_vaga(data)
    return RedirectResponse(url=f"/vagas/{vaga.id}", status_code=303)


@router.get("/{vaga_id}", response_class=HTMLResponse)
async def detalhes_vaga(request: Request, vaga_id: int, db: Session = Depends(get_db)):
    try:
        vaga = VagaService(db).obter_vaga(vaga_id)
    except VagaNotFoundError:
        raise HTTPException(status_code=404, detail="Vaga não encontrada")
    return templates.TemplateResponse("vagas/detalhes.html", {"request": request, "vaga": vaga})


@router.get("/{vaga_id}/editar", response_class=HTMLResponse)
async def form_editar(request: Request, vaga_id: int, db: Session = Depends(get_db)):
    try:
        vaga = VagaService(db).obter_vaga(vaga_id)
    except VagaNotFoundError:
        raise HTTPException(status_code=404, detail="Vaga não encontrada")
    return templates.TemplateResponse("vagas/criar.html", {"request": request, "vaga": vaga})


@router.post("/{vaga_id}/editar")
async def editar_vaga(
    vaga_id: int,
    titulo: str = Form(...),
    descricao: str = Form(...),
    requisitos_tecnicos: str = Form(...),
    experiencia_minima: str = Form(...),
    competencias_desejadas: str = Form(...),
    db: Session = Depends(get_db),
):
    data = VagaCreate(
        titulo=titulo,
        descricao=descricao,
        requisitos_tecnicos=[r.strip() for r in requisitos_tecnicos.split(",") if r.strip()],
        experiencia_minima=experiencia_minima,
        competencias_desejadas=[c.strip() for c in competencias_desejadas.split(",") if c.strip()],
    )
    try:
        VagaService(db).atualizar_vaga(vaga_id, data)
    except VagaNotFoundError:
        raise HTTPException(status_code=404, detail="Vaga não encontrada")
    return RedirectResponse(url=f"/vagas/{vaga_id}", status_code=303)


@router.post("/{vaga_id}/deletar")
async def deletar_vaga(vaga_id: int, db: Session = Depends(get_db)):
    try:
        VagaService(db).deletar_vaga(vaga_id)
    except VagaNotFoundError:
        raise HTTPException(status_code=404, detail="Vaga não encontrada")
    return RedirectResponse(url="/vagas/", status_code=303)
