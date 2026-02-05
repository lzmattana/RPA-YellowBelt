# 🤝 Guia de Contribuição

Obrigado por considerar contribuir com o projeto Automação GE! Este documento fornece diretrizes para tornar o processo de contribuição claro e eficiente.

---

## 📑 Índice

1. [Código de Conduta](#código-de-conduta)
2. [Como Posso Contribuir?](#como-posso-contribuir)
3. [Primeiros Passos](#primeiros-passos)
4. [Processo de Desenvolvimento](#processo-de-desenvolvimento)
5. [Padrões de Código](#padrões-de-código)
6. [Commit Guidelines](#commit-guidelines)
7. [Pull Request Process](#pull-request-process)
8. [Reportando Bugs](#reportando-bugs)
9. [Sugerindo Melhorias](#sugerindo-melhorias)

---

## Código de Conduta

### Nossa Promessa

No interesse de promover um ambiente aberto e acolhedor, nós, como contribuidores e mantenedores, comprometemo-nos a tornar a participação em nosso projeto e nossa comunidade uma experiência livre de assédio para todos.

### Nossos Padrões

**Comportamentos que contribuem para criar um ambiente positivo:**
- ✅ Usar linguagem acolhedora e inclusiva
- ✅ Respeitar pontos de vista e experiências diferentes
- ✅ Aceitar críticas construtivas graciosamente
- ✅ Focar no que é melhor para a comunidade
- ✅ Mostrar empatia com outros membros da comunidade

**Comportamentos inaceitáveis:**
- ❌ Uso de linguagem ou imagens sexualizadas
- ❌ Trolling, comentários insultuosos/depreciativos
- ❌ Assédio público ou privado
- ❌ Publicar informações privadas de outros
- ❌ Outras condutas consideradas inapropriadas

---

## Como Posso Contribuir?

Existem várias maneiras de contribuir com este projeto:

### 🐛 Reportar Bugs
Encontrou um bug? Abra uma issue descrevendo o problema.

### 💡 Sugerir Melhorias
Tem uma ideia para melhorar o projeto? Compartilhe conosco!

### 📝 Melhorar Documentação
Documentação clara é essencial. Correções e melhorias são sempre bem-vindas.

### 💻 Contribuir com Código
Implementar novas funcionalidades ou corrigir bugs existentes.

### 🧪 Testes
Adicionar testes automatizados aumenta a confiabilidade do projeto.

### 🎨 Design e UX
Melhorias na interface e experiência do usuário.

---

## Primeiros Passos

### 1. Fork o Repositório

Clique no botão "Fork" no GitHub para criar sua cópia do projeto.

### 2. Clone Localmente

```bash
git clone https://github.com/SEU-USUARIO/automacao-ge-yellowbelt.git
cd automacao-ge-yellowbelt
```

### 3. Configure o Upstream

```bash
git remote add upstream https://github.com/USUARIO-ORIGINAL/automacao-ge-yellowbelt.git
```

### 4. Crie um Ambiente Virtual

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 5. Instale Dependências

```bash
pip install -r requirements.txt
```

### 6. Configure ChromeDriver

Baixe o ChromeDriver compatível com seu Chrome:
```
https://chromedriver.chromium.org/downloads
```

---

## Processo de Desenvolvimento

### Workflow Git

```
main (branch principal - produção)
  │
  ├── develop (branch de desenvolvimento)
  │     │
  │     ├── feature/nova-funcionalidade
  │     ├── bugfix/correcao-bug
  │     └── hotfix/correcao-urgente
  │
  └── release/v1.1.0
```

### Criando uma Branch

**Para nova funcionalidade:**
```bash
git checkout develop
git pull upstream develop
git checkout -b feature/nome-da-funcionalidade
```

**Para correção de bug:**
```bash
git checkout develop
git pull upstream develop
git checkout -b bugfix/descricao-do-bug
```

**Para correção urgente (hotfix):**
```bash
git checkout main
git pull upstream main
git checkout -b hotfix/descricao-urgente
```

### Nomenclatura de Branches

| Tipo | Padrão | Exemplo |
|------|--------|---------|
| Feature | `feature/descricao` | `feature/busca-em-lote` |
| Bugfix | `bugfix/descricao` | `bugfix/erro-cnpj` |
| Hotfix | `hotfix/descricao` | `hotfix/crash-login` |
| Release | `release/vX.Y.Z` | `release/v1.1.0` |

---

## Padrões de Código

### Python Style Guide

Seguimos [PEP 8](https://pep8.org/) com algumas adaptações:

#### Formatação

```python
# Linha máxima: 88 caracteres (Black formatter)
# Indentação: 4 espaços (não tabs)

# ✅ BOM
def funcao_exemplo(parametro1, parametro2):
    """Docstring explicando a função."""
    resultado = parametro1 + parametro2
    return resultado

# ❌ RUIM
def FuncaoExemplo(p1,p2):
    return p1+p2
```

#### Nomenclatura

```python
# Classes: PascalCase
class MinhaClasse:
    pass

# Funções e variáveis: snake_case
def minha_funcao():
    minha_variavel = 10

# Constantes: UPPER_SNAKE_CASE
TIMEOUT_PADRAO = 30
```

#### Imports

```python
# Ordem dos imports:
# 1. Biblioteca padrão
# 2. Bibliotecas de terceiros
# 3. Módulos locais

import os
import sys
from datetime import datetime

import selenium
from selenium.webdriver.common.by import By

from meu_modulo import MinhaClasse
```

#### Docstrings

```python
def extrair_dados(numero_bd):
    """
    Extrai dados de um chamado do SIGTM.
    
    Args:
        numero_bd (str): Número do BD a ser buscado
        
    Returns:
        dict: Dicionário com dados extraídos ou None se falhar
        
    Raises:
        TimeoutException: Se elemento não for encontrado
        
    Example:
        >>> dados = extrair_dados("BD123456")
        >>> print(dados['razao_social'])
        'Empresa XYZ'
    """
    pass
```

#### Type Hints

```python
from typing import Optional, Dict, List

def processar_carimbo(
    dados: Dict[str, str],
    task: Optional[str] = None,
    sfa: Optional[str] = None
) -> str:
    """Processa e retorna carimbo formatado."""
    pass
```

### Tkinter Guidelines

```python
# Use ttk quando possível (visual melhor)
from tkinter import ttk

# ✅ Preferir
button = ttk.Button(parent, text="Clique", style='Vivo.TButton')

# ❌ Evitar
button = tk.Button(parent, text="Clique")

# Organize widgets logicamente
frame_principal = ttk.Frame(root)
frame_header = ttk.Frame(frame_principal)
frame_conteudo = ttk.Frame(frame_principal)
```

### Selenium Best Practices

```python
# ✅ Use WebDriverWait ao invés de time.sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

elemento = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "meu_id"))
)

# ❌ Evite
import time
time.sleep(5)
driver.find_element(By.ID, "meu_id")

# ✅ Sempre faça cleanup
try:
    driver.get(url)
    # ... operações ...
finally:
    driver.quit()
```

---

## Commit Guidelines

### Formato de Commit

Usamos [Conventional Commits](https://www.conventionalcommits.org/):

```
<tipo>(<escopo>): <descrição curta>

[corpo opcional]

[rodapé opcional]
```

### Tipos de Commit

| Tipo | Descrição | Exemplo |
|------|-----------|---------|
| `feat` | Nova funcionalidade | `feat(busca): adiciona busca em lote` |
| `fix` | Correção de bug | `fix(login): corrige erro ao reconectar` |
| `docs` | Apenas documentação | `docs(readme): atualiza instruções` |
| `style` | Formatação (sem mudança de código) | `style: aplica black formatter` |
| `refactor` | Refatoração | `refactor(extração): simplifica lógica` |
| `perf` | Melhoria de performance | `perf(busca): otimiza query DOM` |
| `test` | Adicionar testes | `test(carimbo): adiciona testes unitários` |
| `chore` | Tarefas de manutenção | `chore: atualiza dependências` |

### Exemplos de Commits

**Bom:**
```bash
git commit -m "feat(ui): adiciona botão de exportar para Excel

Implementa funcionalidade de exportação de carimbos para arquivo Excel.
Inclui validação de dados antes da exportação.

Closes #42"
```

**Ruim:**
```bash
git commit -m "mudanças"
git commit -m "fix"
git commit -m "WIP"
```

### Dicas

- Use verbos no imperativo ("adiciona", não "adicionado")
- Primeira linha com até 50 caracteres
- Corpo da mensagem com até 72 caracteres por linha
- Referencie issues relacionadas

---

## Pull Request Process

### Checklist Antes de Abrir PR

- [ ] Código segue os padrões do projeto
- [ ] Commits seguem o Conventional Commits
- [ ] Documentação atualizada (se necessário)
- [ ] Testes passando (quando aplicável)
- [ ] Branch atualizada com develop/main
- [ ] Sem conflitos

### Abrindo um Pull Request

**1. Atualize sua Branch**
```bash
git checkout develop
git pull upstream develop
git checkout sua-branch
git rebase develop
```

**2. Push para seu Fork**
```bash
git push origin sua-branch
```

**3. Abra PR no GitHub**

Use o template:

```markdown
## Descrição
Breve descrição das mudanças

## Tipo de Mudança
- [ ] Bugfix (correção de bug)
- [ ] Feature (nova funcionalidade)
- [ ] Breaking change (mudança incompatível)
- [ ] Documentação

## Como Testar
Passos para testar as mudanças:
1. ...
2. ...

## Screenshots (se aplicável)
![descrição](url-da-imagem)

## Checklist
- [ ] Código segue os padrões
- [ ] Commits convencionais
- [ ] Documentação atualizada
- [ ] Testes passando

## Issues Relacionadas
Closes #123
Relates to #456
```

### Processo de Review

1. **Mantenedor revisa** o código
2. **Feedback** é fornecido via comentários
3. **Autor atualiza** baseado no feedback
4. **Aprovação** quando tudo estiver OK
5. **Merge** para develop/main

### Após o Merge

```bash
# Atualize seu fork
git checkout develop
git pull upstream develop
git push origin develop

# Delete a branch
git branch -d sua-branch
git push origin --delete sua-branch
```

---

## Reportando Bugs

### Template de Bug Report

```markdown
**Descrição do Bug**
Descrição clara e concisa do problema.

**Passos para Reproduzir**
1. Vá para '...'
2. Clique em '...'
3. Digite '...'
4. Veja o erro

**Comportamento Esperado**
O que deveria acontecer.

**Comportamento Atual**
O que realmente acontece.

**Screenshots**
Se aplicável, adicione screenshots.

**Ambiente:**
 - OS: [Windows 10]
 - Python: [3.9.0]
 - Chrome: [120.0.6099.109]
 - Versão da Aplicação: [1.0.0]

**Informações Adicionais**
Qualquer outra informação relevante.

**Logs (se disponível)**
```
[cole logs aqui]
```
```

### Severity Levels

| Nível | Descrição | Exemplo |
|-------|-----------|---------|
| 🔴 Critical | Sistema não funciona | Crash ao iniciar |
| 🟠 High | Funcionalidade principal quebrada | Login não funciona |
| 🟡 Medium | Funcionalidade secundária com problema | Botão copiar falha às vezes |
| 🟢 Low | Problema cosmético | Alinhamento de texto |

---

## Sugerindo Melhorias

### Template de Feature Request

```markdown
**A Funcionalidade Resolve Algum Problema?**
Descrição clara do problema. Ex: "Sempre fico frustrado quando [...]"

**Descreva a Solução Desejada**
Descrição clara do que você quer que aconteça.

**Descreva Alternativas Consideradas**
Outras soluções ou funcionalidades que você considerou.

**Benefícios Esperados**
- Benefício 1
- Benefício 2

**Complexidade Estimada**
- [ ] Simples (poucas horas)
- [ ] Média (alguns dias)
- [ ] Complexa (semanas)

**Mockups/Wireframes (opcional)**
Se você tiver imagens ou desenhos, adicione aqui.

**Informações Adicionais**
Qualquer outro contexto ou screenshots.
```

---

## Recursos Adicionais

### Documentação
- [README Principal](README.md)
- [Arquitetura Técnica](ARQUITETURA.md)
- [Guia de Instalação](INSTALACAO.md)
- [Changelog](CHANGELOG.md)

### Ferramentas Recomendadas
- **IDE:** VS Code, PyCharm
- **Linting:** pylint, flake8
- **Formatação:** black, autopep8
- **Type Checking:** mypy
- **Git GUI:** GitKraken, Sourcetree

### Links Úteis
- [PEP 8](https://pep8.org/)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Semantic Versioning](https://semver.org/)
- [Git Flow](https://nvie.com/posts/a-successful-git-branching-model/)

---

## Perguntas?

Se você tiver dúvidas sobre como contribuir:

1. Verifique a [documentação](README.md)
2. Procure em [issues existentes](https://github.com/seu-usuario/automacao-ge-yellowbelt/issues)
3. Abra uma [nova issue](https://github.com/seu-usuario/automacao-ge-yellowbelt/issues/new) com a tag `question`
4. Entre em contato: seu.email@exemplo.com

---

## Agradecimentos

Obrigado por dedicar seu tempo para contribuir! 🎉

Cada contribuição, por menor que seja, é valiosa e apreciada.

---

**Mantido por:** Leonardo Mattana  
**Projeto:** Yellow Belt - Automação GE  
**Última atualização:** 2024
