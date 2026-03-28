import logging
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from app.config import get_settings
from app.database import init_db
from app.controllers import vaga_controller, curriculo_controller, ranking_controller

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s — %(message)s")

settings = get_settings()

app = FastAPI(title=settings.app_name, debug=settings.debug)

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

app.include_router(vaga_controller.router, prefix="/vagas", tags=["vagas"])
app.include_router(curriculo_controller.router, prefix="/curriculos", tags=["curriculos"])
app.include_router(ranking_controller.router, prefix="/ranking", tags=["ranking"])


@app.on_event("startup")
def startup():
    init_db()


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
