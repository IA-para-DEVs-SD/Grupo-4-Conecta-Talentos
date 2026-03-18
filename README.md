# ConectaTalentos

## 📄 RH Inteligente — Ranqueamento de Currículos com IA

> Projeto do **Grupo 4** do curso **IA para Desenvolvedores**

---

## 🎯 Objetivo

Ranquear candidatos e facilitar a decisão do RH na escolha do profissional mais adequado para cada vaga.

---

## ⚙️ Como Funciona

1. **Cadastro de Vagas** — O RH registra as oportunidades disponíveis.
2. **Upload de Currículo** — O RH cadastra os currículos recebidos.
3. **Extração** — Conversão de PDF para texto estruturado.
4. **Análise por LLM** — A IA compara o perfil do candidato e ranqueia os mais adequados para cada vaga.

---

## 🚀 Desafios

- Criar o melhor prompt para ler currículos, pontuar e adequar o melhor candidato para a vaga.
- Otimizar para usar a menor quantidade de tokens possíveis mantendo a eficiência da análise.

---

## 🛠️ Tecnologias

| Tecnologia | Uso |
|---|---|
| Python (Web App) | Backend e interface web |
| Extração PDF nativa | Conversão de currículo para texto |
| LLM otimizado | Análise e ranqueamento de candidatos |
| Microsoft Presidio | Anonimização de dados sensíveis (LGPD) |

---

## 📄 Conversão de PDF para Texto

Script utilitário para extrair texto de arquivos PDF, utilizado na etapa de extração de currículos.

### Instalação

```bash
source .venv/bin/activate
pip install pymupdf
```

### Uso

```bash
# Exibir o texto no terminal
python pdf_to_text.py arquivo.pdf

# Salvar o texto em um arquivo
python pdf_to_text.py arquivo.pdf saida.txt
```

### Arquivo de exemplo

O arquivo `exemplo.pdf` contém um texto lorem ipsum para testes rápidos:

```bash
python pdf_to_text.py exemplo.pdf
```

---

## 👥 Integrantes — Grupo 4

| Nome |
|---|
| Gustavo da Rosa Heidemann |
| Halan Germano Bacca |
| Ismael Lunkes Pereira |
| Leandro da Silva Gerolim |
| Mariana Cristina da Silva Gabriel |
| Pedro Santos da Mota |

---

## 📝 Licença

Projeto acadêmico — uso educacional.
