# Script para criar issues no GitHub Projects
# Requer: GitHub CLI (gh) instalado e autenticado
# Uso: .\create-github-issues.ps1

$REPO = "IA-para-DEVs-SD/Conecta-Talentos-Grupo4"
$PROJECT_NUMBER = 22

Write-Host "🚀 Criando issues para o projeto ConectaTalentos..." -ForegroundColor Green
Write-Host "📋 Repositório: $REPO" -ForegroundColor Cyan
Write-Host "📊 Project: #$PROJECT_NUMBER" -ForegroundColor Cyan
Write-Host ""

# Função para criar issue
function Create-Issue {
    param(
        [string]$Title,
        [string]$Body,
        [string]$Labels
    )
    
    gh issue create --repo $REPO --title $Title --body $Body --label $Labels
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ $Title" -ForegroundColor Green
    } else {
        Write-Host "✗ Erro ao criar: $Title" -ForegroundColor Red
    }
}

# Epic 1: Cadastro de Vagas
Write-Host "📦 Epic 1: Cadastro de Vagas" -ForegroundColor Yellow

Create-Issue `
    -Title "[Epic 1] Task 1.1: Criar modelo de dados para Vaga" `
    -Body @"
**Descrição:**
Implementar modelo de dados para armazenar informações de vagas.

**Acceptance Criteria:**
- [ ] Modelo contém campos: título, descrição, requisitos técnicos, experiência mínima, competências desejadas
- [ ] Validação de campos obrigatórios implementada
- [ ] Testes unitários criados

**Estimativa:** 3 pontos
"@ `
    -Labels "backend,database,model"

Create-Issue `
    -Title "[Epic 1] Task 1.2: Implementar API de cadastro de vagas" `
    -Body @"
**Descrição:**
Criar endpoint REST para cadastro de novas vagas.

**Acceptance Criteria:**
- [ ] Endpoint POST /vagas criado
- [ ] Validação de dados implementada
- [ ] Retorna erro descritivo para dados inválidos
- [ ] Testes de integração criados

**Estimativa:** 5 pontos
"@ `
    -Labels "backend,api,feature"

Write-Host ""
Write-Host "✅ Processo concluído!" -ForegroundColor Green
Write-Host "📊 Acesse o projeto em: https://github.com/orgs/IA-para-DEVs-SD/projects/$PROJECT_NUMBER" -ForegroundColor Cyan
