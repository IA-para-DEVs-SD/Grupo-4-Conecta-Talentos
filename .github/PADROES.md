# Padrões do Projeto - Grupo 4

Este documento define os padrões e convenções adotados pelo Grupo 4 para o projeto ConectaTalentos.

---

## 📦 Nomenclatura de Repositórios

### Repositórios de Projetos
- **Formato:** `nome-grupo + nome-projeto`
- **Exemplo:** `grupo-4-conecta-talentos`
- **Regras:**
  - Apenas hífens como caracteres especiais
  - Texto sempre em minúsculas
  - Sem espaços ou underscores

### Repositórios de Atividades
- **Formato:** `nome-grupo + atividades + nome-aluno`
- **Exemplo:** `grupo-4-atividades-fulano-sobrenome`
- **Regras:**
  - Apenas hífens como caracteres especiais
  - Texto sempre em minúsculas
  - Sem espaços ou underscores

---

## 🌿 Padrão Gitflow

### Branches Principais

- **`main`** - Branch principal de produção
  - Contém código estável e testado
  - Apenas merges de `develop` ou hotfixes
  - Protegida contra commits diretos

- **`develop`** - Branch de desenvolvimento
  - Integração de novas funcionalidades
  - Base para criação de features
  - Código em desenvolvimento ativo

### Branches de Funcionalidades

- **Formato:** `feature/issue-xxx` ou `feature/nome-descritivo`
- **Exemplos:**
  - `feature/issue-001`
  - `feature/extrator-pdf`
  - `feature/anonimizacao-dados`
  - `feature/padronizacao-projeto`

### Fluxo de Trabalho

1. Criar branch a partir de `develop`:
   ```bash
   git checkout develop
   git pull origin develop
   git checkout -b feature/nome-funcionalidade
   ```

2. Desenvolver e commitar seguindo padrão semântico

3. Fazer push da branch:
   ```bash
   git push -u origin feature/nome-funcionalidade
   ```

4. Criar Pull Request para `develop`

5. Após aprovação, merge para `develop`

6. Periodicamente, `develop` é mergeada em `main`

---

## 💬 Padrão de Commit Semântico

### Formato

```
tipo: breve descrição

descrição mais detalhada (opcional)
```

### Tipos de Commit

| Tipo | Descrição | Exemplo |
|---|---|---|
| `feat` | Nova funcionalidade | `feat: adiciona extração de PDF` |
| `fix` | Correção de bug | `fix: corrige erro na leitura de PDF` |
| `docs` | Documentação | `docs: atualiza README com instruções` |
| `refactor` | Refatoração de código | `refactor: melhora estrutura do extrator` |
| `test` | Testes | `test: adiciona testes unitários do extrator` |
| `style` | Formatação de código | `style: formata código com black` |
| `chore` | Tarefas de manutenção | `chore: atualiza dependências` |
| `perf` | Melhorias de performance | `perf: otimiza processamento de PDF` |

### Exemplos de Commits

```bash
# Commit simples
git commit -m "feat: adiciona classe ExtratorPDF"

# Commit com descrição detalhada
git commit -m "feat: adiciona anonimização de dados

Implementa anonimização usando Microsoft Presidio
- Remove nomes, CPF, endereços
- Mantém informações profissionais
- Conforme LGPD"

# Outros exemplos
git commit -m "docs: cria documentação de requisitos"
git commit -m "fix: corrige validação de arquivo PDF"
git commit -m "refactor: reorganiza estrutura de pastas"
git commit -m "test: adiciona testes de integração"
```

### Boas Práticas

- Use verbos no imperativo: "adiciona" não "adicionado"
- Primeira linha com no máximo 50 caracteres
- Descrição detalhada com no máximo 72 caracteres por linha
- Commits pequenos e focados em uma única mudança
- Mensagens claras e descritivas

---

## 📋 Nomenclatura de Boards/Projetos

### Formato
- **Padrão:** `Identificação do Grupo + Nome do Projeto`
- **Exemplo:** `Grupo 4 - ConectaTalentos`

### Aplicação
- GitHub Projects
- Trello
- Jira
- Outras ferramentas de gerenciamento

---

## 📄 Estrutura do README

Todo README deve conter os seguintes tópicos na ordem:

1. **Nome do Projeto**
   - Título principal com identificação do grupo

2. **Descrição do Projeto**
   - Breve descrição do que o projeto faz
   - Objetivo principal

3. **Sumário de Documentações**
   - Links para documentos importantes
   - Guias e manuais

4. **Tecnologias Utilizadas**
   - Lista de tecnologias e versões
   - Propósito de cada tecnologia

5. **Instruções de Instalação/Uso**
   - Pré-requisitos
   - Passo a passo de instalação
   - Como executar o projeto
   - Exemplos de uso

6. **Integrantes do Grupo**
   - Lista completa dos membros
   - Informações de contato (opcional)

### Seções Opcionais

- Estrutura do Projeto
- Testes
- Solução de Problemas
- Roadmap
- Contribuindo
- Licença

---

## 📁 Estrutura de Pastas

```
grupo-4-conecta-talentos/
├── .github/                    # Configurações GitHub
│   ├── workflows/              # GitHub Actions
│   ├── PADROES.md             # Este documento
│   └── CONTRIBUTING.md        # Guia de contribuição
├── .kiro/                     # Especificações e configurações
│   └── specs/                 # Documentos de requisitos e design
├── backend/                   # Código backend
│   ├── src/                   # Código-fonte
│   ├── tests/                 # Testes automatizados
│   ├── docs/                  # Documentação técnica
│   └── requirements.txt       # Dependências Python
├── frontend/                  # Código frontend (futuro)
├── scripts/                   # Scripts utilitários
├── .gitignore                # Arquivos ignorados pelo Git
└── README.md                 # Documentação principal
```

---

## 🔍 Code Review

### Checklist para Pull Requests

- [ ] Código segue os padrões do projeto
- [ ] Commits seguem padrão semântico
- [ ] Testes foram adicionados/atualizados
- [ ] Documentação foi atualizada
- [ ] Código foi testado localmente
- [ ] Não há conflitos com `develop`
- [ ] Descrição clara do que foi implementado

### Processo de Revisão

1. Pelo menos 1 aprovação necessária
2. Todos os comentários devem ser resolvidos
3. CI/CD deve passar (quando implementado)
4. Merge apenas pelo responsável da feature

---

## 🧪 Padrões de Teste

### Nomenclatura de Arquivos de Teste

- **Formato:** `test_nome_modulo.py`
- **Exemplo:** `test_extrator_pdf.py`

### Nomenclatura de Funções de Teste

- **Formato:** `test_comportamento_esperado`
- **Exemplos:**
  - `test_extrai_texto_pdf_valido()`
  - `test_retorna_erro_pdf_invalido()`
  - `test_respeita_limite_paginas()`

---

## 📝 Documentação de Código

### Docstrings Python

```python
def extrair_texto(self, caminho_pdf: Path) -> ResultadoExtracao:
    """
    Extrai texto de um arquivo PDF.
    
    Args:
        caminho_pdf: Caminho para o arquivo PDF
        
    Returns:
        ResultadoExtracao com texto extraído e metadados
        
    Raises:
        ArquivoNaoEncontradoError: Se o arquivo não existir
        PDFInvalidoError: Se o arquivo não for um PDF válido
        LimitePaginasExcedidoError: Se exceder o limite de páginas
    """
```

### Comentários

- Use comentários para explicar "por quê", não "o quê"
- Evite comentários óbvios
- Mantenha comentários atualizados com o código

---

## 🎯 Convenções de Código Python

### Formatação

- Usar **Black** para formatação automática
- Linha máxima: 88 caracteres (padrão Black)
- Indentação: 4 espaços

### Nomenclatura

- **Classes:** `PascalCase` - `ExtratorPDF`, `AnalisadorLLM`
- **Funções/Métodos:** `snake_case` - `extrair_texto()`, `processar_curriculo()`
- **Variáveis:** `snake_case` - `caminho_pdf`, `resultado_extracao`
- **Constantes:** `UPPER_SNAKE_CASE` - `MAX_PAGINAS`, `TIMEOUT_SEGUNDOS`
- **Privados:** prefixo `_` - `_validar_arquivo()`, `_processar_interno()`

### Imports

```python
# Bibliotecas padrão
import os
from pathlib import Path

# Bibliotecas de terceiros
import pymupdf

# Módulos locais
from .models import ResultadoExtracao
```

---

## 🔒 Segurança e Boas Práticas

- Nunca commitar credenciais ou chaves de API
- Usar variáveis de ambiente para configurações sensíveis
- Manter `.env.example` atualizado sem valores reais
- Validar todas as entradas de usuário
- Tratar erros adequadamente
- Seguir princípios SOLID
- Escrever código testável

---

## 📞 Contato e Suporte

Para dúvidas sobre os padrões do projeto, entre em contato com qualquer membro do Grupo 4.

---

**Última atualização:** 25/03/2026
**Versão:** 1.0
