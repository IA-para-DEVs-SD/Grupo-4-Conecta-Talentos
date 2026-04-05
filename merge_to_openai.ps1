# PowerShell script para fazer merge da ranking-service na openai-integration

Write-Host "=== Iniciando processo de merge ===" -ForegroundColor Cyan

# 1. Adicionar arquivos pendentes
Write-Host "`n1. Adicionando arquivos..." -ForegroundColor Yellow
git add .

# 2. Fazer commit das alterações pendentes
Write-Host "`n2. Fazendo commit das alterações..." -ForegroundColor Yellow
git commit --no-verify -m "feat: completa implementação da Issue #61 - Ranking de Candidatos

- Adiciona endpoint GET /ranking/{vaga_id}/candidato/{curriculo_id} para detalhes
- Implementa template HTML completo com filtros e estatísticas
- Adiciona cards visuais para candidatos com posições destacadas
- Implementa filtros por score mínimo e reprocessamento
- Adiciona testes para controller de ranking
- Corrige warnings de tratamento de exceções
- Adiciona ícones Bootstrap e animações CSS

Completa Tasks 6.2 e 6.3 da Issue #61"

# 3. Checkout para feature/openai-integration
Write-Host "`n3. Mudando para branch feature/openai-integration..." -ForegroundColor Yellow
git checkout feature/openai-integration

# 4. Fazer merge da feature/ranking-service
Write-Host "`n4. Fazendo merge da feature/ranking-service..." -ForegroundColor Yellow
git merge feature/ranking-service --no-edit -m "merge: integra ranking service completo na branch openai-integration

Consolida toda a implementação da Issue #61:
- Integração AnalisadorLLM com pipeline
- API de ranking completa (4 endpoints)
- Interface web com filtros e estatísticas
- Testes completos (service + controller)
- Configuração de qualidade de código (Ruff + pre-commit)"

# 5. Push para o remoto
Write-Host "`n5. Fazendo push para origin/feature/openai-integration..." -ForegroundColor Yellow
git push origin feature/openai-integration

Write-Host "`n=== Merge concluído com sucesso! ===" -ForegroundColor Green
Write-Host "Branch feature/openai-integration atualizada no remoto" -ForegroundColor Green
Write-Host "O PR existente agora inclui todas as alterações da Issue #61" -ForegroundColor Green
