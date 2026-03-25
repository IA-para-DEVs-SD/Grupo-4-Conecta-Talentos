# Guia de Contribuição - Grupo 4

Obrigado por contribuir com o projeto ConectaTalentos! Este guia ajudará você a seguir os padrões do projeto.

---

## 🚀 Como Contribuir

### 1. Configurar o Ambiente

```bash
# Clonar o repositório
git clone https://github.com/IA-para-DEVs-SD/Conecta-Talentos-Grupo4.git
cd Conecta-Talentos-Grupo4

# Criar ambiente virtual Python
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# Instalar dependências
pip install -r backend/requirements-basico.txt
```

### 2. Criar uma Nova Funcionalidade

```bash
# Atualizar develop
git checkout develop
git pull origin develop

# Criar branch de feature
git checkout -b feature/nome-da-funcionalidade

# Desenvolver a funcionalidade
# ... fazer alterações ...

# Commitar seguindo padrão semântico
git add .
git commit -m "feat: adiciona nova funcionalidade"

# Enviar para o repositório
git push -u origin feature/nome-da-funcionalidade
```

### 3. Criar Pull Request

1. Acesse o repositório no GitHub
2. Clique em "Pull Requests" → "New Pull Request"
3. Selecione sua branch `feature/nome-da-funcionalidade` para merge em `develop`
4. Preencha o template do PR:
   - Descrição clara do que foi implementado
   - Issues relacionadas (se houver)
   - Checklist de verificação
5. Solicite revisão de pelo menos 1 membro do grupo
6. Aguarde aprovação e feedback

---

## 📝 Padrão de Commits

### Formato

```
tipo: breve descrição

descrição detalhada (opcional)
```

### Tipos Principais

- `feat`: Nova funcionalidade
- `fix`: Correção de bug
- `docs`: Documentação
- `refactor`: Refatoração
- `test`: Testes
- `style`: Formatação
- `chore`: Manutenção

### Exemplos

```bash
git commit -m "feat: adiciona validação de CPF"
git commit -m "fix: corrige erro na extração de PDF"
git commit -m "docs: atualiza README com novas instruções"
git commit -m "refactor: melhora estrutura da classe ExtratorPDF"
git commit -m "test: adiciona testes para anonimização"
```

---

## 🌿 Fluxo Git

```
main (produção)
  ↑
  └── develop (desenvolvimento)
        ↑
        ├── feature/funcionalidade-1
        ├── feature/funcionalidade-2
        └── feature/funcionalidade-3
```

### Regras

- **Nunca** commitar direto em `main`
- **Sempre** criar features a partir de `develop`
- **Sempre** fazer PR para `develop`, não para `main`
- Manter `develop` atualizado antes de criar nova feature

---

## ✅ Checklist do Pull Request

Antes de criar um PR, verifique:

- [ ] Código segue os padrões do projeto
- [ ] Commits seguem formato semântico
- [ ] Código foi testado localmente
- [ ] Documentação foi atualizada (se necessário)
- [ ] Não há conflitos com `develop`
- [ ] Código está formatado corretamente
- [ ] Variáveis e funções têm nomes descritivos
- [ ] Não há código comentado desnecessário
- [ ] Não há credenciais ou dados sensíveis

---

## 🧪 Testes

### Executar Testes

```bash
# Executar todos os testes
pytest backend/tests/

# Executar teste específico
pytest backend/tests/test_extrator_pdf.py

# Executar com cobertura
pytest --cov=backend/src backend/tests/
```

### Escrever Testes

```python
# backend/tests/test_exemplo.py

def test_funcionalidade_basica():
    """Testa comportamento básico da funcionalidade."""
    # Arrange (preparar)
    entrada = "valor de teste"
    
    # Act (executar)
    resultado = funcao_testada(entrada)
    
    # Assert (verificar)
    assert resultado == "valor esperado"

def test_tratamento_de_erro():
    """Testa se erro é tratado corretamente."""
    with pytest.raises(ValueError):
        funcao_testada("entrada inválida")
```

---

## 📚 Documentação

### Docstrings

Toda função/classe pública deve ter docstring:

```python
def processar_curriculo(caminho: Path, vaga_id: int) -> Resultado:
    """
    Processa um currículo para uma vaga específica.
    
    Args:
        caminho: Caminho para o arquivo PDF do currículo
        vaga_id: ID da vaga no sistema
        
    Returns:
        Resultado contendo análise e pontuação
        
    Raises:
        ArquivoNaoEncontradoError: Se o arquivo não existir
        PDFInvalidoError: Se o PDF for inválido
    """
```

### Atualizar Documentação

Ao adicionar funcionalidades, atualize:

- README.md (se necessário)
- Documentação técnica em `backend/docs/`
- Comentários no código
- Docstrings

---

## 🎨 Estilo de Código

### Python

```python
# Bom ✅
def calcular_pontuacao(candidato: Candidato, vaga: Vaga) -> float:
    """Calcula pontuação do candidato para a vaga."""
    experiencia = candidato.anos_experiencia
    requisitos = vaga.requisitos_minimos
    
    if experiencia >= requisitos:
        return 100.0
    return (experiencia / requisitos) * 100.0

# Ruim ❌
def calc(c,v):
    e=c.exp
    r=v.req
    if e>=r:return 100.0
    return(e/r)*100.0
```

### Nomenclatura

- Classes: `PascalCase`
- Funções: `snake_case`
- Constantes: `UPPER_SNAKE_CASE`
- Variáveis: `snake_case`

---

## 🐛 Reportar Bugs

### Como Reportar

1. Verifique se o bug já foi reportado nas Issues
2. Crie uma nova Issue com o template:

```markdown
## Descrição do Bug
Descrição clara do problema

## Como Reproduzir
1. Passo 1
2. Passo 2
3. Erro ocorre

## Comportamento Esperado
O que deveria acontecer

## Comportamento Atual
O que está acontecendo

## Ambiente
- OS: Windows/Linux/Mac
- Python: 3.11
- Versão do projeto: commit hash

## Logs/Screenshots
Cole logs ou adicione screenshots
```

---

## 💡 Sugerir Melhorias

Para sugerir novas funcionalidades:

1. Abra uma Issue com label `enhancement`
2. Descreva a funcionalidade proposta
3. Explique o caso de uso
4. Aguarde discussão com o grupo

---

## 🔍 Code Review

### Como Revisar PRs

1. Leia a descrição do PR
2. Verifique o código linha por linha
3. Teste localmente se possível
4. Deixe comentários construtivos
5. Aprove ou solicite mudanças

### Boas Práticas de Review

- Seja respeitoso e construtivo
- Explique o "porquê" das sugestões
- Reconheça boas soluções
- Foque em melhorias, não em críticas pessoais

---

## 📞 Dúvidas

Se tiver dúvidas sobre como contribuir:

1. Consulte a [documentação de padrões](.github/PADROES.md)
2. Pergunte no grupo
3. Abra uma Issue com label `question`

---

## 📜 Licença

Ao contribuir, você concorda que suas contribuições serão licenciadas sob a mesma licença do projeto.

---

**Obrigado por contribuir com o ConectaTalentos!** 🚀
