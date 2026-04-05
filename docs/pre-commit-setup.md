# Configuração do Pre-commit e Ruff

Este documento explica como o pre-commit e o Ruff estão configurados no projeto ConectaTalentos.

## O que é Pre-commit?

Pre-commit é uma ferramenta que executa verificações automáticas antes de cada commit Git. Isso garante que o código segue os padrões de qualidade antes de ser versionado.

## O que é Ruff?

Ruff é um linter e formatter Python extremamente rápido que substitui várias ferramentas (flake8, isort, pyupgrade, etc.) em uma única ferramenta.

## Configuração Atual

### Arquivos de Configuração

1. **`.pre-commit-config.yaml`**: Define quais hooks serão executados
2. **`ruff.toml`**: Configuração específica do Ruff

### Hooks Configurados

1. **Ruff Linter**: Verifica problemas de código e aplica correções automáticas
2. **Ruff Formatter**: Formata o código seguindo padrões Python
3. **Trailing Whitespace**: Remove espaços em branco no final das linhas
4. **End of File Fixer**: Garante que arquivos terminam com uma linha em branco
5. **Check YAML**: Valida sintaxe de arquivos YAML
6. **Check Large Files**: Previne commit de arquivos muito grandes
7. **Check Merge Conflict**: Detecta marcadores de conflito de merge

## Como Usar

### Instalação Inicial

Se você clonou o repositório pela primeira vez:

```bash
# Instalar dependências
pip install -r requirements.txt

# Instalar hooks do pre-commit
pre-commit install
```

### Uso Automático

Após a instalação, os hooks rodam automaticamente a cada `git commit`. Se houver problemas:

1. O commit será bloqueado
2. Correções automáticas serão aplicadas (quando possível)
3. Você verá uma mensagem indicando o que foi corrigido
4. Execute `git add .` novamente para adicionar as correções
5. Tente o commit novamente

### Uso Manual

Para executar os hooks manualmente sem fazer commit:

```bash
# Executar em todos os arquivos
pre-commit run --all-files

# Executar apenas no Ruff
pre-commit run ruff --all-files

# Executar apenas em arquivos staged
pre-commit run
```

### Executar Apenas o Ruff

Se você quiser usar apenas o Ruff diretamente:

```bash
# Verificar problemas
ruff check .

# Verificar e corrigir automaticamente
ruff check --fix .

# Formatar código
ruff format .

# Verificar arquivo específico
ruff check app/services/ranking_service.py
```

## Regras do Ruff

O Ruff está configurado para verificar:

- **E, W**: Erros e avisos do pycodestyle (PEP 8)
- **F**: Erros do pyflakes (imports não usados, variáveis indefinidas)
- **I**: Ordenação de imports (isort)
- **N**: Convenções de nomenclatura (PEP 8)
- **UP**: Sugestões de modernização (pyupgrade)
- **B**: Bugs comuns (flake8-bugbear)
- **C4**: Simplificação de comprehensions
- **SIM**: Simplificações de código

### Regras Ignoradas

- **E501**: Linha muito longa (tratado pelo formatter)
- **B008**: Chamadas de função em argumentos padrão (comum em FastAPI)

## Configuração do Ruff

```toml
# Target Python 3.11+
target-version = "py311"

# Comprimento máximo de linha
line-length = 88

# Diretórios excluídos
extend-exclude = [
    ".git", ".venv", "__pycache__",
    "*.egg-info", ".pytest_cache",
    "migrations"
]
```

## Desabilitar Temporariamente

### Desabilitar Pre-commit para um Commit

```bash
git commit --no-verify -m "mensagem"
```

**Atenção**: Use apenas em casos excepcionais!

### Desabilitar Regra Específica do Ruff

No código, adicione comentário:

```python
# ruff: noqa: E501
linha_muito_longa = "Esta linha é muito longa mas precisa ser assim por algum motivo específico"

# Desabilitar regra em bloco
# ruff: noqa
def funcao_com_problemas():
    pass
```

## Atualizar Hooks

Para atualizar os hooks para as versões mais recentes:

```bash
pre-commit autoupdate
```

## Troubleshooting

### Erro: "pre-commit command not found"

```bash
pip install pre-commit
pre-commit install
```

### Erro: "ruff command not found"

```bash
pip install ruff
```

### Hooks Muito Lentos

Na primeira execução, o pre-commit baixa e instala os ambientes. Execuções subsequentes são muito mais rápidas.

### Limpar Cache do Pre-commit

```bash
pre-commit clean
pre-commit install
```

## Integração com IDE

### VS Code

Instale a extensão "Ruff" e adicione ao `settings.json`:

```json
{
  "[python]": {
    "editor.defaultFormatter": "charliermarsh.ruff",
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
      "source.fixAll": true,
      "source.organizeImports": true
    }
  }
}
```

### PyCharm

1. Vá em Settings → Tools → External Tools
2. Adicione nova ferramenta:
   - Name: Ruff
   - Program: ruff
   - Arguments: check --fix $FilePath$
   - Working directory: $ProjectFileDir$

## Benefícios

1. **Consistência**: Todo código segue os mesmos padrões
2. **Qualidade**: Problemas são detectados antes do commit
3. **Velocidade**: Ruff é extremamente rápido (escrito em Rust)
4. **Automação**: Correções automáticas quando possível
5. **Prevenção**: Evita commits com código problemático

## Comandos Úteis

```bash
# Ver configuração do pre-commit
pre-commit --version

# Listar hooks instalados
pre-commit run --all-files --verbose

# Executar hook específico
pre-commit run ruff --all-files

# Pular hooks temporariamente
SKIP=ruff git commit -m "mensagem"

# Ver estatísticas do Ruff
ruff check --statistics .
```

## Referências

- [Pre-commit Documentation](https://pre-commit.com/)
- [Ruff Documentation](https://docs.astral.sh/ruff/)
- [Ruff Rules](https://docs.astral.sh/ruff/rules/)
