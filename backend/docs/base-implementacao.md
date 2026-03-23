# Base de Implementação - ConectaTalentos

## Visão Geral

Este documento fornece orientações práticas para implementação do sistema ConectaTalentos, servindo como guia para o desenvolvimento do projeto no curso IA para Devs.

## Stack Tecnológica Recomendada

### Backend
- **Python 3.11+**
- **FastAPI** - Framework web moderno e rápido
- **SQLite** - Banco de dados embutido (sem necessidade de servidor)
- **SQLAlchemy** - ORM para acesso ao banco
- **Pydantic** - Validação de dados

### Processamento
- **pymupdf** - Extração de texto de PDFs (já implementado)
- **presidio-analyzer** e **presidio-anonymizer** - Anonimização LGPD
- **tiktoken** - Contagem de tokens para otimização
- **openai** - Cliente para GPT-4o-mini ou GPT-3.5-turbo

### Frontend
- **Jinja2** - Templates HTML (integrado com FastAPI)
- **Bootstrap 5** - Framework CSS responsivo
- **HTMX** - Interatividade sem JavaScript complexo

### Testes
- **pytest** - Framework de testes
- **hypothesis** - Property-based testing
- **pytest-cov** - Cobertura de código

## Estrutura do Projeto

```
conecta-talentos/
├── app/
│   ├── __init__.py
│   ├── main.py                 # Entry point FastAPI
│   ├── config.py               # Configurações e variáveis de ambiente
│   ├── database.py             # Setup do SQLAlchemy
│   │
│   ├── controllers/            # Rotas HTTP
│   │   ├── __init__.py
│   │   ├── vaga_controller.py
│   │   ├── curriculo_controller.py
│   │   └── ranking_controller.py
│   │
│   ├── services/               # Lógica de negócio
│   │   ├── __init__.py
│   │   ├── vaga_service.py
│   │   ├── curriculo_service.py
│   │   ├── processamento_service.py
│   │   └── ranking_service.py
│   │
│   ├── processors/             # Pipeline de processamento
│   │   ├── __init__.py
│   │   ├── extrator_pdf.py
│   │   ├── anonimizador.py
│   │   ├── otimizador_prompt.py
│   │   └── analisador_llm.py
│   │
│   ├── repositories/           # Acesso a dados
│   │   ├── __init__.py
│   │   ├── vaga_repository.py
│   │   ├── curriculo_repository.py
│   │   └── analise_repository.py
│   │
│   ├── models/                 # Modelos de dados
│   │   ├── __init__.py
│   │   ├── domain.py           # Dataclasses de domínio
│   │   └── orm.py              # Modelos SQLAlchemy
│   │
│   ├── templates/              # Templates HTML
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── vagas/
│   │   │   ├── lista.html
│   │   │   ├── criar.html
│   │   │   └── detalhes.html
│   │   ├── curriculos/
│   │   │   └── upload.html
│   │   └── ranking/
│   │       └── visualizar.html
│   │
│   └── static/                 # Arquivos estáticos
│       ├── css/
│       │   └── style.css
│       └── js/
│           └── app.js
│
├── data/
│   ├── database.db             # SQLite (gerado automaticamente)
│   └── uploads/                # PDFs enviados
│       └── vaga_{id}/
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py             # Fixtures compartilhadas
│   ├── unit/
│   ├── integration/
│   └── property/
│
├── .env                        # Variáveis de ambiente (não commitar)
├── .env.example                # Template de variáveis
├── requirements.txt            # Dependências Python
├── README.md
└── run.py                      # Script para iniciar aplicação
```


## Instalação e Setup

### 1. Criar Ambiente Virtual

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate  # Windows
```

### 2. Instalar Dependências

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Arquivo requirements.txt

```txt
# Web Framework
fastapi==0.109.0
uvicorn[standard]==0.27.0
python-multipart==0.0.6
jinja2==3.1.3

# Database
sqlalchemy==2.0.25
alembic==1.13.1

# PDF Processing
pymupdf==1.23.21

# Anonimização
presidio-analyzer==2.2.351
presidio-anonymizer==2.2.351
spacy==3.7.2

# LLM
openai==1.12.0
tiktoken==0.5.2

# Utilities
python-dotenv==1.0.1
pydantic==2.6.0
pydantic-settings==2.1.0

# Testing
pytest==8.0.0
pytest-cov==4.1.0
pytest-asyncio==0.23.4
hypothesis==6.98.0

# Development
black==24.1.1
ruff==0.2.1
```

### 4. Configurar Variáveis de Ambiente

Criar arquivo `.env`:

```env
# Aplicação
APP_NAME=ConectaTalentos
DEBUG=True
SECRET_KEY=sua-chave-secreta-aqui

# Banco de Dados
DATABASE_URL=sqlite:///./data/database.db

# OpenAI
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o-mini
OPENAI_MAX_TOKENS=2000

# Upload
UPLOAD_DIR=./data/uploads
MAX_FILE_SIZE_MB=10
MAX_PDF_PAGES=10

# Presidio
PRESIDIO_LANGUAGE=pt
```

### 5. Baixar Modelo de Linguagem para Presidio

```bash
python -m spacy download pt_core_news_lg
```

### 6. Inicializar Banco de Dados

```bash
python -m app.database init
```

## Implementação por Componentes

### 1. Configuração (app/config.py)

```python
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    app_name: str = "ConectaTalentos"
    debug: bool = False
    secret_key: str
    
    database_url: str = "sqlite:///./data/database.db"
    
    openai_api_key: str
    openai_model: str = "gpt-4o-mini"
    openai_max_tokens: int = 2000
    
    upload_dir: str = "./data/uploads"
    max_file_size_mb: int = 10
    max_pdf_pages: int = 10
    
    presidio_language: str = "pt"
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()
```

### 2. Modelos ORM (app/models/orm.py)

```python
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()

class VagaORM(Base):
    __tablename__ = "vagas"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String(200), nullable=False)
    descricao = Column(Text, nullable=False)
    requisitos_tecnicos = Column(Text, nullable=False)  # JSON
    experiencia_minima = Column(String(100), nullable=False)
    competencias_desejadas = Column(Text, nullable=False)  # JSON
    criado_em = Column(DateTime, default=datetime.utcnow)
    atualizado_em = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    curriculos = relationship("CurriculoORM", back_populates="vaga", cascade="all, delete-orphan")

class CurriculoORM(Base):
    __tablename__ = "curriculos"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    vaga_id = Column(Integer, ForeignKey("vagas.id", ondelete="CASCADE"), nullable=False)
    nome_arquivo = Column(String(255), nullable=False)
    caminho_pdf = Column(String(500), nullable=False)
    texto_extraido = Column(Text)
    texto_anonimizado = Column(Text)
    enviado_em = Column(DateTime, default=datetime.utcnow)
    status = Column(String(50), default="pendente")
    
    vaga = relationship("VagaORM", back_populates="curriculos")
    analise = relationship("AnaliseORM", back_populates="curriculo", uselist=False, cascade="all, delete-orphan")

class AnaliseORM(Base):
    __tablename__ = "analises"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    curriculo_id = Column(Integer, ForeignKey("curriculos.id", ondelete="CASCADE"), nullable=False, unique=True)
    score = Column(Integer, nullable=False)
    justificativa = Column(Text, nullable=False)
    pontos_fortes = Column(Text, nullable=False)  # JSON
    gaps = Column(Text, nullable=False)  # JSON
    tokens_usados = Column(Integer, nullable=False)
    analisado_em = Column(DateTime, default=datetime.utcnow)
    
    curriculo = relationship("CurriculoORM", back_populates="analise")
    
    __table_args__ = (
        CheckConstraint('score >= 0 AND score <= 100', name='check_score_range'),
    )
```

### 3. Database Setup (app/database.py)

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.config import get_settings
from app.models.orm import Base

settings = get_settings()

engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False} if "sqlite" in settings.database_url else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Inicializa o banco de dados criando todas as tabelas."""
    Base.metadata.create_all(bind=engine)

def get_db() -> Session:
    """Dependency para obter sessão do banco."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### 4. Extrator PDF (app/processors/extrator_pdf.py)

```python
from pathlib import Path
from dataclasses import dataclass
import pymupdf

@dataclass
class TextoExtraido:
    conteudo: str
    num_paginas: int
    tamanho_bytes: int

class PDFError(Exception):
    pass

class PDFCorromidoError(PDFError):
    pass

class PDFMuitoGrandeError(PDFError):
    pass

class ExtratorPDF:
    def __init__(self, max_paginas: int = 10):
        self.max_paginas = max_paginas
    
    def extrair_texto(self, pdf_path: Path) -> TextoExtraido:
        """Extrai texto de um arquivo PDF."""
        try:
            doc = pymupdf.open(pdf_path)
        except Exception as e:
            raise PDFCorromidoError(f"Não foi possível abrir o PDF: {e}")
        
        try:
            num_paginas = len(doc)
            
            if num_paginas > self.max_paginas:
                raise PDFMuitoGrandeError(
                    f"PDF tem {num_paginas} páginas, máximo permitido: {self.max_paginas}"
                )
            
            texto = "\n".join(page.get_text() for page in doc)
            tamanho = pdf_path.stat().st_size
            
            return TextoExtraido(
                conteudo=texto,
                num_paginas=num_paginas,
                tamanho_bytes=tamanho
            )
        finally:
            doc.close()
```

### 5. Anonimizador (app/processors/anonimizador.py)

```python
from dataclasses import dataclass
from typing import Dict, List
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig

@dataclass
class TextoAnonimizado:
    conteudo: str
    substituicoes: Dict[str, List[str]]
    sucesso: bool

class AnonimizacaoError(Exception):
    pass

class Anonimizador:
    def __init__(self, language: str = "pt"):
        self.language = language
        self.analyzer = AnalyzerEngine()
        self.anonymizer = AnonymizerEngine()
        
        # Mapeamento de entidades para tokens
        self.entity_mapping = {
            "PERSON": "[NOME]",
            "EMAIL_ADDRESS": "[EMAIL]",
            "PHONE_NUMBER": "[TELEFONE]",
            "LOCATION": "[ENDEREÇO]",
            "BR_CPF": "[CPF]",
        }
    
    def anonimizar(self, texto: str) -> TextoAnonimizado:
        """Remove dados sensíveis do texto."""
        try:
            # Analisar texto para encontrar entidades
            results = self.analyzer.analyze(
                text=texto,
                language=self.language,
                entities=list(self.entity_mapping.keys())
            )
            
            # Configurar operadores de anonimização
            operators = {}
            for entity_type, token in self.entity_mapping.items():
                operators[entity_type] = OperatorConfig("replace", {"new_value": token})
            
            # Anonimizar
            anonymized_result = self.anonymizer.anonymize(
                text=texto,
                analyzer_results=results,
                operators=operators
            )
            
            # Coletar substituições
            substituicoes = {}
            for result in results:
                entity_type = result.entity_type
                if entity_type not in substituicoes:
                    substituicoes[entity_type] = []
                substituicoes[entity_type].append(texto[result.start:result.end])
            
            return TextoAnonimizado(
                conteudo=anonymized_result.text,
                substituicoes=substituicoes,
                sucesso=True
            )
        
        except Exception as e:
            # Falha não-crítica: retornar texto original
            raise AnonimizacaoError(f"Falha na anonimização: {e}")
```


### 6. Otimizador de Prompt (app/processors/otimizador_prompt.py)

```python
import json
import tiktoken
from dataclasses import dataclass
from typing import Dict, Any
from app.models.domain import Vaga

@dataclass
class PromptOtimizado:
    conteudo: str
    tokens_estimados: int
    formato: str = "json"

class OtimizadorPrompt:
    def __init__(self, model: str = "gpt-4o-mini", max_tokens: int = 2000):
        self.model = model
        self.max_tokens = max_tokens
        self.encoding = tiktoken.encoding_for_model(model)
    
    def contar_tokens(self, texto: str) -> int:
        """Conta tokens usando tiktoken."""
        return len(self.encoding.encode(texto))
    
    def otimizar(self, vaga: Vaga, texto_anonimizado: str) -> PromptOtimizado:
        """Cria prompt otimizado para o LLM."""
        # Estrutura compacta da vaga
        vaga_dict = {
            "titulo": vaga.titulo,
            "requisitos": vaga.requisitos_tecnicos,
            "experiencia": vaga.experiencia_minima,
            "competencias": vaga.competencias_desejadas
        }
        
        # Extrair seções relevantes do currículo
        curriculo_otimizado = self._extrair_secoes_relevantes(texto_anonimizado)
        
        # Montar prompt JSON
        prompt_dict = {
            "vaga": vaga_dict,
            "candidato": curriculo_otimizado
        }
        
        prompt_json = json.dumps(prompt_dict, ensure_ascii=False, indent=None)
        tokens = self.contar_tokens(prompt_json)
        
        # Se exceder limite, resumir
        if tokens > self.max_tokens:
            prompt_json = self._resumir_prompt(prompt_dict)
            tokens = self.contar_tokens(prompt_json)
        
        return PromptOtimizado(
            conteudo=prompt_json,
            tokens_estimados=tokens
        )
    
    def _extrair_secoes_relevantes(self, texto: str) -> Dict[str, str]:
        """Extrai seções relevantes do currículo."""
        # Implementação simplificada - pode ser melhorada com NLP
        secoes = {
            "experiencia": "",
            "formacao": "",
            "habilidades": ""
        }
        
        # Buscar por palavras-chave de seções
        texto_lower = texto.lower()
        
        # Experiência
        if "experiência" in texto_lower or "experiencia" in texto_lower:
            inicio = texto_lower.find("experiência")
            if inicio == -1:
                inicio = texto_lower.find("experiencia")
            fim = texto_lower.find("\n\n", inicio + 100)
            if fim == -1:
                fim = inicio + 500
            secoes["experiencia"] = texto[inicio:fim].strip()
        
        # Formação
        if "formação" in texto_lower or "formacao" in texto_lower or "educação" in texto_lower:
            inicio = max(
                texto_lower.find("formação"),
                texto_lower.find("formacao"),
                texto_lower.find("educação")
            )
            fim = texto_lower.find("\n\n", inicio + 100)
            if fim == -1:
                fim = inicio + 300
            secoes["formacao"] = texto[inicio:fim].strip()
        
        # Habilidades
        if "habilidades" in texto_lower or "competências" in texto_lower:
            inicio = max(
                texto_lower.find("habilidades"),
                texto_lower.find("competências")
            )
            fim = texto_lower.find("\n\n", inicio + 100)
            if fim == -1:
                fim = inicio + 300
            secoes["habilidades"] = texto[inicio:fim].strip()
        
        return secoes
    
    def _resumir_prompt(self, prompt_dict: Dict[str, Any]) -> str:
        """Resume o prompt se exceder limite de tokens."""
        # Estratégia: truncar seções do currículo
        candidato = prompt_dict["candidato"]
        
        for secao in ["experiencia", "formacao", "habilidades"]:
            if secao in candidato and len(candidato[secao]) > 200:
                candidato[secao] = candidato[secao][:200] + "..."
        
        return json.dumps(prompt_dict, ensure_ascii=False, indent=None)
```

### 7. Analisador LLM (app/processors/analisador_llm.py)

```python
import json
from dataclasses import dataclass
from typing import List
from openai import OpenAI
from tenacity import retry, stop_after_attempt, wait_exponential
from app.config import get_settings

@dataclass
class AnaliseCanditado:
    score: int
    justificativa: str
    pontos_fortes: List[str]
    gaps: List[str]
    tokens_usados: int

class LLMError(Exception):
    pass

class LLMIndisponivelError(LLMError):
    pass

class LLMTimeoutError(LLMError):
    pass

class AnalisadorLLM:
    def __init__(self):
        settings = get_settings()
        self.client = OpenAI(api_key=settings.openai_api_key)
        self.model = settings.openai_model
        
        self.system_prompt = """Você é um especialista em recrutamento e seleção.
Analise o candidato em relação à vaga e retorne APENAS um JSON válido com:
{
  "score": <número de 0 a 100>,
  "justificativa": "<máximo 3 frases explicando o score>",
  "pontos_fortes": ["<ponto 1>", "<ponto 2>", ...],
  "gaps": ["<gap 1>", "<gap 2>", ...]
}

Critérios de avaliação:
- Adequação técnica aos requisitos (40%)
- Experiência relevante (30%)
- Competências comportamentais (20%)
- Formação acadêmica (10%)"""
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    def analisar(self, prompt_otimizado: str) -> AnaliseCanditado:
        """Analisa candidato usando LLM com retry automático."""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": prompt_otimizado}
                ],
                temperature=0.3,
                max_tokens=500,
                response_format={"type": "json_object"}
            )
            
            # Extrair resposta
            content = response.choices[0].message.content
            tokens_usados = response.usage.total_tokens
            
            # Parse JSON
            resultado = json.loads(content)
            
            return AnaliseCanditado(
                score=int(resultado["score"]),
                justificativa=resultado["justificativa"],
                pontos_fortes=resultado.get("pontos_fortes", []),
                gaps=resultado.get("gaps", []),
                tokens_usados=tokens_usados
            )
        
        except json.JSONDecodeError as e:
            raise LLMError(f"Resposta do LLM não é JSON válido: {e}")
        except Exception as e:
            raise LLMIndisponivelError(f"Erro ao chamar LLM: {e}")
```

### 8. Service de Processamento (app/services/processamento_service.py)

```python
import logging
from pathlib import Path
from app.processors.extrator_pdf import ExtratorPDF, PDFError
from app.processors.anonimizador import Anonimizador, AnonimizacaoError
from app.processors.otimizador_prompt import OtimizadorPrompt
from app.processors.analisador_llm import AnalisadorLLM, LLMError
from app.models.domain import Vaga, Curriculo, Analise
from app.repositories.curriculo_repository import CurriculoRepository
from app.repositories.analise_repository import AnaliseRepository

logger = logging.getLogger(__name__)

class ProcessamentoService:
    def __init__(self):
        self.extrator = ExtratorPDF()
        self.anonimizador = Anonimizador()
        self.otimizador = OtimizadorPrompt()
        self.analisador = AnalisadorLLM()
    
    def processar_curriculo(
        self,
        curriculo: Curriculo,
        vaga: Vaga,
        curriculo_repo: CurriculoRepository,
        analise_repo: AnaliseRepository
    ) -> Analise:
        """Processa currículo através do pipeline completo."""
        
        # 1. Extrair texto
        logger.info(f"Extraindo texto do currículo {curriculo.id}")
        try:
            texto_extraido = self.extrator.extrair_texto(Path(curriculo.caminho_pdf))
            curriculo.texto_extraido = texto_extraido.conteudo
            curriculo.status = "extraido"
            curriculo_repo.atualizar(curriculo)
        except PDFError as e:
            logger.error(f"Erro ao extrair PDF: {e}")
            curriculo.status = "erro"
            curriculo_repo.atualizar(curriculo)
            raise
        
        # 2. Anonimizar
        logger.info(f"Anonimizando currículo {curriculo.id}")
        try:
            texto_anonimizado = self.anonimizador.anonimizar(curriculo.texto_extraido)
            curriculo.texto_anonimizado = texto_anonimizado.conteudo
            curriculo_repo.atualizar(curriculo)
        except AnonimizacaoError as e:
            logger.warning(f"Falha na anonimização (não-crítico): {e}")
            curriculo.texto_anonimizado = curriculo.texto_extraido
        
        # 3. Otimizar prompt
        logger.info(f"Otimizando prompt para currículo {curriculo.id}")
        prompt_otimizado = self.otimizador.otimizar(vaga, curriculo.texto_anonimizado)
        
        # 4. Analisar com LLM
        logger.info(f"Analisando currículo {curriculo.id} com LLM")
        try:
            analise_resultado = self.analisador.analisar(prompt_otimizado.conteudo)
            
            # Criar análise
            analise = Analise(
                id=None,
                curriculo_id=curriculo.id,
                score=analise_resultado.score,
                justificativa=analise_resultado.justificativa,
                pontos_fortes=analise_resultado.pontos_fortes,
                gaps=analise_resultado.gaps,
                tokens_usados=analise_resultado.tokens_usados,
                analisado_em=None  # Será preenchido pelo repository
            )
            
            analise = analise_repo.criar(analise)
            
            curriculo.status = "concluido"
            curriculo_repo.atualizar(curriculo)
            
            logger.info(f"Currículo {curriculo.id} processado com sucesso. Score: {analise.score}")
            return analise
        
        except LLMError as e:
            logger.error(f"Erro ao analisar com LLM: {e}")
            curriculo.status = "erro_llm"
            curriculo_repo.atualizar(curriculo)
            raise
```


### 9. FastAPI Main (app/main.py)

```python
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.config import get_settings
from app.database import init_db
from app.controllers import vaga_controller, curriculo_controller, ranking_controller

settings = get_settings()

# Criar aplicação
app = FastAPI(
    title=settings.app_name,
    debug=settings.debug
)

# Montar arquivos estáticos
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Templates
templates = Jinja2Templates(directory="app/templates")

# Incluir routers
app.include_router(vaga_controller.router, prefix="/vagas", tags=["vagas"])
app.include_router(curriculo_controller.router, prefix="/curriculos", tags=["curriculos"])
app.include_router(ranking_controller.router, prefix="/ranking", tags=["ranking"])

@app.on_event("startup")
def startup_event():
    """Inicializa banco de dados na startup."""
    init_db()

@app.get("/")
async def home(request: Request):
    """Página inicial."""
    return templates.TemplateResponse("index.html", {"request": request})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
```

### 10. Controller de Vagas (app/controllers/vaga_controller.py)

```python
from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.services.vaga_service import VagaService
from app.models.domain import VagaCreate

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
async def listar_vagas(request: Request, db: Session = Depends(get_db)):
    """Lista todas as vagas."""
    service = VagaService(db)
    vagas = service.listar_vagas()
    return templates.TemplateResponse(
        "vagas/lista.html",
        {"request": request, "vagas": vagas}
    )

@router.get("/criar", response_class=HTMLResponse)
async def form_criar_vaga(request: Request):
    """Formulário de criação de vaga."""
    return templates.TemplateResponse("vagas/criar.html", {"request": request})

@router.post("/criar")
async def criar_vaga(
    titulo: str = Form(...),
    descricao: str = Form(...),
    requisitos_tecnicos: str = Form(...),
    experiencia_minima: str = Form(...),
    competencias_desejadas: str = Form(...),
    db: Session = Depends(get_db)
):
    """Cria nova vaga."""
    service = VagaService(db)
    
    # Converter strings separadas por vírgula em listas
    requisitos = [r.strip() for r in requisitos_tecnicos.split(",")]
    competencias = [c.strip() for c in competencias_desejadas.split(",")]
    
    vaga_create = VagaCreate(
        titulo=titulo,
        descricao=descricao,
        requisitos_tecnicos=requisitos,
        experiencia_minima=experiencia_minima,
        competencias_desejadas=competencias
    )
    
    vaga = service.criar_vaga(vaga_create)
    return RedirectResponse(url=f"/vagas/{vaga.id}", status_code=303)

@router.get("/{vaga_id}", response_class=HTMLResponse)
async def detalhes_vaga(request: Request, vaga_id: int, db: Session = Depends(get_db)):
    """Detalhes de uma vaga."""
    service = VagaService(db)
    vaga = service.obter_vaga(vaga_id)
    return templates.TemplateResponse(
        "vagas/detalhes.html",
        {"request": request, "vaga": vaga}
    )
```

### 11. Controller de Currículos (app/controllers/curriculo_controller.py)

```python
from fastapi import APIRouter, Depends, Request, UploadFile, File, Form, BackgroundTasks
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from pathlib import Path
from app.database import get_db
from app.services.curriculo_service import CurriculoService
from app.services.vaga_service import VagaService
from app.config import get_settings

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")
settings = get_settings()

@router.get("/upload/{vaga_id}", response_class=HTMLResponse)
async def form_upload(request: Request, vaga_id: int, db: Session = Depends(get_db)):
    """Formulário de upload de currículo."""
    vaga_service = VagaService(db)
    vaga = vaga_service.obter_vaga(vaga_id)
    return templates.TemplateResponse(
        "curriculos/upload.html",
        {"request": request, "vaga": vaga}
    )

@router.post("/upload/{vaga_id}")
async def upload_curriculo(
    vaga_id: int,
    background_tasks: BackgroundTasks,
    arquivo: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Faz upload e processa currículo."""
    # Validar formato
    if not arquivo.filename.endswith(".pdf"):
        return {"error": "Apenas arquivos PDF são aceitos"}
    
    service = CurriculoService(db)
    
    # Processar currículo (em background)
    curriculo = await service.processar_curriculo_upload(vaga_id, arquivo, background_tasks)
    
    return RedirectResponse(url=f"/ranking/{vaga_id}", status_code=303)
```

### 12. Template Base (app/templates/base.html)

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}ConectaTalentos{% endblock %}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="{{ url_for('static', path='/css/style.css') }}">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
        <div class="container">
            <a class="navbar-brand" href="/">ConectaTalentos</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav">
                    <li class="nav-item">
                        <a class="nav-link" href="/vagas">Vagas</a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>

    <main class="container mt-4">
        {% block content %}{% endblock %}
    </main>

    <footer class="mt-5 py-3 bg-light">
        <div class="container text-center">
            <p class="text-muted">ConectaTalentos - Grupo 4 - IA para Devs</p>
        </div>
    </footer>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    {% block scripts %}{% endblock %}
</body>
</html>
```

### 13. Template de Lista de Vagas (app/templates/vagas/lista.html)

```html
{% extends "base.html" %}

{% block title %}Vagas - ConectaTalentos{% endblock %}

{% block content %}
<div class="d-flex justify-content-between align-items-center mb-4">
    <h1>Vagas Cadastradas</h1>
    <a href="/vagas/criar" class="btn btn-primary">Nova Vaga</a>
</div>

{% if vagas %}
<div class="row">
    {% for vaga in vagas %}
    <div class="col-md-6 mb-3">
        <div class="card">
            <div class="card-body">
                <h5 class="card-title">{{ vaga.titulo }}</h5>
                <p class="card-text">{{ vaga.descricao[:150] }}...</p>
                <p class="text-muted">
                    <small>Experiência: {{ vaga.experiencia_minima }}</small>
                </p>
                <div class="d-flex gap-2">
                    <a href="/vagas/{{ vaga.id }}" class="btn btn-sm btn-outline-primary">Ver Detalhes</a>
                    <a href="/curriculos/upload/{{ vaga.id }}" class="btn btn-sm btn-outline-success">Upload Currículo</a>
                    <a href="/ranking/{{ vaga.id }}" class="btn btn-sm btn-outline-info">Ver Ranking</a>
                </div>
            </div>
        </div>
    </div>
    {% endfor %}
</div>
{% else %}
<div class="alert alert-info">
    Nenhuma vaga cadastrada. <a href="/vagas/criar">Criar primeira vaga</a>
</div>
{% endif %}
{% endblock %}
```

## Executando a Aplicação

### Desenvolvimento

```bash
# Ativar ambiente virtual
source .venv/bin/activate

# Executar aplicação
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Acessar: http://localhost:8000

### Produção

```bash
# Instalar gunicorn
pip install gunicorn

# Executar com gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## Próximos Passos

1. **Implementar todos os controllers e services**
2. **Criar todos os templates HTML**
3. **Implementar testes unitários e de propriedade**
4. **Adicionar logging estruturado**
5. **Implementar processamento assíncrono com Celery (opcional)**
6. **Adicionar autenticação de usuários (opcional)**
7. **Deploy em produção (Heroku, Railway, ou similar)**

## Dicas de Implementação

### 1. Comece Simples
- Implemente primeiro o fluxo básico: criar vaga → upload currículo → ver resultado
- Adicione features incrementalmente

### 2. Use Mocks nos Testes
- Mock do LLM para testes rápidos
- Mock do Presidio se necessário

### 3. Otimize Depois
- Foque primeiro em funcionalidade
- Otimize tokens e performance depois

### 4. Documente o Código
- Use docstrings em todas as funções
- Comente decisões não-óbvias

### 5. Versionamento
- Commit frequente com mensagens claras
- Use branches para features

## Recursos Adicionais

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Hypothesis Documentation](https://hypothesis.readthedocs.io/)
- [Microsoft Presidio](https://microsoft.github.io/presidio/)
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)
