# Technology Stack - ConectaTalentos

## Core Technologies

### Backend
- **Python 3.11+** - Primary language
- **FastAPI** - Web framework and REST API
- **SQLAlchemy** - ORM for database access
- **SQLite** - Embedded database (no server required)
- **Pydantic** - Data validation and settings management

### PDF Processing & AI
- **PyMuPDF (pymupdf)** - PDF text extraction
- **Microsoft Presidio** (analyzer + anonymizer) - LGPD-compliant data anonymization
- **spaCy** - NLP model for Presidio (pt_core_news_lg)
- **OpenAI API** - LLM analysis (GPT-4o-mini or GPT-3.5-turbo)
- **tiktoken** - Token counting for prompt optimization

### Frontend
- **Jinja2** - HTML templating (integrated with FastAPI)
- **Bootstrap 5** - CSS framework
- **HTMX** - Dynamic interactions (optional)

### Testing
- **pytest** - Test framework
- **hypothesis** - Property-based testing
- **pytest-cov** - Code coverage
- **pytest-asyncio** - Async test support

### Development Tools
- **python-dotenv** - Environment variable management
- **black** - Code formatting
- **ruff** - Linting

## Common Commands

### Environment Setup
```bash
# Create virtual environment
python -m venv .venv

# Activate (Linux/Mac)
source .venv/bin/activate

# Activate (Windows)
.venv\Scripts\activate

# Install dependencies
pip install -r backend/requirements-basico.txt
```

### Development
```bash
# Run FastAPI development server (when implemented)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Test PDF extraction
python backend/src/services/exemplo_uso_extrator.py

# Extract specific PDF
python backend/src/services/extrator_pdf.py path/to/file.pdf
```

### Testing
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=backend/src --cov-report=html

# Run specific test file
pytest backend/tests/test_extrator.py

# Run property-based tests
pytest backend/tests/property/
```

### Database
```bash
# Initialize database (when implemented)
python -m app.database init

# Run migrations (when using Alembic)
alembic upgrade head
```

### Code Quality
```bash
# Format code
black backend/src

# Lint code
ruff check backend/src

# Type checking (if using mypy)
mypy backend/src
```

## Configuration

Environment variables are managed via `.env` file (see `.env.example` for template):
- `OPENAI_API_KEY` - OpenAI API key for LLM
- `OPENAI_MODEL` - Model to use (gpt-4o-mini recommended)
- `DATABASE_URL` - SQLite database path
- `UPLOAD_DIR` - Directory for uploaded PDFs
- `MAX_FILE_SIZE_MB` - Maximum PDF file size
- `MAX_PDF_PAGES` - Maximum pages per PDF (default: 10)
