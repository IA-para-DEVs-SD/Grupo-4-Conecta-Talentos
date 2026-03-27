# Scripts de Automação - ConectaTalentos

Este diretório contém scripts para automatizar tarefas do projeto.

## 📋 github-tasks.md

Documento completo com todas as 41 tasks do projeto, organizadas por Epic.

**Conteúdo:**
- Descrição detalhada de cada task
- Acceptance criteria
- Labels sugeridas
- Estimativas em pontos
- Priorização por sprints
- Resumo de estimativas

**Como usar:**
1. Abra o arquivo `github-tasks.md`
2. Copie cada task
3. Crie manualmente no GitHub Projects: https://github.com/orgs/IA-para-DEVs-SD/projects/22

---

## 🤖 create-github-issues.sh (Linux/Mac)

Script bash para criar issues automaticamente usando GitHub CLI.

### Pré-requisitos

1. Instalar GitHub CLI:
```bash
# Mac
brew install gh

# Linux (Debian/Ubuntu)
sudo apt install gh

# Linux (Fedora)
sudo dnf install gh
```

2. Autenticar:
```bash
gh auth login
```

### Como usar

```bash
# Dar permissão de execução
chmod +x scripts/create-github-issues.sh

# Executar
./scripts/create-github-issues.sh
```

---

## 🤖 create-github-issues.ps1 (Windows)

Script PowerShell para criar issues automaticamente usando GitHub CLI.

### Pré-requisitos

1. Instalar GitHub CLI:
```powershell
# Usando winget
winget install --id GitHub.cli

# Ou baixar de: https://cli.github.com/
```

2. Autenticar:
```powershell
gh auth login
```

### Como usar

```powershell
# Executar
.\scripts\create-github-issues.ps1
```

---

## 📊 Estrutura das Issues

Cada issue criada contém:

- **Título:** `[Epic X] Task X.Y: Nome da task`
- **Descrição:** Descrição detalhada da task
- **Acceptance Criteria:** Lista de critérios de aceitação
- **Estimativa:** Pontos de story points
- **Labels:** Tags para categorização (backend, frontend, api, etc.)

### Labels Utilizadas

| Label | Descrição |
|-------|-----------|
| `backend` | Tarefas de backend |
| `frontend` | Tarefas de frontend |
| `api` | Desenvolvimento de APIs |
| `database` | Banco de dados |
| `ai` | Inteligência Artificial |
| `lgpd` | Conformidade LGPD |
| `testing` | Testes |
| `documentation` | Documentação |
| `feature` | Nova funcionalidade |
| `setup` | Configuração inicial |
| `integration` | Integração de componentes |

---

## 📈 Resumo do Projeto

- **Total de Tasks:** 41
- **Total de Pontos:** 203
- **Epics:** 11
- **Sprints Sugeridos:** 6

### Distribuição por Epic

| Epic | Tasks | Pontos |
|------|-------|--------|
| Cadastro de Vagas | 5 | 19 |
| Upload e Armazenamento | 4 | 18 |
| Extração de Texto | 2 | 13 |
| Anonimização | 3 | 16 |
| Análise por IA | 5 | 32 |
| Visualização | 3 | 16 |
| Interface Web | 4 | 14 |
| Persistência | 4 | 23 |
| Tratamento de Erros | 5 | 17 |
| Testes | 3 | 24 |
| Documentação | 3 | 11 |

---

## 🎯 Priorização Sugerida

### Sprint 1 - Fundação (34 pontos)
Configuração inicial, banco de dados, cadastro de vagas

### Sprint 2 - Upload e Processamento (31 pontos)
Upload de currículos, validação, extração de texto

### Sprint 3 - Anonimização e IA (37 pontos)
Anonimização LGPD, integração com OpenAI, análise de currículos

### Sprint 4 - Visualização e Ranking (29 pontos)
Ranking de candidatos, interface de visualização

### Sprint 5 - Refinamento e Qualidade (42 pontos)
Tratamento de erros, testes, melhorias

### Sprint 6 - Finalização (30 pontos)
Testes E2E, documentação, ajustes finais

---

## 🔧 Troubleshooting

### Erro: "gh: command not found"
**Solução:** Instale o GitHub CLI seguindo as instruções acima

### Erro: "authentication required"
**Solução:** Execute `gh auth login` e siga as instruções

### Erro: "permission denied"
**Solução (Linux/Mac):** Execute `chmod +x scripts/create-github-issues.sh`

### Issues não aparecem no Project
**Solução:** Adicione manualmente as issues ao project board após criação

---

## 📝 Notas

- Os scripts criam apenas as issues no repositório
- Você precisará adicionar as issues ao Project Board manualmente
- Ajuste as labels conforme necessário no seu repositório
- Revise as estimativas com a equipe antes de iniciar

---

## 🤝 Contribuindo

Para adicionar novos scripts:

1. Crie o script neste diretório
2. Documente no README
3. Adicione exemplos de uso
4. Teste antes de commitar

---

**Última atualização:** 25/03/2026
