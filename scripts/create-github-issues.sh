#!/bin/bash

# Script para criar issues no GitHub Projects
# Requer: GitHub CLI (gh) instalado e autenticado
# Uso: ./create-github-issues.sh

REPO="IA-para-DEVs-SD/Conecta-Talentos-Grupo4"
PROJECT_NUMBER=22

echo "🚀 Criando issues para o projeto ConectaTalentos..."
echo "📋 Repositório: $REPO"
echo "📊 Project: #$PROJECT_NUMBER"
echo ""

# Epic 1: Cadastro de Vagas
echo "📦 Epic 1: Cadastro de Vagas"

gh issue create --repo $REPO \
  --title "[Epic 1] Task 1.1: Criar modelo de dados para Vaga" \
  --body "**Descrição:**
Implementar modelo de dados para armazenar informações de vagas.

**Acceptance Criteria:**
- [ ] Modelo contém campos: título, descrição, requisitos técnicos, experiência mínima, competências desejadas
- [ ] Validação de campos obrigatórios implementada
- [ ] Testes unitários criados

**Estimativa:** 3 pontos" \
  --label "backend,database,model"

gh issue create --repo $REPO \
  --title "[Epic 1] Task 1.2: Implementar API de cadastro de vagas" \
  --body "**Descrição:**
Criar endpoint REST para cadastro de novas vagas.

**Acceptance Criteria:**
- [ ] Endpoint POST /vagas criado
- [ ] Validação de dados implementada
- [ ] Retorna erro descritivo para dados inválidos
- [ ] Testes de integração criados

**Estimativa:** 5 pontos" \
  --label "backend,api,feature"

gh issue create --repo $REPO \
  --title "[Epic 1] Task 1.3: Implementar API de edição de vagas" \
  --body "**Descrição:**
Criar endpoint REST para editar vagas existentes.

**Acceptance Criteria:**
- [ ] Endpoint PUT /vagas/{id} criado
- [ ] Validação de dados implementada
- [ ] Retorna 404 se vaga não existe
- [ ] Testes de integração criados

**Estimativa:** 3 pontos" \
  --label "backend,api,feature"

gh issue create --repo $REPO \
  --title "[Epic 1] Task 1.4: Implementar API de listagem de vagas" \
  --body "**Descrição:**
Criar endpoint REST para listar todas as vagas cadastradas.

**Acceptance Criteria:**
- [ ] Endpoint GET /vagas criado
- [ ] Retorna lista completa de vagas
- [ ] Suporta paginação
- [ ] Testes de integração criados

**Estimativa:** 3 pontos" \
  --label "backend,api,feature"

gh issue create --repo $REPO \
  --title "[Epic 1] Task 1.5: Criar interface de cadastro de vagas" \
  --body "**Descrição:**
Implementar tela web para cadastro de vagas.

**Acceptance Criteria:**
- [ ] Formulário com todos os campos necessários
- [ ] Validação de campos no frontend
- [ ] Feedback visual de sucesso/erro
- [ ] Design responsivo

**Estimativa:** 5 pontos" \
  --label "frontend,ui,feature"

# Epic 2: Upload e Armazenamento
echo "📦 Epic 2: Upload e Armazenamento de Currículos"

gh issue create --repo $REPO \
  --title "[Epic 2] Task 2.1: Implementar validação de arquivo PDF" \
  --body "**Descrição:**
Criar função para validar se arquivo enviado é PDF válido.

**Acceptance Criteria:**
- [ ] Valida extensão do arquivo
- [ ] Valida magic number do PDF
- [ ] Retorna erro descritivo para arquivos inválidos
- [ ] Testes unitários criados

**Estimativa:** 3 pontos" \
  --label "backend,validation,feature"

gh issue create --repo $REPO \
  --title "[Epic 2] Task 2.2: Implementar armazenamento de PDFs" \
  --body "**Descrição:**
Criar sistema de armazenamento de arquivos PDF.

**Acceptance Criteria:**
- [ ] PDFs salvos em diretório estruturado
- [ ] Nome de arquivo único gerado
- [ ] Metadados do arquivo armazenados no banco
- [ ] Testes de integração criados

**Estimativa:** 5 pontos" \
  --label "backend,storage,feature"

gh issue create --repo $REPO \
  --title "[Epic 2] Task 2.3: Implementar API de upload de currículos" \
  --body "**Descrição:**
Criar endpoint REST para upload de currículos.

**Acceptance Criteria:**
- [ ] Endpoint POST /vagas/{id}/curriculos criado
- [ ] Valida formato PDF
- [ ] Associa currículo à vaga
- [ ] Suporta múltiplos uploads
- [ ] Testes de integração criados

**Estimativa:** 5 pontos" \
  --label "backend,api,feature"

gh issue create --repo $REPO \
  --title "[Epic 2] Task 2.4: Criar interface de upload de currículos" \
  --body "**Descrição:**
Implementar tela web para upload de currículos.

**Acceptance Criteria:**
- [ ] Drag and drop de arquivos
- [ ] Validação de formato no frontend
- [ ] Barra de progresso de upload
- [ ] Feedback visual de sucesso/erro
- [ ] Suporta múltiplos arquivos

**Estimativa:** 5 pontos" \
  --label "frontend,ui,feature"

# Epic 3: Extração de Texto
echo "📦 Epic 3: Extração de Texto de Currículos"

gh issue create --repo $REPO \
  --title "[Epic 3] Task 3.2: Integrar ExtratorPDF com pipeline" \
  --body "**Descrição:**
Integrar extração de PDF no fluxo de processamento de currículos.

**Acceptance Criteria:**
- [ ] Extração executada automaticamente após upload
- [ ] Texto extraído armazenado no banco
- [ ] Erros tratados adequadamente
- [ ] Testes de integração criados

**Estimativa:** 5 pontos
**Nota:** Task 3.1 já foi concluída" \
  --label "backend,integration,feature"

# Epic 4: Anonimização
echo "📦 Epic 4: Anonimização de Dados Sensíveis"

gh issue create --repo $REPO \
  --title "[Epic 4] Task 4.1: Configurar Microsoft Presidio" \
  --body "**Descrição:**
Instalar e configurar Microsoft Presidio para anonimização.

**Acceptance Criteria:**
- [ ] Presidio instalado e configurado
- [ ] Reconhecedores de entidades em português configurados
- [ ] Testes de reconhecimento criados

**Estimativa:** 5 pontos" \
  --label "backend,lgpd,setup"

gh issue create --repo $REPO \
  --title "[Epic 4] Task 4.2: Implementar classe Anonimizador" \
  --body "**Descrição:**
Criar classe para anonimizar dados sensíveis usando Presidio.

**Acceptance Criteria:**
- [ ] Identifica e substitui nomes por [NOME]
- [ ] Identifica e substitui CPF por [CPF]
- [ ] Identifica e substitui endereços por [ENDEREÇO]
- [ ] Identifica e substitui telefones por [TELEFONE]
- [ ] Identifica e substitui emails por [EMAIL]
- [ ] Preserva informações profissionais
- [ ] Testes unitários criados

**Estimativa:** 8 pontos" \
  --label "backend,lgpd,feature"

gh issue create --repo $REPO \
  --title "[Epic 4] Task 4.3: Integrar Anonimizador com pipeline" \
  --body "**Descrição:**
Integrar anonimização no fluxo de processamento de currículos.

**Acceptance Criteria:**
- [ ] Anonimização executada após extração de texto
- [ ] Texto anonimizado armazenado no banco
- [ ] Erros tratados adequadamente
- [ ] Testes de integração criados

**Estimativa:** 3 pontos" \
  --label "backend,integration,feature"

# Epic 5: Análise por IA
echo "📦 Epic 5: Análise e Ranqueamento por IA"

gh issue create --repo $REPO \
  --title "[Epic 5] Task 5.1: Configurar integração com OpenAI API" \
  --body "**Descrição:**
Configurar credenciais e cliente para OpenAI API.

**Acceptance Criteria:**
- [ ] Variáveis de ambiente configuradas
- [ ] Cliente OpenAI inicializado
- [ ] Tratamento de erros de API implementado
- [ ] Testes de conexão criados

**Estimativa:** 3 pontos" \
  --label "backend,ai,setup"

gh issue create --repo $REPO \
  --title "[Epic 5] Task 5.2: Implementar otimização de prompt" \
  --body "**Descrição:**
Criar função para otimizar prompt e minimizar tokens.

**Acceptance Criteria:**
- [ ] Extrai apenas informações essenciais da vaga
- [ ] Extrai apenas seções relevantes do currículo
- [ ] Remove texto redundante
- [ ] Estrutura em formato JSON
- [ ] Resume currículos longos (>2000 tokens)
- [ ] Testes unitários criados

**Estimativa:** 8 pontos" \
  --label "backend,ai,optimization"

gh issue create --repo $REPO \
  --title "[Epic 5] Task 5.3: Implementar classe AnalisadorLLM" \
  --body "**Descrição:**
Criar classe para análise e ranqueamento de candidatos usando LLM.

**Acceptance Criteria:**
- [ ] Compara perfil do candidato com requisitos da vaga
- [ ] Atribui score de 0 a 100
- [ ] Gera justificativa textual
- [ ] Identifica pontos fortes
- [ ] Identifica gaps (lacunas)
- [ ] Testes unitários criados

**Estimativa:** 13 pontos" \
  --label "backend,ai,feature"

gh issue create --repo $REPO \
  --title "[Epic 5] Task 5.4: Implementar geração de ranking" \
  --body "**Descrição:**
Criar função para gerar ranking ordenado de candidatos.

**Acceptance Criteria:**
- [ ] Ordena candidatos por score decrescente
- [ ] Armazena ranking no banco
- [ ] Testes unitários criados

**Estimativa:** 3 pontos" \
  --label "backend,feature"

gh issue create --repo $REPO \
  --title "[Epic 5] Task 5.5: Integrar AnalisadorLLM com pipeline" \
  --body "**Descrição:**
Integrar análise por IA no fluxo de processamento.

**Acceptance Criteria:**
- [ ] Análise executada após anonimização
- [ ] Resultados armazenados no banco
- [ ] Erros tratados adequadamente
- [ ] Testes de integração criados

**Estimativa:** 5 pontos" \
  --label "backend,integration,feature"

echo ""
echo "✅ Issues criadas com sucesso!"
echo "📊 Acesse o projeto em: https://github.com/orgs/IA-para-DEVs-SD/projects/$PROJECT_NUMBER"
