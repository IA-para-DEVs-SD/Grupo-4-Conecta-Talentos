from urllib.parse import quote
from typing import List

from fastapi import APIRouter, Request, Depends, UploadFile, File, Query
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.curriculo_service import (
    CurriculoService,
    CurriculoError,
    VagaNaoEncontradaError,
    CurriculoNaoEncontradoError,
)
from app.services.vaga_service import VagaService, VagaNotFoundError

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.post("/api/{vaga_id}", status_code=201)
async def api_upload_curriculos(
    vaga_id: int,
    arquivos: List[UploadFile] = File(...),
    db: Session = Depends(get_db),
):

    from fastapi import HTTPException

    service = CurriculoService(db)

    itens = []
    for arq in arquivos:
        conteudo = await arq.read()
        itens.append((arq.filename or "sem_nome.pdf", conteudo))

    try:
        sucessos, erros = service.upload_multiplos(vaga_id, itens)
    except VagaNaoEncontradaError:
        raise HTTPException(status_code=404, detail=f"Vaga #{vaga_id} não encontrada.")

    return JSONResponse(
        status_code=201 if sucessos else 400,
        content={
            "enviados": len(sucessos),
            "erros": erros,
            "curriculos": [
                {
                    "id": c.id,
                    "nome_arquivo": c.nome_arquivo,
                    "status": c.status,
                }
                for c in sucessos
            ],
        },
    )


@router.get("/api/{vaga_id}")
def api_listar_curriculos(vaga_id: int, db: Session = Depends(get_db)):
    service = CurriculoService(db)
    curriculos = service.listar_por_vaga(vaga_id)
    return {
        "vaga_id": vaga_id,
        "total": len(curriculos),
        "curriculos": [
            {
                "id": c.id,
                "nome_arquivo": c.nome_arquivo,
                "status": c.status,
                "enviado_em": c.enviado_em.isoformat() if c.enviado_em else None,
            }
            for c in curriculos
        ],
    }


@router.delete("/api/{curriculo_id}", status_code=204)
def api_deletar_curriculo(curriculo_id: int, db: Session = Depends(get_db)):
    from fastapi import HTTPException
    service = CurriculoService(db)
    try:
        service.deletar(curriculo_id)
    except CurriculoNaoEncontradoError:
        raise HTTPException(status_code=404, detail=f"Currículo #{curriculo_id} não encontrado.")


@router.get("/upload/{vaga_id}", response_class=HTMLResponse)
def form_upload(request: Request, vaga_id: int, db: Session = Depends(get_db)):
    vaga_service = VagaService(db)
    try:
        vaga = vaga_service.obter(vaga_id)
    except VagaNotFoundError:
        return RedirectResponse(
            url=f"/vagas?msg={quote('Vaga não encontrada.')}&msg_level=danger",
            status_code=303,
        )
    curriculo_service = CurriculoService(db)
    curriculos = curriculo_service.listar_por_vaga(vaga_id)
    return templates.TemplateResponse(request, "curriculos/upload.html", {
        "vaga": vaga,
        "vaga_id": vaga_id,
        "curriculos": curriculos,
        "erro": None,
    })


@router.post("/upload/{vaga_id}", response_class=HTMLResponse)
async def upload_curriculos(
    request: Request,
    vaga_id: int,
    arquivos: List[UploadFile] = File(...),
    db: Session = Depends(get_db),
):
    service = CurriculoService(db)

    itens = []
    for arq in arquivos:
        conteudo = await arq.read()
        itens.append((arq.filename or "sem_nome.pdf", conteudo))

    try:
        sucessos, erros = service.upload_multiplos(vaga_id, itens)
    except VagaNaoEncontradaError:
        return RedirectResponse(
            url=f"/vagas?msg={quote('Vaga não encontrada.')}&msg_level=danger",
            status_code=303,
        )

    if erros and not sucessos:
        msg = quote("; ".join(erros))
        return RedirectResponse(
            url=f"/curriculos/upload/{vaga_id}?msg={msg}&msg_level=danger",
            status_code=303,
        )

    partes = []
    if sucessos:
        n = len(sucessos)
        partes.append(f"{n} currículo(s) enviado(s) com sucesso")
    if erros:
        partes.append(f"{len(erros)} erro(s): {'; '.join(erros)}")

    level = "success" if not erros else "warning"
    msg = quote(". ".join(partes) + ".")
    return RedirectResponse(
        url=f"/curriculos/upload/{vaga_id}?msg={msg}&msg_level={level}",
        status_code=303,
    )


@router.post("/{curriculo_id}/excluir")
def excluir_curriculo(
    curriculo_id: int,
    db: Session = Depends(get_db),
):
    service = CurriculoService(db)
    try:
        curriculo = service.obter(curriculo_id)
        vaga_id = curriculo.vaga_id
    except CurriculoNaoEncontradoError:
        return RedirectResponse(
            url=f"/vagas?msg={quote('Currículo não encontrado.')}&msg_level=danger",
            status_code=303,
        )
    service.deletar(curriculo_id)
    return RedirectResponse(
        url=f"/curriculos/upload/{vaga_id}?msg={quote('Currículo excluído com sucesso!')}&msg_level=success",
        status_code=303,
    )
