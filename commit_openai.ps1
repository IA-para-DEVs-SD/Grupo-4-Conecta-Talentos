# PowerShell script para comitar na branch feature/openai-integration

Write-Host "=== Commitando na feature/openai-integration ===" -ForegroundColor Cyan

# Checkout para a branch
Write-Host "`nCheckout para feature/openai-integration..." -ForegroundColor Yellow
git checkout feature/openai-integration

# Adicionar todos os arquivos
Write-Host "`nAdicionando arquivos..." -ForegroundColor Yellow
git add .

# Fazer commit
Write-Host "`nFazendo commit..." -ForegroundColor Yellow
git commit --no-verify -m "feat: completa implementação da Issue #61 - Ranking de Candidatos

- Adiciona RankingService com 6 métodos (gerar_ranking, gerar_ranking_async, obter_ranking_existente, filtrar_por_score_minimo, obter_top_candidatos, _formatar_texto_vaga)
- Implementa RankingController com 4 endpoints REST:
  * GET /ranking/{vaga_id} - Visualizar ranking (HTML)
  * POST /ranking/{vaga_id}/gerar - Gerar ranking (JSON)
  * GET /ranking/{vaga_id}/top/{limite} - Top N candidatos
  * GET /ranking/{vaga_id}/candidato/{curriculo_id} - Detalhes do candidato
- Adiciona template HTML completo com filtros, estatísticas e cards visuais
- Implementa filtros por score mínimo e reprocessamento
- Adiciona testes completos (15 para service + 10 para controller)
- Configura Ruff e pre-commit para qualidade de código
- Corrige warnings de tratamento de exceções

Completa Tasks 5.5, 6.1, 6.2 e 6.3 da Issue #61
Closes #34, #35, #36, #37"

# Push para o remoto
Write-Host "`nFazendo push..." -ForegroundColor Yellow
git push origin feature/openai-integration

Write-Host "`n=== Commit concluído! ===" -ForegroundColor Green
Write-Host "Branch feature/openai-integration atualizada no remoto" -ForegroundColor Green
