# Como Usar a Classe ExtratorPDF

## Instalação Rápida

### 1. Instalar Dependência

```bash
pip install pymupdf
```

Ou usando o arquivo de requisitos:

```bash
pip install -r requirements-basico.txt
```

### 2. Testar a Classe

Execute o script de exemplo:

```bash
python exemplo_uso_extrator.py
```

Ou teste diretamente com o arquivo de exemplo:

```bash
python extrator_pdf.py exemplo.pdf
```

## Exemplos de Uso

### Exemplo 1: Uso Básico

```python
from pathlib import Path
from extrator_pdf import ExtratorPDF

# Criar extrator
extrator = ExtratorPDF(max_paginas=10)

# Extrair texto
resultado = extrator.extrair_texto(Path("exemplo.pdf"))

# Usar o resultado
print(f"Páginas: {resultado.num_paginas}")
print(f"Texto: {resultado.conteudo}")
```

### Exemplo 2: Com Tratamento de Erros

```python
from pathlib import Path
from extrator_pdf import ExtratorPDF, PDFError

extrator = ExtratorPDF()

try:
    resultado = extrator.extrair_texto(Path("curriculo.pdf"))
    print("✓ Sucesso!")
    print(resultado.conteudo)
except PDFError as e:
    print(f"✗ Erro: {e}")
```

### Exemplo 3: Validação Prévia

```python
from pathlib import Path
from extrator_pdf import ExtratorPDF

extrator = ExtratorPDF()
pdf_path = Path("curriculo.pdf")

# Validar antes de processar
valido, erro = extrator.validar_pdf(pdf_path)

if valido:
    resultado = extrator.extrair_texto(pdf_path)
    print("Processado com sucesso!")
else:
    print(f"PDF inválido: {erro}")
```

### Exemplo 4: Salvar Resultado em Arquivo

```python
from pathlib import Path
from extrator_pdf import ExtratorPDF

extrator = ExtratorPDF()
resultado = extrator.extrair_texto(Path("curriculo.pdf"))

# Salvar em arquivo de texto
output_path = Path("curriculo_extraido.txt")
output_path.write_text(resultado.conteudo, encoding="utf-8")
print(f"Salvo em: {output_path}")
```

## Testando com o Arquivo de Exemplo

O projeto já inclui um arquivo `exemplo.pdf` para testes:

```bash
# Exibir no terminal
python extrator_pdf.py exemplo.pdf

# Salvar em arquivo
python extrator_pdf.py exemplo.pdf saida.txt
```

## Características da Classe

✅ **Validação de Arquivo**: Verifica se o PDF existe e pode ser aberto  
✅ **Limite de Páginas**: Configura máximo de páginas (padrão: 10)  
✅ **Estrutura Preservada**: Mantém separadores de página  
✅ **Tratamento de Erros**: Exceções específicas para cada tipo de erro  
✅ **Metadados**: Retorna número de páginas e tamanho do arquivo  
✅ **Type Hints**: Código totalmente tipado para melhor IDE support  
✅ **Documentação**: Docstrings completas em todos os métodos  

## Erros Comuns e Soluções

### Erro: "ModuleNotFoundError: No module named 'pymupdf'"

**Solução**: Instale a dependência
```bash
pip install pymupdf
```

### Erro: "Arquivo não encontrado"

**Solução**: Verifique o caminho do arquivo
```python
from pathlib import Path

pdf_path = Path("curriculo.pdf")
if not pdf_path.exists():
    print(f"Arquivo não existe: {pdf_path.absolute()}")
```

### Erro: "PDF tem X páginas, máximo permitido: Y"

**Solução**: Aumente o limite de páginas
```python
extrator = ExtratorPDF(max_paginas=20)  # Aumentar limite
```

## Integração com o Projeto ConectaTalentos

A classe `ExtratorPDF` é o primeiro componente do pipeline:

```python
# Pipeline completo (simplificado)
from pathlib import Path
from extrator_pdf import ExtratorPDF

def processar_curriculo_completo(pdf_path: Path):
    # 1. Extrair texto
    extrator = ExtratorPDF()
    resultado = extrator.extrair_texto(pdf_path)
    texto = resultado.conteudo
    
    # 2. Anonimizar (próximo componente)
    # texto_anonimizado = anonimizador.anonimizar(texto)
    
    # 3. Analisar com LLM (próximo componente)
    # analise = analisador_llm.analisar(texto_anonimizado, vaga)
    
    return texto

# Usar
texto = processar_curriculo_completo(Path("curriculo.pdf"))
```

## Próximos Passos

Após dominar a classe `ExtratorPDF`, você pode:

1. Implementar a classe `Anonimizador` (Microsoft Presidio)
2. Implementar a classe `AnalisadorLLM` (OpenAI)
3. Criar a interface web com FastAPI
4. Adicionar testes automatizados

## Suporte

Para dúvidas ou problemas:
1. Consulte a documentação completa em `docs/classe-extrator-pdf.md`
2. Veja exemplos em `exemplo_uso_extrator.py`
3. Entre em contato com o Grupo 4

---

**ConectaTalentos - IA para Desenvolvedores**  
Grupo 4 - 2024
