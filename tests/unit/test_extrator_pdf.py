"""Testes unitários para ExtratorPDF."""
import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch

from backend.src.services.extrator_pdf import (
    ExtratorPDF,
    PDFCorromidoError,
    PDFMuitoGrandeError,
)


def test_arquivo_inexistente():
    extrator = ExtratorPDF()
    with pytest.raises(PDFCorromidoError):
        extrator.extrair_texto(Path("nao_existe.pdf"))


def test_pdf_muitas_paginas(tmp_path):
    """Simula PDF com mais páginas que o limite."""
    pdf_fake = tmp_path / "grande.pdf"
    pdf_fake.write_bytes(b"%PDF-1.4")

    with patch("pymupdf.open") as mock_open:
        doc_mock = MagicMock()
        doc_mock.__len__.return_value = 20
        doc_mock.__enter__ = lambda s: s
        doc_mock.__exit__ = MagicMock(return_value=False)
        mock_open.return_value = doc_mock

        extrator = ExtratorPDF(max_paginas=10)
        with pytest.raises(PDFMuitoGrandeError):
            extrator.extrair_texto(pdf_fake)


def test_validar_pdf_arquivo_inexistente():
    extrator = ExtratorPDF()
    valido, msg = extrator.validar_pdf(Path("nao_existe.pdf"))
    assert valido is False
    assert msg is not None
