"""Converte arquivos PDF em texto."""

import sys
from pathlib import Path

try:
    import pymupdf
except ImportError:
    print("Instale a dependência: pip install pymupdf")
    sys.exit(1)


def pdf_to_text(pdf_path: str) -> str:
    """Extrai todo o texto de um arquivo PDF."""
    doc = pymupdf.open(pdf_path)
    text = "\n".join(page.get_text() for page in doc)
    doc.close()
    return text


def main():
    if len(sys.argv) < 2:
        print("Uso: python pdf_to_text.py <arquivo.pdf> [arquivo_saida.txt]")
        sys.exit(1)

    pdf_path = sys.argv[1]

    if not Path(pdf_path).exists():
        print(f"Arquivo não encontrado: {pdf_path}")
        sys.exit(1)

    text = pdf_to_text(pdf_path)

    if len(sys.argv) >= 3:
        output_path = sys.argv[2]
        Path(output_path).write_text(text, encoding="utf-8")
        print(f"Texto salvo em: {output_path}")
    else:
        print(text)


if __name__ == "__main__":
    main()