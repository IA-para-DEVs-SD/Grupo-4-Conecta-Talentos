#!/bin/bash
# Script para fazer merge da branch ranking-service na openai-integration

# Checkout para feature/openai-integration
git checkout feature/openai-integration

# Merge da feature/ranking-service
git merge feature/ranking-service --no-edit

# Push das alterações
git push origin feature/openai-integration

echo "Merge concluído com sucesso!"
