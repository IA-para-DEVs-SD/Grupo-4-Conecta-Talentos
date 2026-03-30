from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.database import init_db
from app.controllers import vaga_controller, curriculo_controller, ranking_controller

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
    description="Sistema inteligente de ranqueamento de currículos com IA",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if settings.debug else [],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")


app.include_router(vaga_controller.router, prefix="/vagas", tags=["vagas"])
app.include_router(curriculo_controller.router, prefix="/curriculos", tags=["curriculos"])
app.include_router(ranking_controller.router, prefix="/ranking", tags=["ranking"])


@app.get("/", include_in_schema=False)
async def home(request: Request):
    return templates.TemplateResponse(request, "index.html")


@app.get("/health", tags=["infra"])
async def health():
    return {"status": "ok", "app": settings.app_name}
