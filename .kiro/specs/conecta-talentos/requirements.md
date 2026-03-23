# Documento de Requisitos - ConectaTalentos

## Introdução

O ConectaTalentos é um sistema de ranqueamento inteligente de currículos que utiliza IA para auxiliar profissionais de RH na seleção de candidatos. O sistema recebe vagas cadastradas, processa currículos em formato PDF, extrai informações relevantes, anonimiza dados sensíveis conforme LGPD, e utiliza um modelo de linguagem (LLM) para analisar e ranquear candidatos de acordo com a adequação ao perfil da vaga.

## Glossário

- **Sistema**: O sistema ConectaTalentos completo
- **RH**: Profissional de Recursos Humanos que utiliza o sistema
- **Vaga**: Oportunidade de emprego cadastrada no sistema com requisitos específicos
- **Currículo**: Documento em formato PDF contendo informações profissionais do candidato
- **Candidato**: Pessoa cujo currículo foi submetido para análise
- **Extrator_PDF**: Componente responsável por converter PDF em texto estruturado
- **Anônimizador**: Componente que remove dados sensíveis usando Microsoft Presidio
- **Analisador_LLM**: Componente de IA que avalia e ranqueia candidatos
- **Score**: Pontuação numérica de adequação do candidato à vaga (0-100)
- **Ranking**: Lista ordenada de candidatos por score decrescente
- **Dados_Sensíveis**: Informações pessoais protegidas pela LGPD (nome, CPF, endereço, telefone, email)
- **Prompt_Otimizado**: Instrução estruturada para o LLM que minimiza uso de tokens
- **Texto_Estruturado**: Texto extraído do PDF organizado em seções identificáveis

## Requisitos

### Requisito 1: Cadastro de Vagas

**User Story:** Como RH, eu quero cadastrar vagas com requisitos detalhados, para que o sistema possa comparar candidatos adequadamente.

#### Acceptance Criteria

1. THE Sistema SHALL permitir o cadastro de uma nova Vaga
2. WHEN uma Vaga é cadastrada, THE Sistema SHALL armazenar título, descrição, requisitos técnicos, experiência mínima e competências desejadas
3. THE Sistema SHALL validar que todos os campos obrigatórios da Vaga estão preenchidos
4. THE Sistema SHALL permitir a edição de Vagas existentes
5. THE Sistema SHALL permitir a visualização de todas as Vagas cadastradas

### Requisito 2: Upload e Armazenamento de Currículos

**User Story:** Como RH, eu quero fazer upload de currículos em PDF, para que o sistema possa processá-los e analisá-los.

#### Acceptance Criteria

1. WHEN o RH submete um arquivo, THE Sistema SHALL validar que o formato é PDF
2. IF o arquivo não é PDF, THEN THE Sistema SHALL retornar mensagem de erro descritiva
3. THE Sistema SHALL armazenar o arquivo PDF original
4. WHEN um Currículo é enviado, THE Sistema SHALL associá-lo a uma Vaga específica
5. THE Sistema SHALL permitir upload de múltiplos Currículos para a mesma Vaga

### Requisito 3: Extração de Texto de Currículos

**User Story:** Como sistema, eu preciso extrair texto de PDFs, para que o conteúdo possa ser analisado pelo LLM.

#### Acceptance Criteria

1. WHEN um Currículo em PDF é processado, THE Extrator_PDF SHALL converter o documento em Texto_Estruturado
2. THE Extrator_PDF SHALL preservar a estrutura lógica do documento (seções, parágrafos)
3. THE Extrator_PDF SHALL extrair texto de todas as páginas do PDF
4. IF o PDF está corrompido ou ilegível, THEN THE Extrator_PDF SHALL retornar erro específico
5. THE Extrator_PDF SHALL processar PDFs com até 10 páginas

### Requisito 4: Anonimização de Dados Sensíveis

**User Story:** Como sistema, eu preciso anonimizar dados pessoais, para que o sistema esteja em conformidade com a LGPD.

#### Acceptance Criteria

1. WHEN o texto é extraído do Currículo, THE Anônimizador SHALL identificar Dados_Sensíveis usando Microsoft Presidio
2. THE Anônimizador SHALL substituir nomes por tokens genéricos (ex: [NOME])
3. THE Anônimizador SHALL substituir CPF por [CPF]
4. THE Anônimizador SHALL substituir endereços por [ENDEREÇO]
5. THE Anônimizador SHALL substituir telefones por [TELEFONE]
6. THE Anônimizador SHALL substituir emails por [EMAIL]
7. THE Anônimizador SHALL preservar informações profissionais relevantes (experiências, habilidades, formação)

### Requisito 5: Análise e Ranqueamento por LLM

**User Story:** Como RH, eu quero que a IA analise e ranqueie candidatos automaticamente, para que eu possa focar nos perfis mais adequados.

#### Acceptance Criteria

1. WHEN um Currículo anonimizado está disponível, THE Analisador_LLM SHALL comparar o perfil do Candidato com os requisitos da Vaga
2. THE Analisador_LLM SHALL atribuir um Score de 0 a 100 para cada Candidato
3. THE Analisador_LLM SHALL gerar justificativa textual para o Score atribuído
4. THE Analisador_LLM SHALL identificar pontos fortes do Candidato em relação à Vaga
5. THE Analisador_LLM SHALL identificar gaps (lacunas) entre o perfil do Candidato e os requisitos da Vaga
6. WHEN múltiplos Candidatos são analisados para uma Vaga, THE Sistema SHALL gerar um Ranking ordenado por Score decrescente

### Requisito 6: Otimização de Tokens do Prompt

**User Story:** Como desenvolvedor, eu quero minimizar o uso de tokens, para que o sistema seja eficiente e econômico.

#### Acceptance Criteria

1. THE Sistema SHALL utilizar um Prompt_Otimizado que minimize o número de tokens enviados ao LLM
2. THE Prompt_Otimizado SHALL incluir apenas informações essenciais da Vaga (título, requisitos-chave, competências)
3. THE Prompt_Otimizado SHALL incluir apenas seções relevantes do Currículo anonimizado
4. THE Sistema SHALL remover texto redundante ou irrelevante antes de enviar ao LLM
5. THE Sistema SHALL estruturar o prompt em formato conciso (JSON ou lista estruturada)
6. WHEN o texto do Currículo excede 2000 tokens, THE Sistema SHALL resumir seções menos relevantes

### Requisito 7: Visualização de Resultados

**User Story:** Como RH, eu quero visualizar o ranking de candidatos com justificativas, para que eu possa tomar decisões informadas.

#### Acceptance Criteria

1. THE Sistema SHALL exibir o Ranking de Candidatos para cada Vaga
2. WHEN o RH visualiza o Ranking, THE Sistema SHALL mostrar Score, nome do arquivo do Currículo e resumo da justificativa
3. THE Sistema SHALL permitir expandir a visualização para ver justificativa completa, pontos fortes e gaps
4. THE Sistema SHALL permitir ordenação do Ranking por Score ou nome
5. THE Sistema SHALL permitir filtrar Candidatos por Score mínimo

### Requisito 8: Interface Web

**User Story:** Como RH, eu quero acessar o sistema via navegador web, para que eu possa utilizá-lo de qualquer lugar.

#### Acceptance Criteria

1. THE Sistema SHALL fornecer interface web acessível via navegador
2. THE Sistema SHALL implementar navegação entre páginas (cadastro de vagas, upload de currículos, visualização de rankings)
3. THE Sistema SHALL exibir feedback visual durante processamento de Currículos (loading, progresso)
4. THE Sistema SHALL exibir mensagens de erro claras quando operações falham
5. THE Sistema SHALL ser responsivo para uso em desktop

### Requisito 9: Persistência de Dados

**User Story:** Como sistema, eu preciso armazenar dados de forma persistente, para que informações não sejam perdidas entre sessões.

#### Acceptance Criteria

1. THE Sistema SHALL persistir dados de Vagas cadastradas
2. THE Sistema SHALL persistir arquivos PDF de Currículos
3. THE Sistema SHALL persistir resultados de análises (Scores, justificativas, Rankings)
4. THE Sistema SHALL permitir recuperação de dados após reinicialização
5. WHEN uma Vaga é excluída, THE Sistema SHALL remover Currículos e análises associadas

### Requisito 10: Tratamento de Erros

**User Story:** Como RH, eu quero receber mensagens claras quando algo falha, para que eu possa corrigir problemas rapidamente.

#### Acceptance Criteria

1. IF o Extrator_PDF falha, THEN THE Sistema SHALL exibir mensagem indicando problema com o arquivo PDF
2. IF o Anônimizador falha, THEN THE Sistema SHALL registrar erro e continuar processamento sem anonimização
3. IF o Analisador_LLM falha ou está indisponível, THEN THE Sistema SHALL exibir mensagem de erro e permitir reprocessamento
4. IF o upload de arquivo falha, THEN THE Sistema SHALL exibir mensagem de erro específica
5. THE Sistema SHALL registrar todos os erros em log para diagnóstico

