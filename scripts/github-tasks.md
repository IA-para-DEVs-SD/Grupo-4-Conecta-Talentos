# Tasks para GitHub Projects - ConectaTalentos

## Instruções
Copie cada task abaixo e crie como uma Issue no GitHub Projects: https://github.com/orgs/IA-para-DEVs-SD/projects/22

---

## Epic 1: Cadastro de Vagas

### Task 1.1: Criar modelo de dados para Vaga
**Descrição:**
Implementar modelo de dados para armazenar informações de vagas.

**Acceptance Criteria:**
- [ ] Modelo contém campos: título, descrição, requisitos técnicos, experiência mínima, competências desejadas
- [ ] Validação de campos obrigatórios implementada
- [ ] Testes unitários criados

**Labels:** `backend`, `database`, `model`
**Estimativa:** 3 pontos

---

### Task 1.2: Implementar API de cadastro de vagas
**Descrição:**
Criar endpoint REST para cadastro de novas vagas.

**Acceptance Criteria:**
- [ ] Endpoint POST /vagas criado
- [ ] Validação de dados implementada
- [ ] Retorna erro descritivo para dados inválidos
- [ ] Testes de integração criados

**Labels:** `backend`, `api`, `feature`
**Estimativa:** 5 pontos

---

### Task 1.3: Implementar API de edição de vagas
**Descrição:**
Criar endpoint REST para editar vagas existentes.

**Acceptance Criteria:**
- [ ] Endpoint PUT /vagas/{id} criado
- [ ] Validação de dados implementada
- [ ] Retorna 404 se vaga não existe
- [ ] Testes de integração criados

**Labels:** `backend`, `api`, `feature`
**Estimativa:** 3 pontos

---

### Task 1.4: Implementar API de listagem de vagas
**Descrição:**
Criar endpoint REST para listar todas as vagas cadastradas.

**Acceptance Criteria:**
- [ ] Endpoint GET /vagas criado
- [ ] Retorna lista completa de vagas
- [ ] Suporta paginação
- [ ] Testes de integração criados

**Labels:** `backend`, `api`, `feature`
**Estimativa:** 3 pontos

---

### Task 1.5: Criar interface de cadastro de vagas
**Descrição:**
Implementar tela web para cadastro de vagas.

**Acceptance Criteria:**
- [ ] Formulário com todos os campos necessários
- [ ] Validação de campos no frontend
- [ ] Feedback visual de sucesso/erro
- [ ] Design responsivo

**Labels:** `frontend`, `ui`, `feature`
**Estimativa:** 5 pontos

---

## Epic 2: Upload e Armazenamento de Currículos

### Task 2.1: Implementar validação de arquivo PDF
**Descrição:**
Criar função para validar se arquivo enviado é PDF válido.

**Acceptance Criteria:**
- [ ] Valida extensão do arquivo
- [ ] Valida magic number do PDF
- [ ] Retorna erro descritivo para arquivos inválidos
- [ ] Testes unitários criados

**Labels:** `backend`, `validation`, `feature`
**Estimativa:** 3 pontos

---

### Task 2.2: Implementar armazenamento de PDFs
**Descrição:**
Criar sistema de armazenamento de arquivos PDF.

**Acceptance Criteria:**
- [ ] PDFs salvos em diretório estruturado
- [ ] Nome de arquivo único gerado
- [ ] Metadados do arquivo armazenados no banco
- [ ] Testes de integração criados

**Labels:** `backend`, `storage`, `feature`
**Estimativa:** 5 pontos

---

### Task 2.3: Implementar API de upload de currículos
**Descrição:**
Criar endpoint REST para upload de currículos.

**Acceptance Criteria:**
- [ ] Endpoint POST /vagas/{id}/curriculos criado
- [ ] Valida formato PDF
- [ ] Associa currículo à vaga
- [ ] Suporta múltiplos uploads
- [ ] Testes de integração criados

**Labels:** `backend`, `api`, `feature`
**Estimativa:** 5 pontos

---

### Task 2.4: Criar interface de upload de currículos
**Descrição:**
Implementar tela web para upload de currículos.

**Acceptance Criteria:**
- [ ] Drag and drop de arquivos
- [ ] Validação de formato no frontend
- [ ] Barra de progresso de upload
- [ ] Feedback visual de sucesso/erro
- [ ] Suporta múltiplos arquivos

**Labels:** `frontend`, `ui`, `feature`
**Estimativa:** 5 pontos

---

## Epic 3: Extração de Texto de Currículos

### Task 3.1: Implementar classe ExtratorPDF
**Descrição:**
Criar classe para extrair texto de arquivos PDF usando PyMuPDF.

**Acceptance Criteria:**
- [ ] Extrai texto de todas as páginas
- [ ] Preserva estrutura do documento
- [ ] Trata PDFs corrompidos
- [ ] Respeita limite de 10 páginas
- [ ] Testes unitários criados

**Labels:** `backend`, `pdf`, `feature`
**Estimativa:** 8 pontos
**Status:** ✅ CONCLUÍDO

---

### Task 3.2: Integrar ExtratorPDF com pipeline de processamento
**Descrição:**
Integrar extração de PDF no fluxo de processamento de currículos.

**Acceptance Criteria:**
- [ ] Extração executada automaticamente após upload
- [ ] Texto extraído armazenado no banco
- [ ] Erros tratados adequadamente
- [ ] Testes de integração criados

**Labels:** `backend`, `integration`, `feature`
**Estimativa:** 5 pontos

---

## Epic 4: Anonimização de Dados Sensíveis

### Task 4.1: Configurar Microsoft Presidio
**Descrição:**
Instalar e configurar Microsoft Presidio para anonimização.

**Acceptance Criteria:**
- [ ] Presidio instalado e configurado
- [ ] Reconhecedores de entidades em português configurados
- [ ] Testes de reconhecimento criados

**Labels:** `backend`, `lgpd`, `setup`
**Estimativa:** 5 pontos

---

### Task 4.2: Implementar classe Anonimizador
**Descrição:**
Criar classe para anonimizar dados sensíveis usando Presidio.

**Acceptance Criteria:**
- [ ] Identifica e substitui nomes por [NOME]
- [ ] Identifica e substitui CPF por [CPF]
- [ ] Identifica e substitui endereços por [ENDEREÇO]
- [ ] Identifica e substitui telefones por [TELEFONE]
- [ ] Identifica e substitui emails por [EMAIL]
- [ ] Preserva informações profissionais
- [ ] Testes unitários criados

**Labels:** `backend`, `lgpd`, `feature`
**Estimativa:** 8 pontos

---

### Task 4.3: Integrar Anonimizador com pipeline
**Descrição:**
Integrar anonimização no fluxo de processamento de currículos.

**Acceptance Criteria:**
- [ ] Anonimização executada após extração de texto
- [ ] Texto anonimizado armazenado no banco
- [ ] Erros tratados adequadamente
- [ ] Testes de integração criados

**Labels:** `backend`, `integration`, `feature`
**Estimativa:** 3 pontos

---

## Epic 5: Análise e Ranqueamento por IA

### Task 5.1: Configurar integração com OpenAI API
**Descrição:**
Configurar credenciais e cliente para OpenAI API.

**Acceptance Criteria:**
- [ ] Variáveis de ambiente configuradas
- [ ] Cliente OpenAI inicializado
- [ ] Tratamento de erros de API implementado
- [ ] Testes de conexão criados

**Labels:** `backend`, `ai`, `setup`
**Estimativa:** 3 pontos

---

### Task 5.2: Implementar otimização de prompt
**Descrição:**
Criar função para otimizar prompt e minimizar tokens.

**Acceptance Criteria:**
- [ ] Extrai apenas informações essenciais da vaga
- [ ] Extrai apenas seções relevantes do currículo
- [ ] Remove texto redundante
- [ ] Estrutura em formato JSON
- [ ] Resume currículos longos (>2000 tokens)
- [ ] Testes unitários criados

**Labels:** `backend`, `ai`, `optimization`
**Estimativa:** 8 pontos

---

### Task 5.3: Implementar classe AnalisadorLLM
**Descrição:**
Criar classe para análise e ranqueamento de candidatos usando LLM.

**Acceptance Criteria:**
- [ ] Compara perfil do candidato com requisitos da vaga
- [ ] Atribui score de 0 a 100
- [ ] Gera justificativa textual
- [ ] Identifica pontos fortes
- [ ] Identifica gaps (lacunas)
- [ ] Testes unitários criados

**Labels:** `backend`, `ai`, `feature`
**Estimativa:** 13 pontos

---

### Task 5.4: Implementar geração de ranking
**Descrição:**
Criar função para gerar ranking ordenado de candidatos.

**Acceptance Criteria:**
- [ ] Ordena candidatos por score decrescente
- [ ] Armazena ranking no banco
- [ ] Testes unitários criados

**Labels:** `backend`, `feature`
**Estimativa:** 3 pontos

---

### Task 5.5: Integrar AnalisadorLLM com pipeline
**Descrição:**
Integrar análise por IA no fluxo de processamento.

**Acceptance Criteria:**
- [ ] Análise executada após anonimização
- [ ] Resultados armazenados no banco
- [ ] Erros tratados adequadamente
- [ ] Testes de integração criados

**Labels:** `backend`, `integration`, `feature`
**Estimativa:** 5 pontos

---

## Epic 6: Visualização de Resultados

### Task 6.1: Implementar API de ranking
**Descrição:**
Criar endpoint REST para obter ranking de candidatos.

**Acceptance Criteria:**
- [ ] Endpoint GET /vagas/{id}/ranking criado
- [ ] Retorna lista ordenada por score
- [ ] Inclui score, nome do arquivo e resumo
- [ ] Suporta ordenação por score ou nome
- [ ] Suporta filtro por score mínimo
- [ ] Testes de integração criados

**Labels:** `backend`, `api`, `feature`
**Estimativa:** 5 pontos

---

### Task 6.2: Implementar API de detalhes do candidato
**Descrição:**
Criar endpoint REST para obter detalhes completos de um candidato.

**Acceptance Criteria:**
- [ ] Endpoint GET /candidatos/{id} criado
- [ ] Retorna justificativa completa
- [ ] Retorna pontos fortes
- [ ] Retorna gaps
- [ ] Testes de integração criados

**Labels:** `backend`, `api`, `feature`
**Estimativa:** 3 pontos

---

### Task 6.3: Criar interface de visualização de ranking
**Descrição:**
Implementar tela web para visualizar ranking de candidatos.

**Acceptance Criteria:**
- [ ] Lista de candidatos com score e resumo
- [ ] Ordenação por score ou nome
- [ ] Filtro por score mínimo
- [ ] Expansão para ver detalhes completos
- [ ] Design responsivo

**Labels:** `frontend`, `ui`, `feature`
**Estimativa:** 8 pontos

---

## Epic 7: Interface Web

### Task 7.1: Configurar projeto FastAPI
**Descrição:**
Configurar estrutura inicial do projeto FastAPI.

**Acceptance Criteria:**
- [ ] FastAPI instalado e configurado
- [ ] Estrutura de pastas criada
- [ ] CORS configurado
- [ ] Documentação Swagger disponível

**Labels:** `backend`, `setup`
**Estimativa:** 3 pontos

---

### Task 7.2: Implementar navegação entre páginas
**Descrição:**
Criar sistema de navegação da aplicação web.

**Acceptance Criteria:**
- [ ] Menu de navegação implementado
- [ ] Rotas para todas as páginas criadas
- [ ] Navegação funcional
- [ ] Design responsivo

**Labels:** `frontend`, `ui`, `feature`
**Estimativa:** 5 pontos

---

### Task 7.3: Implementar feedback visual de processamento
**Descrição:**
Criar componentes de loading e progresso.

**Acceptance Criteria:**
- [ ] Spinner de loading implementado
- [ ] Barra de progresso implementada
- [ ] Feedback visual durante uploads
- [ ] Feedback visual durante análises

**Labels:** `frontend`, `ui`, `feature`
**Estimativa:** 3 pontos

---

### Task 7.4: Implementar sistema de mensagens de erro
**Descrição:**
Criar componente para exibir mensagens de erro.

**Acceptance Criteria:**
- [ ] Toast/notificação de erro implementado
- [ ] Mensagens claras e descritivas
- [ ] Diferentes níveis de severidade (erro, aviso, info)
- [ ] Auto-dismiss configurável

**Labels:** `frontend`, `ui`, `feature`
**Estimativa:** 3 pontos

---

## Epic 8: Persistência de Dados

### Task 8.1: Configurar banco de dados
**Descrição:**
Configurar banco de dados para o projeto.

**Acceptance Criteria:**
- [ ] Banco de dados escolhido e instalado
- [ ] Conexão configurada
- [ ] Migrations configuradas
- [ ] Testes de conexão criados

**Labels:** `backend`, `database`, `setup`
**Estimativa:** 5 pontos

---

### Task 8.2: Criar schema do banco de dados
**Descrição:**
Definir schema completo do banco de dados.

**Acceptance Criteria:**
- [ ] Tabela de vagas criada
- [ ] Tabela de currículos criada
- [ ] Tabela de análises criada
- [ ] Relacionamentos definidos
- [ ] Índices criados

**Labels:** `backend`, `database`, `feature`
**Estimativa:** 5 pontos

---

### Task 8.3: Implementar repositórios de dados
**Descrição:**
Criar classes de repositório para acesso aos dados.

**Acceptance Criteria:**
- [ ] Repository para Vagas implementado
- [ ] Repository para Currículos implementado
- [ ] Repository para Análises implementado
- [ ] Operações CRUD implementadas
- [ ] Testes unitários criados

**Labels:** `backend`, `database`, `feature`
**Estimativa:** 8 pontos

---

### Task 8.4: Implementar exclusão em cascata
**Descrição:**
Implementar lógica de exclusão em cascata de vagas.

**Acceptance Criteria:**
- [ ] Ao excluir vaga, currículos associados são removidos
- [ ] Ao excluir vaga, análises associadas são removidas
- [ ] Arquivos PDF são removidos do storage
- [ ] Testes de integração criados

**Labels:** `backend`, `database`, `feature`
**Estimativa:** 5 pontos

---

## Epic 9: Tratamento de Erros

### Task 9.1: Implementar sistema de logging
**Descrição:**
Configurar sistema de logging da aplicação.

**Acceptance Criteria:**
- [ ] Logger configurado
- [ ] Logs salvos em arquivo
- [ ] Diferentes níveis de log (debug, info, warning, error)
- [ ] Rotação de logs configurada

**Labels:** `backend`, `logging`, `feature`
**Estimativa:** 3 pontos

---

### Task 9.2: Implementar tratamento de erros de PDF
**Descrição:**
Criar handlers para erros de processamento de PDF.

**Acceptance Criteria:**
- [ ] Erros de PDF corrompido tratados
- [ ] Mensagens descritivas retornadas
- [ ] Erros registrados em log
- [ ] Testes criados

**Labels:** `backend`, `error-handling`, `feature`
**Estimativa:** 3 pontos

---

### Task 9.3: Implementar tratamento de erros de anonimização
**Descrição:**
Criar handlers para erros de anonimização.

**Acceptance Criteria:**
- [ ] Erros de anonimização tratados
- [ ] Processamento continua sem anonimização em caso de erro
- [ ] Erros registrados em log
- [ ] Testes criados

**Labels:** `backend`, `error-handling`, `feature`
**Estimativa:** 3 pontos

---

### Task 9.4: Implementar tratamento de erros de LLM
**Descrição:**
Criar handlers para erros de API do LLM.

**Acceptance Criteria:**
- [ ] Erros de API tratados (timeout, rate limit, etc)
- [ ] Mensagens descritivas retornadas
- [ ] Opção de reprocessamento disponível
- [ ] Erros registrados em log
- [ ] Testes criados

**Labels:** `backend`, `error-handling`, `feature`
**Estimativa:** 5 pontos

---

### Task 9.5: Implementar tratamento de erros de upload
**Descrição:**
Criar handlers para erros de upload de arquivos.

**Acceptance Criteria:**
- [ ] Erros de upload tratados
- [ ] Mensagens descritivas retornadas
- [ ] Erros registrados em log
- [ ] Testes criados

**Labels:** `backend`, `error-handling`, `feature`
**Estimativa:** 3 pontos

---

## Epic 10: Testes e Qualidade

### Task 10.1: Configurar ambiente de testes
**Descrição:**
Configurar pytest e ferramentas de teste.

**Acceptance Criteria:**
- [ ] Pytest instalado e configurado
- [ ] Coverage configurado
- [ ] Fixtures criadas
- [ ] CI/CD configurado para rodar testes

**Labels:** `testing`, `setup`
**Estimativa:** 3 pontos

---

### Task 10.2: Atingir 80% de cobertura de testes
**Descrição:**
Criar testes para atingir cobertura mínima de 80%.

**Acceptance Criteria:**
- [ ] Testes unitários criados
- [ ] Testes de integração criados
- [ ] Cobertura >= 80%
- [ ] Relatório de cobertura gerado

**Labels:** `testing`, `quality`
**Estimativa:** 13 pontos

---

### Task 10.3: Implementar testes E2E
**Descrição:**
Criar testes end-to-end do fluxo completo.

**Acceptance Criteria:**
- [ ] Teste de fluxo completo: cadastro vaga → upload currículo → análise → visualização
- [ ] Testes de cenários de erro
- [ ] Testes automatizados

**Labels:** `testing`, `e2e`
**Estimativa:** 8 pontos

---

## Epic 11: Documentação

### Task 11.1: Documentar APIs
**Descrição:**
Criar documentação completa das APIs.

**Acceptance Criteria:**
- [ ] Swagger/OpenAPI configurado
- [ ] Todos os endpoints documentados
- [ ] Exemplos de request/response incluídos
- [ ] Códigos de erro documentados

**Labels:** `documentation`
**Estimativa:** 5 pontos

---

### Task 11.2: Criar guia de instalação
**Descrição:**
Documentar processo de instalação e configuração.

**Acceptance Criteria:**
- [ ] Pré-requisitos listados
- [ ] Passo a passo de instalação
- [ ] Configuração de variáveis de ambiente
- [ ] Troubleshooting incluído

**Labels:** `documentation`
**Estimativa:** 3 pontos

---

### Task 11.3: Criar guia de contribuição
**Descrição:**
Documentar processo de contribuição ao projeto.

**Acceptance Criteria:**
- [ ] Padrões de código documentados
- [ ] Fluxo de Git documentado
- [ ] Processo de code review documentado
- [ ] Exemplos incluídos

**Labels:** `documentation`
**Estimativa:** 3 pontos
**Status:** ✅ CONCLUÍDO

---

## Resumo de Estimativas

| Epic | Tasks | Pontos Totais |
|------|-------|---------------|
| Epic 1: Cadastro de Vagas | 5 | 19 |
| Epic 2: Upload e Armazenamento | 4 | 18 |
| Epic 3: Extração de Texto | 2 | 13 |
| Epic 4: Anonimização | 3 | 16 |
| Epic 5: Análise por IA | 5 | 32 |
| Epic 6: Visualização | 3 | 16 |
| Epic 7: Interface Web | 4 | 14 |
| Epic 8: Persistência | 4 | 23 |
| Epic 9: Tratamento de Erros | 5 | 17 |
| Epic 10: Testes | 3 | 24 |
| Epic 11: Documentação | 3 | 11 |
| **TOTAL** | **41** | **203** |

---

## Priorização Sugerida (Ordem de Implementação)

### Sprint 1 - Fundação (34 pontos)
1. Task 8.1: Configurar banco de dados
2. Task 8.2: Criar schema do banco
3. Task 7.1: Configurar projeto FastAPI
4. Task 1.1: Criar modelo de dados para Vaga
5. Task 1.2: Implementar API de cadastro de vagas
6. Task 1.5: Criar interface de cadastro de vagas
7. Task 9.1: Implementar sistema de logging

### Sprint 2 - Upload e Processamento (31 pontos)
1. Task 2.1: Implementar validação de arquivo PDF
2. Task 2.2: Implementar armazenamento de PDFs
3. Task 2.3: Implementar API de upload
4. Task 2.4: Criar interface de upload
5. Task 3.2: Integrar ExtratorPDF com pipeline
6. Task 8.3: Implementar repositórios de dados

### Sprint 3 - Anonimização e IA (37 pontos)
1. Task 4.1: Configurar Microsoft Presidio
2. Task 4.2: Implementar classe Anonimizador
3. Task 4.3: Integrar Anonimizador
4. Task 5.1: Configurar OpenAI API
5. Task 5.2: Implementar otimização de prompt
6. Task 5.3: Implementar classe AnalisadorLLM

### Sprint 4 - Visualização e Ranking (29 pontos)
1. Task 5.4: Implementar geração de ranking
2. Task 5.5: Integrar AnalisadorLLM
3. Task 6.1: Implementar API de ranking
4. Task 6.2: Implementar API de detalhes
5. Task 6.3: Criar interface de visualização
6. Task 7.2: Implementar navegação

### Sprint 5 - Refinamento e Qualidade (42 pontos)
1. Task 1.3: Implementar API de edição
2. Task 1.4: Implementar API de listagem
3. Task 7.3: Implementar feedback visual
4. Task 7.4: Implementar mensagens de erro
5. Task 8.4: Implementar exclusão em cascata
6. Task 9.2-9.5: Implementar tratamento de erros
7. Task 10.1: Configurar ambiente de testes
8. Task 10.2: Atingir 80% de cobertura

### Sprint 6 - Finalização (30 pontos)
1. Task 10.3: Implementar testes E2E
2. Task 11.1: Documentar APIs
3. Task 11.2: Criar guia de instalação
4. Ajustes finais e correções de bugs
