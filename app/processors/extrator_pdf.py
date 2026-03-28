"""Extração de texto de arquivos PDF — wrapper para uso no pipeline app."""

from pathlib import Path
from backend.src.services.extrator_pdf import (  # reutiliza implementação existente
    ExtratorPDF,
    TextoExtraido,
    PDFError,
    PDFCorromidoError,
    PDFMuitoGrandeError,
)

__all__ = [
    "ExtratorPDF",
    "TextoExtraido",
    "PDFError",
    "PDFCorromidoError",
    "PDFMuitoGrandeError",
]
