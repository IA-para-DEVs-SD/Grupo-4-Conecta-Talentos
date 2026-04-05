"""Processor de extração de texto PDF — integra ExtratorPDF no pipeline da app."""

from pathlib import Path

from backend.src.services.extrator_pdf import (
    ExtratorPDF,
    PDFCorromidoError,
    PDFError,
    PDFMuitoGrandeError,
    TextoExtraido,
)

__all__ = [
    "ExtratorPDF",
    "TextoExtraido",
    "PDFError",
    "PDFCorromidoError",
    "PDFMuitoGrandeError",
    "extrair_texto_pdf",
]


def extrair_texto_pdf(caminho: Path, max_paginas: int = 10) -> TextoExtraido:
    """Extrai texto de um PDF salvo em disco.

    Args:
        caminho: Caminho absoluto ou relativo para o arquivo PDF.
        max_paginas: Limite de páginas a processar.

    Returns:
        TextoExtraido com conteúdo e metadados.

    Raises:
        PDFCorromidoError: Se o arquivo não puder ser aberto.
        PDFMuitoGrandeError: Se o PDF exceder o limite de páginas.
    """
    return ExtratorPDF(max_paginas=max_paginas).extrair_texto(caminho)
