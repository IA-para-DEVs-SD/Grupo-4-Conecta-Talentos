#!/bin/bash
# Script para fazer commit das alterações

git add .

git commit --no-verify -m "feat: completa implementação da Issue #61 - Ranking de Candidatos

- Adiciona endpoint GET /ranking/{vaga_id}/candidato/{curriculo_id} para detalhes
- Implementa template HTML completo com filtros e estatísticas
- Adiciona cards visuais para candidatos com posições destacadas
- Implementa filtros por score mínimo e reprocessamento
- Adiciona testes para controller de ranking
- Corrige warnings de tratamento de exceções
- Adiciona ícones Bootstrap e animações CSS

Completa Tasks 6.2 e 6.3 da Issue #61"

echo "Commit realizado com sucesso!"
