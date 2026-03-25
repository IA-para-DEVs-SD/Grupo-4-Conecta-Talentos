# Grupo 4 - ConectaTalentos

## Descrição do Projeto

Sistema inteligente de ranqueamento de currículos que utiliza Inteligência Artificial para auxiliar profissionais de RH na seleção de candidatos. O sistema processa currículos em PDF, extrai informações relevantes, anonimiza dados sensíveis conforme LGPD, e utiliza IA para analisar e ranquear candidatos de acordo com a adequação ao perfil da vaga.

## Sumário de Documentações

- [Requisitos do Sistema](/.kiro/specs/conecta-talentos/requirements.md)
- [Design e Arquitetura](/.kiro/specs/conecta-talentos/design.md)
- [Guia de Uso do ExtratorPDF](backend/docs/como-usar-extrator.md)
- [Documentação Técnica](backend/docs/classe-extrator-pdf.md)
- [Base de Implementação](backend/docs/base-implementacao.md)
- [Padrões do Projeto](.github/PADROES.md)
- [Guia de Contribuição](.github/CONTRIBUTING.md)

## Tecnologias Utilizadas

| Tecnologia | Versão | Uso |
|---|---|---|
| Python | 3.11+ | Backend e processamento |
| PyMuPDF | Latest | Extração de texto de PDFs |
| Microsoft Presidio | Latest | Anonimização de dados (LGPD) |
| OpenAI API | Latest | Análise e ranqueamento com IA |
| FastAPI | Latest | Interface web e API REST |

## Instruções de Instalação e Uso

### Pré-requisitos

- Python 3.11 ou superior
- pip (gerenciador de pacotes Python)
- Git

### Instalação

1. Clone o repositório:
```bash
git clone https://github.com/IA-para-DEVs-SD/Conecta-Talentos-Grupo4.git
cd Conecta-Talentos-Grupo4
```

2. Crie e ative o ambiente virtual:

**Linux/Mac:**
```bash
python -m venv .venv
source .venv/bin/activate
```

**Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

3. Instale as dependências:
```bash
pip install -r backend/requirements-basico.txt
```

### Uso

Testar extração de PDF:
```bash
python backend/src/services/exemplo_uso_extrator.py
```

Usar com arquivo específico:
```bash
python backend/src/services/extrator_pdf.py caminho/para/arquivo.pdf
```

## Integrantes do Grupo

- Gustavo da Rosa Heidemann
- Halan Germano Bacca
- Ismael Lunkes Pereira
- Leandro da Silva Gerolim
- Mariana Cristina da Silva Gabriel
- Pedro Santos da Mota
