# Project Structure - ConectaTalentos

## Directory Organization

```
conecta-talentos/
├── .kiro/                      # Kiro configuration and specs
│   ├── specs/                  # Feature specifications
│   │   └── conecta-talentos/   # Main project spec
│   └── steering/               # AI assistant guidance rules
│
├── backend/                    # Backend application
│   ├── docs/                   # Technical documentation
│   ├── src/                    # Source code
│   │   └── services/           # Business logic and processors
│   ├── tests/                  # Test files
│   ├── requirements-basico.txt # Python dependencies
│   └── .env.example            # Environment variables template
│
├── scripts/                    # Utility scripts
│   ├── create-github-issues.*  # GitHub issue creation scripts
│   └── github-tasks.md         # Task definitions for GitHub
│
└── README.md                   # Project documentation
```

## Planned Architecture (from spec)

The full application will follow this structure:

```
app/
├── main.py                     # FastAPI entry point
├── config.py                   # Settings and environment variables
├── database.py                 # SQLAlchemy setup
│
├── controllers/                # HTTP routes (FastAPI routers)
│   ├── vaga_controller.py
│   ├── curriculo_controller.py
│   └── ranking_controller.py
│
├── services/                   # Business logic layer
│   ├── vaga_service.py
│   ├── curriculo_service.py
│   ├── processamento_service.py
│   └── ranking_service.py
│
├── processors/                 # Processing pipeline components
│   ├── extrator_pdf.py         # PDF text extraction
│   ├── anonimizador.py         # LGPD data anonymization
│   ├── otimizador_prompt.py    # Token optimization
│   └── analisador_llm.py       # LLM analysis
│
├── repositories/               # Data access layer
│   ├── vaga_repository.py
│   ├── curriculo_repository.py
│   └── analise_repository.py
│
├── models/                     # Data models
│   ├── domain.py               # Domain dataclasses
│   └── orm.py                  # SQLAlchemy ORM models
│
├── templates/                  # Jinja2 HTML templates
│   ├── base.html
│   ├── vagas/
│   ├── curriculos/
│   └── ranking/
│
└── static/                     # Static assets
    ├── css/
    └── js/
```

## Current Implementation Status

### Implemented
- `backend/src/services/extrator_pdf.py` - PDF text extraction with PyMuPDF
- `backend/src/services/exemplo_uso_extrator.py` - Usage example
- `backend/docs/` - Technical documentation for PDF extractor

### Pending
- FastAPI application structure
- Database models and repositories
- Anonymization with Presidio
- LLM integration with OpenAI
- Web interface
- Complete test suite

## Architectural Patterns

### Layered Architecture
- **Controllers**: Handle HTTP requests/responses
- **Services**: Implement business logic
- **Repositories**: Abstract data access
- **Processors**: Specialized processing components (PDF, anonymization, LLM)

### Data Flow
1. User uploads PDF via controller
2. Service orchestrates processing pipeline
3. Processors handle extraction → anonymization → LLM analysis
4. Repository persists results
5. Controller returns ranked results

### Error Handling
- Custom exception hierarchy (PDFError, LLMError, etc.)
- Non-critical failures (anonymization) allow graceful degradation
- Critical failures (PDF extraction, LLM) propagate with descriptive messages

## File Naming Conventions

- Python modules: `snake_case.py`
- Classes: `PascalCase`
- Functions/variables: `snake_case`
- Constants: `UPPER_SNAKE_CASE`
- Test files: `test_*.py`
- Documentation: `kebab-case.md`

## Import Organization

Follow this order in Python files:
1. Standard library imports
2. Third-party imports
3. Local application imports

Example:
```python
from pathlib import Path
from dataclasses import dataclass

import pymupdf
from fastapi import APIRouter

from app.models.domain import Vaga
from app.services.vaga_service import VagaService
```
