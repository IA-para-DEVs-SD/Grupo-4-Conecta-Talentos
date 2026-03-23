"""
Exemplo de uso da classe ExtratorPDF.

Este script demonstra como usar a classe ExtratorPDF para extrair
texto de arquivos PDF no projeto ConectaTalentos.
"""

from pathlib import Path
from extrator_pdf import ExtratorPDF, PDFError


def exemplo_basico():
    """Exemplo básico de extração de texto."""
    print("=== Exemplo 1: Extração Básica ===\n")
    
    # Criar instância do extrator
    extrator = ExtratorPDF(max_paginas=10)
    
    # Extrair texto do arquivo de exemplo
    pdf_path = Path("exemplo.pdf")
    
    try:
        resultado = extrator.extrair_texto(pdf_path)
        
        print(f"✓ Extração bem-sucedida!")
        print(f"  Arquivo: {pdf_path}")
        print(f"  Páginas: {resultado.num_paginas}")
        print(f"  Tamanho: {resultado.tamanho_bytes} bytes")
        print(f"  Caracteres extraídos: {len(resultado.conteudo)}")
        print(f"\nPrimeiros 200 caracteres:")
        print(resultado.conteudo[:200])
        print("...\n")
        
    except PDFError as e:
        print(f"✗ Erro: {e}\n")


def exemplo_validacao():
    """Exemplo de validação de PDF antes de processar."""
    print("=== Exemplo 2: Validação de PDF ===\n")
    
    extrator = ExtratorPDF(max_paginas=10)
    pdf_path = Path("exemplo.pdf")
    
    # Validar antes de processar
    valido, erro = extrator.validar_pdf(pdf_path)
    
    if valido:
        print(f"✓ PDF válido: {pdf_path}")
        print("  O arquivo pode ser processado com segurança.\n")
    else:
        print(f"✗ PDF inválido: {pdf_path}")
        print(f"  Erro: {erro}\n")


def exemplo_tratamento_erros():
    """Exemplo de tratamento de diferentes tipos de erro."""
    print("=== Exemplo 3: Tratamento de Erros ===\n")
    
    extrator = ExtratorPDF(max_paginas=5)  # Limite reduzido para demonstração
    
    # Testar arquivo inexistente
    print("Testando arquivo inexistente...")
    try:
        extrator.extrair_texto(Path("nao_existe.pdf"))
    except PDFError as e:
        print(f"  ✓ Erro capturado corretamente: {e}\n")
    
    # Testar arquivo válido
    print("Testando arquivo válido...")
    try:
        resultado = extrator.extrair_texto(Path("exemplo.pdf"))
        print(f"  ✓ Arquivo processado: {resultado.num_paginas} páginas\n")
    except PDFError as e:
        print(f"  ✗ Erro: {e}\n")


def exemplo_uso_em_pipeline():
    """Exemplo de uso no pipeline do ConectaTalentos."""
    print("=== Exemplo 4: Pipeline ConectaTalentos ===\n")
    
    # Simular processamento de currículo
    extrator = ExtratorPDF(max_paginas=10)
    curriculo_path = Path("exemplo.pdf")
    
    print(f"Processando currículo: {curriculo_path}")
    
    try:
        # Passo 1: Extrair texto
        print("  [1/3] Extraindo texto do PDF...")
        resultado = extrator.extrair_texto(curriculo_path)
        print(f"        ✓ {len(resultado.conteudo)} caracteres extraídos")
        
        # Passo 2: Simular anonimização (próximo componente)
        print("  [2/3] Anonimizando dados sensíveis...")
        print("        ✓ Dados anonimizados (simulado)")
        
        # Passo 3: Simular análise LLM (próximo componente)
        print("  [3/3] Analisando com LLM...")
        print("        ✓ Análise concluída (simulado)")
        
        print(f"\n✓ Pipeline completo! Currículo processado com sucesso.\n")
        
    except PDFError as e:
        print(f"\n✗ Falha no pipeline: {e}\n")


def main():
    """Executa todos os exemplos."""
    print("\n" + "="*60)
    print("  EXEMPLOS DE USO - ExtratorPDF")
    print("  ConectaTalentos - IA para Devs")
    print("="*60 + "\n")
    
    exemplo_basico()
    exemplo_validacao()
    exemplo_tratamento_erros()
    exemplo_uso_em_pipeline()
    
    print("="*60)
    print("  Exemplos concluídos!")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
