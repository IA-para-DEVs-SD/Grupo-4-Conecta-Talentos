from urllib.parse import quote

from fastapi import APIRouter, Request, Depends, Form, Query
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.vaga_schema import (
    VagaCreateSchema, VagaResponseSchema, VagaListResponseSchema, _CAMPO_LABELS,
)
from app.services.vaga_service import VagaService, VagaNotFoundError

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.post("/api", response_model=VagaResponseSchema, status_code=201)
def api_criar_vaga(dados: VagaCreateSchema, db: Session = Depends(get_db)):
    service = VagaService(db)
    vaga = service.criar(dados)
    return _vaga_to_response(vaga)


@router.put("/api/{vaga_id}", response_model=VagaResponseSchema)
def api_atualizar_vaga(vaga_id: int, dados: VagaCreateSchema, db: Session = Depends(get_db)):
    service = VagaService(db)
    try:
        vaga = service.atualizar(vaga_id, dados)
    except VagaNotFoundError:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail=f"Vaga #{vaga_id} não encontrada.")
    return _vaga_to_response(vaga)


@router.get("/api", response_model=VagaListResponseSchema)
def api_listar_vagas(
    pagina: int = Query(1, ge=1),
    por_pagina: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    service = VagaService(db)
    vagas, total, total_paginas = service.listar_paginado(pagina, por_pagina)
    return VagaListResponseSchema(
        vagas=[_vaga_to_response(v) for v in vagas],
        total=total,
        pagina=pagina,
        por_pagina=por_pagina,
        total_paginas=total_paginas,
    )


@router.get("/api/{vaga_id}", response_model=VagaResponseSchema)
def api_obter_vaga(vaga_id: int, db: Session = Depends(get_db)):
    service = VagaService(db)
    try:
        vaga = service.obter(vaga_id)
    except VagaNotFoundError:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail=f"Vaga #{vaga_id} não encontrada.")
    return _vaga_to_response(vaga)


@router.delete("/api/{vaga_id}", status_code=204)
def api_deletar_vaga(vaga_id: int, db: Session = Depends(get_db)):
    service = VagaService(db)
    try:
        service.deletar(vaga_id)
    except VagaNotFoundError:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail=f"Vaga #{vaga_id} não encontrada.")


@router.get("/", response_class=HTMLResponse)
def listar_vagas(
    request: Request,
    pagina: int = Query(1, ge=1),
    db: Session = Depends(get_db),
):
    service = VagaService(db)
    vagas, total, total_paginas = service.listar_paginado(pagina, por_pagina=10)
    return templates.TemplateResponse(request, "vagas/lista.html", {
        "vagas": vagas,
        "pagina": pagina,
        "total_paginas": total_paginas,
        "total": total,
    })


@router.get("/criar", response_class=HTMLResponse)
def form_criar_vaga(request: Request):
    return templates.TemplateResponse(request, "vagas/criar.html", {"erro": None})


@router.post("/criar", response_class=HTMLResponse)
def criar_vaga(
    request: Request,
    titulo: str = Form(""),
    descricao: str = Form(""),
    requisitos_tecnicos: str = Form(""),
    experiencia_minima: str = Form(""),
    competencias_desejadas: str = Form(""),
    db: Session = Depends(get_db),
):
    try:
        schema = VagaCreateSchema(
            titulo=titulo,
            descricao=descricao,
            requisitos_tecnicos=[r.strip() for r in requisitos_tecnicos.split(",") if r.strip()],
            experiencia_minima=f"{experiencia_minima.strip()} ano(s)" if experiencia_minima.strip() else "",
            competencias_desejadas=[c.strip() for c in competencias_desejadas.split(",") if c.strip()],
        )
    except ValidationError as e:
        erros = _formatar_erros_pt(e)
        return templates.TemplateResponse(request, "vagas/criar.html", {
            "erro": erros,
            "form": {
                "titulo": titulo,
                "descricao": descricao,
                "requisitos_tecnicos": requisitos_tecnicos,
                "experiencia_minima": experiencia_minima,
                "competencias_desejadas": competencias_desejadas,
            },
        })

    service = VagaService(db)
    vaga = service.criar(schema)
    return RedirectResponse(
        url=f"/vagas/{vaga.id}?msg={quote('Vaga criada com sucesso!')}&msg_level=success",
        status_code=303,
    )


@router.get("/{vaga_id}", response_class=HTMLResponse)
def detalhes_vaga(request: Request, vaga_id: int, db: Session = Depends(get_db)):
    service = VagaService(db)
    try:
        vaga = service.obter(vaga_id)
    except VagaNotFoundError:
        return templates.TemplateResponse(request, "vagas/detalhes.html", {"vaga": None}, status_code=404)
    return templates.TemplateResponse(request, "vagas/detalhes.html", {"vaga": vaga})


@router.get("/{vaga_id}/editar", response_class=HTMLResponse)
def form_editar_vaga(request: Request, vaga_id: int, db: Session = Depends(get_db)):
    service = VagaService(db)
    try:
        vaga = service.obter(vaga_id)
    except VagaNotFoundError:
        return templates.TemplateResponse(request, "vagas/detalhes.html", {"vaga": None}, status_code=404)
    return templates.TemplateResponse(request, "vagas/editar.html", {
        "vaga": vaga,
        "erro": None,
    })


@router.post("/{vaga_id}/editar", response_class=HTMLResponse)
def editar_vaga(
    request: Request,
    vaga_id: int,
    titulo: str = Form(""),
    descricao: str = Form(""),
    requisitos_tecnicos: str = Form(""),
    experiencia_minima: str = Form(""),
    competencias_desejadas: str = Form(""),
    db: Session = Depends(get_db),
):
    try:
        schema = VagaCreateSchema(
            titulo=titulo,
            descricao=descricao,
            requisitos_tecnicos=[r.strip() for r in requisitos_tecnicos.split(",") if r.strip()],
            experiencia_minima=f"{experiencia_minima.strip()} ano(s)" if experiencia_minima.strip() else "",
            competencias_desejadas=[c.strip() for c in competencias_desejadas.split(",") if c.strip()],
        )
    except ValidationError as e:
        erros = _formatar_erros_pt(e)
        service = VagaService(db)
        try:
            vaga = service.obter(vaga_id)
        except VagaNotFoundError:
            vaga = None
        return templates.TemplateResponse(request, "vagas/editar.html", {
            "vaga": vaga,
            "erro": erros,
            "form": {
                "titulo": titulo,
                "descricao": descricao,
                "requisitos_tecnicos": requisitos_tecnicos,
                "experiencia_minima": experiencia_minima,
                "competencias_desejadas": competencias_desejadas,
            },
        })

    service = VagaService(db)
    try:
        service.atualizar(vaga_id, schema)
    except VagaNotFoundError:
        return templates.TemplateResponse(request, "vagas/detalhes.html", {"vaga": None}, status_code=404)
    return RedirectResponse(
        url=f"/vagas/{vaga_id}?msg={quote('Vaga atualizada com sucesso!')}&msg_level=success",
        status_code=303,
    )


@router.post("/{vaga_id}/excluir")
def excluir_vaga(vaga_id: int, db: Session = Depends(get_db)):
    service = VagaService(db)
    try:
        service.deletar(vaga_id)
    except VagaNotFoundError:
        return RedirectResponse(
            url=f"/vagas?msg={quote('Vaga não encontrada.')}&msg_level=danger",
            status_code=303,
        )
    return RedirectResponse(
        url=f"/vagas?msg={quote('Vaga excluída com sucesso!')}&msg_level=success",
        status_code=303,
    )


_MENSAGENS_PT = {
    "string_too_short": "deve ter pelo menos {min_length} caracteres",
    "string_too_long": "deve ter no máximo {max_length} caracteres",
    "missing": "é obrigatório",
    "string_type": "deve ser um texto",
    "list_type": "deve ser uma lista",
    "too_short": "deve ter pelo menos {min_length} item(ns)",
    "value_error": None,  # usa a mensagem do validator diretamente
}


def _formatar_erros_pt(e: ValidationError) -> str:
    mensagens = []
    for err in e.errors():
        campo = err["loc"][-1] if err["loc"] else "campo"
        label = _CAMPO_LABELS.get(campo, campo)
        tipo = err["type"]

        if tipo == "value_error":
            msg = err["msg"].replace("Value error, ", "")
            mensagens.append(msg)
        elif tipo in _MENSAGENS_PT:
            template = _MENSAGENS_PT[tipo]
            ctx = err.get("ctx", {})
            mensagens.append(f"{label}: {template.format(**ctx)}")
        else:
            mensagens.append(f"{label}: campo inválido")

    return "; ".join(mensagens) if mensagens else "Verifique os campos e tente novamente."


def _vaga_to_response(vaga) -> VagaResponseSchema:
    return VagaResponseSchema(
        id=vaga.id,
        titulo=vaga.titulo,
        descricao=vaga.descricao,
        requisitos_tecnicos=vaga.requisitos_tecnicos,
        experiencia_minima=vaga.experiencia_minima,
        competencias_desejadas=vaga.competencias_desejadas,
        criado_em=vaga.criado_em,
        atualizado_em=vaga.atualizado_em,
    )
