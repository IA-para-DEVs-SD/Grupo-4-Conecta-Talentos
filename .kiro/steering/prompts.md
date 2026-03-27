# Histórico de Prompts - ConectaTalentos

Este documento registra os principais prompts utilizados durante o desenvolvimento do projeto ConectaTalentos, servindo como referência para interações futuras com assistentes de IA.

## Configuração Inicial do Projeto

### 1. Análise e Criação de Steering Rules

**Prompt:**
```
Analyze this repository and create basic steering rules that would help guide an AI assistant.

Steering documents are markdown files that are always in '.kiro/steering'.

Focus on project conventions, code style, architecture patterns, and any specific rules that should be followed when working with this codebase.

For the initial setup, please only create the following files:
  - product.md: Short summary of the product
  - tech.md: Build system used, tech stack, libraries, frameworks etc. If there are any common commands for building, testing, compiling etc make sure to include a section for that
  - structure.md: Project organization and folder structure
  
You do not need to create any folders. They have been created for you.

The goal is to be succinct, but capture information that will be useful for an LLM application operating in this project.
```

**Resultado:**
- Criação de `product.md` com visão geral do produto
- Criação de `tech.md` com stack tecnológico e comandos comuns
- Criação de `structure.md` com organização e padrões do projeto

**Data:** 2026-03-27

---

### 2. Commit, Push e Pull Request

**Prompt:**
```
de o commit de tudo, inclusive do steering de o push e crie o pr na develop
```

**Resultado:**
- Commit com mensagem seguindo conventional commits
- Push para branch `feature/padronizacao-projeto`
- Criação do PR #56 para branch `develop`

**Data:** 2026-03-27

---

## Padrões de Interação Identificados

### Comandos Git
- Preferência por comandos em português
- Uso de conventional commits para mensagens
- PRs com descrição detalhada incluindo checklist

### Documentação
- Documentos em markdown
- Estrutura clara com seções bem definidas
- Foco em informações práticas e acionáveis
- Exemplos de código quando relevante

### Estilo de Comunicação
- Respostas diretas e objetivas
- Confirmação de ações realizadas
- Links para recursos criados (PRs, issues, etc.)

---

## Notas para Futuras Interações

1. **Idioma**: O usuário alterna entre português e inglês. Seguir o idioma do prompt.

2. **Contexto do Projeto**: ConectaTalentos é um sistema de ranqueamento de currículos com IA, focado em:
   - Conformidade com LGPD
   - Otimização de tokens para LLM
   - Arquitetura em camadas (controllers → services → repositories → processors)

3. **Ferramentas Preferidas**:
   - Git CLI para versionamento
   - GitHub CLI (`gh`) para PRs
   - Python 3.11+ com FastAPI
   - PyMuPDF para processamento de PDFs
   - Microsoft Presidio para anonimização

4. **Estrutura de Branches**:
   - `develop`: branch principal de desenvolvimento
   - `feature/*`: branches de funcionalidades
   - PRs sempre direcionados para `develop`

---

## Prompts Úteis para Referência Futura

### Análise de Código
```
Analise o código em [arquivo] e sugira melhorias seguindo os padrões do projeto
```

### Criação de Testes
```
Crie testes unitários para [componente] usando pytest e hypothesis
```

### Documentação
```
Documente a funcionalidade [nome] seguindo o padrão estabelecido em backend/docs/
```

### Refatoração
```
Refatore [componente] para seguir a arquitetura em camadas definida em structure.md
```

### Implementação de Features
```
Implemente [funcionalidade] seguindo os requisitos em .kiro/specs/conecta-talentos/requirements.md
```
