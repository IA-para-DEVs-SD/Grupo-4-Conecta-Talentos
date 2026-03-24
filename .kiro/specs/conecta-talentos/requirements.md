# Documento de Requisitos - ConectaTalentos

## Introdução

O ConectaTalentos é um sistema inteligente que usa Inteligência Artificial para ajudar profissionais de RH a selecionar candidatos. O sistema funciona assim: você cadastra uma vaga, envia currículos em PDF, e a IA analisa automaticamente cada candidato, dando uma nota e explicando por que aquela pessoa é adequada (ou não) para a vaga. O sistema também protege dados pessoais dos candidatos, seguindo as regras da LGPD.

## Glossário (Termos Importantes)

- **Sistema**: O ConectaTalentos completo
- **RH**: Profissional de Recursos Humanos que usa o sistema
- **Vaga**: Oportunidade de emprego cadastrada no sistema
- **Currículo**: Documento em PDF com informações profissionais do candidato
- **Candidato**: Pessoa que enviou currículo para análise
- **Pontuação**: Nota de 0 a 100 que indica o quanto o candidato se encaixa na vaga
- **Ranking**: Lista de candidatos ordenados da maior para a menor pontuação
- **Dados Sensíveis**: Informações pessoais protegidas por lei (nome, CPF, endereço, telefone, email)
- **IA/Inteligência Artificial**: Tecnologia que analisa e avalia os currículos automaticamente

## Requisitos

### Requisito 1: Cadastro de Vagas

**História do Usuário:** Como profissional de RH, eu quero cadastrar vagas com todos os detalhes necessários, para que o sistema consiga comparar os candidatos corretamente.

#### O que o sistema precisa fazer:

1. Permitir criar uma nova vaga
2. Ao cadastrar uma vaga, guardar as seguintes informações:
   - Título da vaga
   - Descrição do trabalho
   - Requisitos técnicos necessários
   - Experiência mínima exigida
   - Competências desejadas
3. Verificar se todos os campos obrigatórios foram preenchidos antes de salvar
4. Permitir editar vagas que já foram criadas
5. Mostrar uma lista com todas as vagas cadastradas

### Requisito 2: Upload e Armazenamento de Currículos

**História do Usuário:** Como profissional de RH, eu quero enviar currículos em PDF para o sistema, para que eles possam ser processados e analisados automaticamente.

#### O que o sistema precisa fazer:

1. Verificar se o arquivo enviado está em formato PDF
2. Se o arquivo não for PDF, mostrar mensagem de erro explicando o problema
3. Guardar o arquivo PDF original enviado
4. Associar cada currículo enviado a uma vaga específica
5. Permitir enviar vários currículos para a mesma vaga

### Requisito 3: Extração de Texto de Currículos

**História do Usuário:** Como sistema, eu preciso ler o conteúdo dos PDFs, para que a Inteligência Artificial possa analisar as informações dos candidatos.

#### O que o sistema precisa fazer:

1. Converter o currículo em PDF para texto que possa ser lido
2. Manter a organização do documento (seções, parágrafos) ao extrair o texto
3. Ler o texto de todas as páginas do PDF
4. Se o PDF estiver corrompido ou ilegível, mostrar mensagem de erro específica
5. Processar currículos com até 10 páginas

### Requisito 4: Anonimização de Dados Sensíveis

**História do Usuário:** Como sistema, eu preciso esconder dados pessoais dos candidatos, para estar de acordo com a Lei Geral de Proteção de Dados (LGPD).

#### O que o sistema precisa fazer:

1. Identificar dados pessoais no currículo usando tecnologia Microsoft Presidio
2. Substituir nomes por [NOME]
3. Substituir CPF por [CPF]
4. Substituir endereços por [ENDEREÇO]
5. Substituir telefones por [TELEFONE]
6. Substituir emails por [EMAIL]
7. Manter todas as informações profissionais importantes (experiências de trabalho, habilidades, formação acadêmica)

### Requisito 5: Análise e Ranqueamento por Inteligência Artificial

**História do Usuário:** Como profissional de RH, eu quero que a IA analise e classifique os candidatos automaticamente, para que eu possa focar nos perfis mais adequados para a vaga.

#### O que o sistema precisa fazer:

1. Comparar o perfil de cada candidato com os requisitos da vaga
2. Dar uma pontuação de 0 a 100 para cada candidato
3. Escrever uma explicação do porquê daquela pontuação
4. Identificar os pontos fortes do candidato em relação à vaga
5. Identificar o que falta no perfil do candidato (lacunas em relação aos requisitos)
6. Quando houver vários candidatos para uma vaga, criar um ranking ordenado da maior para a menor pontuação

### Requisito 6: Otimização de Custos com IA

**História do Usuário:** Como desenvolvedor, eu quero que o sistema use a IA de forma eficiente, para que os custos sejam menores e o sistema seja mais rápido.

#### O que o sistema precisa fazer:

1. Enviar para a IA apenas as informações essenciais, sem textos desnecessários
2. Da vaga, incluir apenas: título, requisitos principais e competências necessárias
3. Do currículo, incluir apenas as partes relevantes para a análise
4. Remover textos repetidos ou irrelevantes antes de enviar para a IA
5. Organizar as informações de forma compacta (em formato JSON ou lista estruturada)
6. Se o currículo for muito longo (mais de 2000 palavras), resumir as partes menos importantes

### Requisito 7: Visualização de Resultados

**História do Usuário:** Como profissional de RH, eu quero ver o ranking dos candidatos com as explicações, para tomar decisões bem informadas sobre quem contratar.

#### O que o sistema precisa fazer:

1. Mostrar o ranking de candidatos para cada vaga
2. Para cada candidato, exibir:
   - Pontuação recebida
   - Nome do arquivo do currículo
   - Resumo da avaliação
3. Permitir clicar para ver mais detalhes:
   - Explicação completa da avaliação
   - Pontos fortes do candidato
   - O que falta no perfil
4. Permitir ordenar a lista por pontuação ou por nome
5. Permitir filtrar candidatos por pontuação mínima (exemplo: mostrar apenas quem tirou acima de 70)

### Requisito 8: Interface Web

**História do Usuário:** Como profissional de RH, eu quero acessar o sistema pelo navegador, para poder usá-lo de qualquer computador sem precisar instalar nada.

#### O que o sistema precisa fazer:

1. Funcionar em qualquer navegador web (Chrome, Firefox, Edge, etc.)
2. Ter páginas para:
   - Cadastrar vagas
   - Enviar currículos
   - Ver rankings de candidatos
3. Mostrar indicadores visuais quando algo estiver sendo processado (ícone de carregamento, barra de progresso)
4. Mostrar mensagens de erro claras quando algo der errado
5. Funcionar bem em telas de computador (desktop)

### Requisito 9: Armazenamento de Dados

**História do Usuário:** Como sistema, eu preciso guardar todas as informações de forma permanente, para que nada seja perdido quando o sistema for fechado ou reiniciado.

#### O que o sistema precisa fazer:

1. Guardar permanentemente todas as vagas cadastradas
2. Guardar permanentemente todos os arquivos PDF de currículos
3. Guardar permanentemente todos os resultados das análises (pontuações, explicações, rankings)
4. Permitir recuperar todas essas informações depois que o sistema for reiniciado
5. Quando uma vaga for excluída, apagar também todos os currículos e análises relacionados a ela

### Requisito 10: Tratamento de Erros

**História do Usuário:** Como profissional de RH, eu quero receber mensagens claras quando algo der errado, para que eu possa resolver o problema rapidamente.

#### O que o sistema precisa fazer:

1. Se houver problema ao ler o PDF, mostrar mensagem explicando que há algo errado com o arquivo
2. Se houver problema ao esconder dados pessoais, registrar o erro mas continuar o processamento
3. Se a IA estiver indisponível ou falhar, mostrar mensagem de erro e permitir tentar novamente
4. Se o envio de arquivo falhar, mostrar mensagem de erro específica explicando o que aconteceu
5. Registrar todos os erros em um arquivo de log para que problemas possam ser investigados depois

### Requisito 11: Exportação de Relatórios

**História do Usuário:** Como profissional de RH, eu quero baixar o ranking de candidatos em PDF ou Excel, para compartilhar com meus gestores e guardar como documentação do processo seletivo.

#### O que o sistema precisa fazer:

1. Oferecer botão para baixar o ranking em PDF
2. Oferecer botão para baixar o ranking em Excel
3. No arquivo exportado, incluir para cada candidato:
   - Pontuação recebida
   - Resumo da avaliação
   - Principais qualificações
   - O que falta no perfil
4. No topo do relatório, mostrar:
   - Nome da vaga
   - Data em que a vaga foi criada
   - Principais requisitos da vaga
5. Permitir escolher quantos candidatos incluir (exemplo: apenas os 10 melhores ou todos)
6. Criar nome automático para o arquivo com o nome da vaga e a data (exemplo: "Desenvolvedor-Java-23-03-2026.pdf")
7. Iniciar o download automaticamente quando o arquivo estiver pronto

### Requisito 12: Histórico e Auditoria

**História do Usuário:** Como profissional de RH, eu quero ver o histórico de tudo que foi feito no sistema, para acompanhar o processo seletivo e entender como as avaliações dos candidatos mudaram ao longo do tempo.

#### O que o sistema precisa fazer:

1. Guardar data e hora de todas as ações importantes:
   - Quando uma vaga foi criada
   - Quando um currículo foi enviado
   - Quando uma análise foi feita
2. Guardar todas as avaliações anteriores quando um currículo for analisado novamente
3. Quando um candidato for avaliado mais de uma vez, mostrar:
   - Todas as pontuações que ele recebeu
   - Data e hora de cada avaliação
4. Permitir ver todo o histórico de uma vaga específica
5. Mostrar quem fez cada ação (qual usuário do RH)
6. Permitir comparar avaliações diferentes do mesmo candidato lado a lado
7. Registrar quando uma vaga foi modificada, mostrando:
   - O que foi alterado
   - Quando foi alterado
8. Mostrar tudo em ordem cronológica (do mais antigo para o mais recente ou vice-versa)

