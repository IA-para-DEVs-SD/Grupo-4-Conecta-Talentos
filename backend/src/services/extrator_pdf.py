"""
Módulo de extração de texto de arquivos PDF.

Este módulo implementa a classe ExtratorPDF que converte documentos PDF
em texto estruturado, preservando a organização lógica do conteúdo.
"""

from pathlib import Path
from dataclasses import dataclass
from typing import Optional
import pymupdf


@dataclass
class TextoExtraido:
    """Resultado da extração de texto de um PDF.
    
    Attributes:
        conteudo: Texto completo extraído do PDF
        num_paginas: Número de páginas do documento
        tamanho_bytes: Tamanho do arquivo PDF em bytes
        sucesso: Indica se a extração foi bem-sucedida
    """
    conteudo: str
    num_paginas: int
    tamanho_bytes: int
    sucesso: bool = True


class PDFError(Exception):
    """Exceção base para erros relacionados a PDF."""
    pass


class PDFCorromidoError(PDFError):
    """Exceção lançada quando o PDF está corrompido ou ilegível."""
    pass


class PDFMuitoGrandeError(PDFError):
    """Exceção lançada quando o PDF excede o limite de páginas."""
    pass


class ExtratorPDF:
    """Extrator de texto de arquivos PDF.
    
    Esta classe é responsável por converter documentos PDF em texto estruturado,
    validando o arquivo e preservando a organização lógica do conteúdo.
    
    Attributes:
        max_paginas: Número máximo de páginas permitido (padrão: 10)
    
    Example:
        >>> extrator = ExtratorPDF(max_paginas=10)
        >>> resultado = extrator.extrair_texto(Path("curriculo.pdf"))
        >>> print(f"Extraídas {resultado.num_paginas} páginas")
        >>> print(resultado.conteudo)
    """
    
    def __init__(self, max_paginas: int = 10):
        """Inicializa o extrator de PDF.
        
        Args:
            max_paginas: Número máximo de páginas permitido para processamento
        """
        self.max_paginas = max_paginas
    
    def extrair_texto(self, pdf_path: Path) -> TextoExtraido:
        """Extrai texto de um arquivo PDF.
        
        Args:
            pdf_path: Caminho para o arquivo PDF
            
        Returns:
            TextoExtraido contendo o conteúdo extraído e metadados
            
        Raises:
            PDFCorromidoError: Se o PDF não pode ser aberto ou está corrompido
            PDFMuitoGrandeError: Se o PDF excede o limite de páginas
            
        Example:
            >>> extrator = ExtratorPDF()
            >>> resultado = extrator.extrair_texto(Path("exemplo.pdf"))
            >>> if resultado.sucesso:
            ...     print(resultado.conteudo)
        """
        # Validar se o arquivo existe
        if not pdf_path.exists():
            raise PDFCorromidoError(f"Arquivo não encontrado: {pdf_path}")
        
        # Tentar abrir o PDF
        try:
            doc = pymupdf.open(pdf_path)
        except Exception as e:
            raise PDFCorromidoError(f"Não foi possível abrir o PDF: {e}")
        
        try:
            # Validar número de páginas
            num_paginas = len(doc)
            
            if num_paginas > self.max_paginas:
                raise PDFMuitoGrandeError(
                    f"PDF tem {num_paginas} páginas, máximo permitido: {self.max_paginas}"
                )
            
            # Extrair texto de todas as páginas
            texto = self._extrair_texto_estruturado(doc)
            
            # Obter tamanho do arquivo
            tamanho = pdf_path.stat().st_size
            
            return TextoExtraido(
                conteudo=texto,
                num_paginas=num_paginas,
                tamanho_bytes=tamanho,
                sucesso=True
            )
        
        finally:
            # Garantir que o documento seja fechado
            doc.close()
    
    def _extrair_texto_estruturado(self, doc: pymupdf.Document) -> str:
        """Extrai texto preservando a estrutura do documento.
        
        Args:
            doc: Documento pymupdf aberto
            
        Returns:
            Texto extraído com estrutura preservada
        """
        paginas = []
        
        for num_pagina, page in enumerate(doc, start=1):
            # Extrair texto da página
            texto_pagina = page.get_text()
            
            # Adicionar separador de página (exceto na primeira)
            if num_pagina > 1:
                paginas.append(f"\n--- Página {num_pagina} ---\n")
            
            paginas.append(texto_pagina)
        
        return "".join(paginas)
    
    def validar_pdf(self, pdf_path: Path) -> tuple[bool, Optional[str]]:
        """Valida se um arquivo PDF pode ser processado.
        
        Args:
            pdf_path: Caminho para o arquivo PDF
            
        Returns:
            Tupla (válido, mensagem_erro)
            - válido: True se o PDF pode ser processado
            - mensagem_erro: Descrição do erro se inválido, None caso contrário
            
        Example:
            >>> extrator = ExtratorPDF()
            >>> valido, erro = extrator.validar_pdf(Path("teste.pdf"))
            >>> if not valido:
            ...     print(f"Erro: {erro}")
        """
        try:
            self.extrair_texto(pdf_path)
            return True, None
        except PDFCorromidoError as e:
            return False, str(e)
        except PDFMuitoGrandeError as e:
            return False, str(e)
        except Exception as e:
            return False, f"Erro inesperado: {e}"


# Função auxiliar para compatibilidade com o script original
def pdf_to_text(pdf_path: str) -> str:
    """Extrai todo o texto de um arquivo PDF (função legada).
    
    Args:
        pdf_path: Caminho para o arquivo PDF (string)
        
    Returns:
        Texto extraído do PDF
        
    Note:
        Esta função é mantida para compatibilidade com o código existente.
        Para novos desenvolvimentos, use a classe ExtratorPDF.
    """
    extrator = ExtratorPDF()
    resultado = extrator.extrair_texto(Path(pdf_path))
    return resultado.conteudo


if __name__ == "__main__":
    # Exemplo de uso
    import sys
    
    if len(sys.argv) < 2:
        print("Uso: python extrator_pdf.py <arquivo.pdf> [arquivo_saida.txt]")
        sys.exit(1)
    
    pdf_path = Path(sys.argv[1])
    
    # Criar extrator
    extrator = ExtratorPDF(max_paginas=10)
    
    try:
        # Extrair texto
        resultado = extrator.extrair_texto(pdf_path)
        
        print(f"✓ Extração bem-sucedida!")
        print(f"  Páginas: {resultado.num_paginas}")
        print(f"  Tamanho: {resultado.tamanho_bytes} bytes")
        print(f"  Caracteres: {len(resultado.conteudo)}")
        print()
        
        # Salvar ou exibir
        if len(sys.argv) >= 3:
            output_path = Path(sys.argv[2])
            output_path.write_text(resultado.conteudo, encoding="utf-8")
            print(f"✓ Texto salvo em: {output_path}")
        else:
            print("--- CONTEÚDO ---")
            print(resultado.conteudo)
    
    except PDFError as e:
        print(f"✗ Erro ao processar PDF: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"✗ Erro inesperado: {e}")
        sys.exit(1)
