# 📚 Exemplos de Uso

Este documento apresenta exemplos práticos de uso da Automação GE em diferentes cenários do dia a dia.

---

## 📑 Índice

1. [Casos de Uso Comuns](#casos-de-uso-comuns)
2. [Fluxos de Trabalho](#fluxos-de-trabalho)
3. [Exemplos de Carimbos Gerados](#exemplos-de-carimbos-gerados)
4. [Resolução de Problemas](#resolução-de-problemas)
5. [Dicas e Truques](#dicas-e-truques)

---

## Casos de Uso Comuns

### Caso 1: Busca Simples de Chamado

**Cenário:** Você recebeu um número de BD e precisa gerar um carimbo básico.

**Passos:**

```
1. Conectar ao SIGTM
   ├─ Usuário: seu.usuario
   ├─ Senha: sua.senha
   └─ Clique: CONECTAR SIGTM
   
2. Aguardar confirmação
   └─ Status: "✅ Pronto para buscar chamados!"
   
3. Inserir dados mínimos
   ├─ Número do BD: BD123456
   ├─ TASK: (vazio - opcional)
   └─ SFA: (vazio - opcional)
   
4. Buscar
   └─ Clique: BUSCAR CHAMADO
   
5. Aguardar extração (~15 segundos)
   
6. Copiar carimbo
   └─ Clique: COPIAR CARIMBO
```

**Resultado:**
```
***** CARIMBO GESTAO DE EXPECTATIVA TOP *****
TASK: 
SFA: 
SIGITM: BD123456
Nome do Cliente: João Silva
Contato: 11987654321 / 1133334444
CNPJ: 12.345.678/0001-90
Razão Social: EMPRESA EXEMPLO LTDA
Designador Responsável: 551133334444 INDISPONIBILIDADE PARCIAL

***** CARIMBO GESTAO DE EXPECTATIVA TOP *****
TASK: 
SIGITM: BD123456

Ação Realizada / Tentativas de contato: 

--------------------------------------------------------
```

**Tempo Total:** ~30 segundos

---

### Caso 2: Busca com TASK e SFA

**Cenário:** Chamado associado a uma TASK específica e SFA.

**Dados de Entrada:**
```
BD: BD789012
TASK: TASK-2024-001
SFA: SFA12345
```

**Carimbo Gerado:**
```
***** CARIMBO GESTAO DE EXPECTATIVA TOP *****
TASK: TASK-2024-001
SFA: SFA12345
SIGITM: BD789012
Nome do Cliente: Maria Santos
Contato: 21987654321 / 2133334444
CNPJ: 98.765.432/0001-10
Razão Social: SERVICOS EXEMPLO S/A
Designador Responsável: 552133334444 INDISPONIBILIDADE TOTAL

***** CARIMBO GESTAO DE EXPECTATIVA TOP *****
TASK: TASK-2024-001
SIGITM: BD789012

Ação Realizada / Tentativas de contato: 

--------------------------------------------------------
```

---

### Caso 3: Múltiplos Chamados Sequenciais

**Cenário:** Você precisa processar vários BDs em sequência.

**Workflow Otimizado:**

```
1. Conectar SIGTM (uma vez)

2. Para cada BD:
   ├─ Inserir número do BD
   ├─ Inserir TASK/SFA (se aplicável)
   ├─ BUSCAR CHAMADO
   ├─ Aguardar resultado
   ├─ COPIAR CARIMBO
   ├─ Colar no sistema de destino
   └─ LIMPAR campos (opcional)
   
3. Ao final: SAIR
```

**Exemplo de Lote:**
```
BD345678 → Processar → Copiar → Próximo
BD456789 → Processar → Copiar → Próximo
BD567890 → Processar → Copiar → Próximo
```

**Tempo Economizado:**
- Manual: 3 BDs × 6 min = 18 minutos
- Automatizado: 3 BDs × 0.5 min = 1.5 minutos
- **Ganho: 16.5 minutos (91%)**

---

## Fluxos de Trabalho

### Workflow 1: Gestão de Expectativa Padrão

```
┌─────────────────────────────────────────┐
│ 1. Receber Demanda de Gestão            │
│    (Email, Slack, Sistema)              │
└───────────────┬─────────────────────────┘
                │
                ▼
┌─────────────────────────────────────────┐
│ 2. Abrir Automação GE                   │
│    - Conectar ao SIGTM                  │
└───────────────┬─────────────────────────┘
                │
                ▼
┌─────────────────────────────────────────┐
│ 3. Processar Chamado                    │
│    - Inserir BD/TASK/SFA                │
│    - Buscar e extrair dados             │
└───────────────┬─────────────────────────┘
                │
                ▼
┌─────────────────────────────────────────┐
│ 4. Analisar Carimbo                     │
│    - Verificar dados extraídos          │
│    - Validar informações de contato     │
└───────────────┬─────────────────────────┘
                │
                ▼
┌─────────────────────────────────────────┐
│ 5. Realizar Ações                       │
│    - Copiar carimbo                     │
│    - Contatar cliente                   │
│    - Documentar no sistema              │
└───────────────┬─────────────────────────┘
                │
                ▼
┌─────────────────────────────────────────┐
│ 6. Follow-up                            │
│    - Acompanhar escalonamento           │
│    - Atualizar status                   │
└─────────────────────────────────────────┘
```

---

### Workflow 2: Troubleshooting de Chamado

```
Chamado com Dados Incompletos
    │
    ├─ Executar Busca Normal
    │   └─ Alguns campos: "Não encontrado"
    │
    ├─ Analisar Carimbo
    │   ├─ CNPJ: ✅ Encontrado
    │   ├─ Razão Social: ✅ Encontrado
    │   ├─ Contato: ❌ Não encontrado
    │   └─ Telefone: ❌ Não encontrado
    │
    ├─ Ações Alternativas
    │   ├─ Buscar no sistema legado
    │   ├─ Contatar via email
    │   └─ Documentar ausência de dados
    │
    └─ Usar carimbo parcial
        └─ Preencher manualmente campos faltantes
```

---

## Exemplos de Carimbos Gerados

### Exemplo 1: Carimbo Completo

**Entrada:**
- BD: BD123456
- TASK: TASK-2024-042
- SFA: SFA98765

**Saída:**
```
***** CARIMBO GESTAO DE EXPECTATIVA TOP *****
TASK: TASK-2024-042
SFA: SFA98765
SIGITM: BD123456
Nome do Cliente: Carlos Eduardo Oliveira
Contato: 11987654321 / 1140028922
CNPJ: 12.345.678/0001-90
Razão Social: TECNOLOGIA EXEMPLO LTDA
Designador Responsável: 551140028922 INDISPONIBILIDADE PARCIAL

***** CARIMBO GESTAO DE EXPECTATIVA TOP *****
TASK: TASK-2024-042
SIGITM: BD123456

Ação Realizada / Tentativas de contato: 

--------------------------------------------------------
```

**Uso:**
1. Colar em ticket de atendimento
2. Adicionar ações realizadas manualmente
3. Enviar atualização ao cliente

---

### Exemplo 2: Carimbo com Dados Parciais

**Entrada:**
- BD: BD654321
- TASK: (vazio)
- SFA: (vazio)

**Sistema não encontrou:**
- Telefone 2
- Designador (formato diferente)

**Saída:**
```
***** CARIMBO GESTAO DE EXPECTATIVA TOP *****
TASK: 
SFA: 
SIGITM: BD654321
Nome do Cliente: Ana Paula Costa
Contato: 21987654321 / 
CNPJ: 98.765.432/0001-10
Razão Social: CONSULTORIA EXEMPLO S/A
Designador Responsável:  LINHA TELEFONICA MUDA

***** CARIMBO GESTAO DE EXPECTATIVA TOP *****
TASK: 
SIGITM: BD654321

Ação Realizada / Tentativas de contato: 

--------------------------------------------------------
```

**Ação:**
- Complementar manualmente campos vazios
- Ou usar informações disponíveis

---

### Exemplo 3: Múltiplos Formatos de CNPJ

O sistema tenta 3 localizadores diferentes para CNPJ:

**Tentativa 1:**
```python
cnpj = safe_find_value("input[id$=':tisClienteCnpj']")
# Resultado: "12.345.678/0001-90"
```

**Se falhar, Tentativa 2:**
```python
cnpj = safe_find_value("input[id$=':tisClienteCnpj01']")
# Resultado: "12345678000190" (sem formatação)
```

**Se falhar, Tentativa 3:**
```python
cnpj = safe_find_value("input[id$=':ddrtisClienteNumNrf']")
# Resultado: CNPJ alternativo
```

---

## Resolução de Problemas

### Problema 1: "Não foi possível extrair dados"

**Sintomas:**
- Mensagem de erro após busca
- Carimbo não é gerado

**Possíveis Causas e Soluções:**

```
Causa 1: BD inexistente
├─ Sintoma: Sistema retorna página vazia
├─ Solução: Verificar número do BD
└─ Ação: Digitar novamente com atenção

Causa 2: Timeout de conexão
├─ Sintoma: Demora excessiva (>30 seg)
├─ Solução: Reconectar ao SIGTM
└─ Ação: Clicar em RECONECTAR

Causa 3: Mudança na estrutura do SIGTM
├─ Sintoma: Campos "Não encontrado" em massa
├─ Solução: Atualizar seletores CSS
└─ Ação: Reportar issue no GitHub
```

---

### Problema 2: Campos "Não encontrado"

**Exemplo de Saída:**
```
Nome do Cliente: Não encontrado
Contato: Não encontrado / Não encontrado
CNPJ: 12.345.678/0001-90
```

**Interpretação:**
- ✅ CNPJ foi encontrado normalmente
- ❌ Nome e Contato não existem neste chamado específico

**Ações:**
```
1. Verificar no SIGTM manualmente se dados existem
2. Se existem mas não foram encontrados:
   └─ Reportar bug com número do BD
3. Se não existem:
   └─ Usar carimbo parcial ou buscar em outro sistema
```

---

### Problema 3: Erro ao Conectar

**Mensagem:**
```
❌ Erro ao conectar: Message: session not created: This version of 
ChromeDriver only supports Chrome version 120
```

**Solução:**
```
1. Verificar versão do Chrome:
   Chrome → Ajuda → Sobre o Google Chrome
   
2. Baixar ChromeDriver compatível:
   https://chromedriver.chromium.org/downloads
   
3. Substituir chromedriver.exe:
   - Fechar aplicação
   - Substituir arquivo
   - Reabrir aplicação
```

---

## Dicas e Truques

### Dica 1: Atalhos de Teclado

```
Ctrl+C  → Copiar texto selecionado
Ctrl+V  → Colar texto
Ctrl+A  → Selecionar tudo (em campos de texto)
Tab     → Navegar entre campos
Enter   → Confirmar (em alguns campos)
```

### Dica 2: Copiar Dados de Entrada Rapidamente

**Cenário:** Você quer salvar BD/TASK/SFA para referência futura.

**Método:**
```
1. Preencher campos normalmente
2. Clicar em COPIAR ENTRADA (acima de BUSCAR CHAMADO)
3. Colar em documento de acompanhamento
```

**Resultado Copiado:**
```
BD: BD123456
TASK: TASK-2024-042
SFA: SFA98765
```

---

### Dica 3: Manter Sessão Ativa

**Problema:** Sessão SIGTM expira após inatividade.

**Solução:**
```
- Não feche a janela do Chrome automatizado
- Se precisar afastar, clique em RECONECTAR ao voltar
- Em longas pausas, faça logout e login novamente
```

---

### Dica 4: Validação Visual Rápida

Antes de copiar o carimbo, verifique rapidamente:

```
Checklist de Validação:
✓ CNPJ tem 14 dígitos?
✓ Telefones têm formato válido?
✓ Razão Social está preenchida?
✓ Designador faz sentido?
✓ Data de escalonamento está correta (+4h)?
```

---

### Dica 5: Personalizar Carimbo Após Copiar

**Workflow:**
```
1. Copiar carimbo gerado
2. Colar em editor de texto (Notepad++)
3. Preencher seção "Ação Realizada":
   
   Exemplo:
   Ação Realizada / Tentativas de contato:
   - 14:30 - Ligação realizada, sem atendimento
   - 14:45 - Enviado email para contato@empresa.com
   - 15:00 - Aguardando retorno
   
4. Copiar versão final
5. Colar no sistema de tickets
```

---

### Dica 6: Organização para Alto Volume

**Para processar 20+ chamados/dia:**

```
1. Preparar planilha de controle:
   ┌────────┬──────────┬────────┬────────────┐
   │   BD   │   TASK   │  SFA   │   Status   │
   ├────────┼──────────┼────────┼────────────┤
   │ 123456 │ TASK-001 │ SFA123 │ Processado │
   │ 234567 │ TASK-002 │ SFA124 │ Processado │
   └────────┴──────────┴────────┴────────────┘

2. Processar em lote:
   - 5-10 chamados por vez
   - Pausa para validação
   - Continuar próximo lote

3. Marcar processados:
   - Atualizar planilha
   - Evitar duplicatas
```

---

## Casos Especiais

### Caso 1: BD com Múltiplos Designadores

**Situação:** Chamado com vários terminais afetados.

**O que acontece:**
- Sistema captura apenas primeiro designador
- Outros aparecem no sistema mas não no carimbo

**Solução:**
```
1. Gerar carimbo normalmente
2. Acessar SIGTM manualmente
3. Copiar designadores adicionais
4. Adicionar ao carimbo:
   
   Designador Responsável: 551140028922 INDISPONIBILIDADE
   Designadores Adicionais: 551140028923, 551140028924
```

---

### Caso 2: Reclamação com Caracteres Especiais

**Situação:** Reclamação com acentos ou símbolos.

**Exemplo:**
```
Original: INTERRUPÇÃO DA COMUNICAÇÃO
Extraído: INTERRUPÃ‡ÃƒO DA COMUNICAÃ‡ÃƒO
```

**Causa:** Encoding UTF-8 vs ISO-8859-1

**Solução Temporária:**
```
Corrigir manualmente após copiar carimbo
```

**Solução Permanente:**
```python
# Adicionar no código (futuro):
texto = texto.encode('iso-8859-1').decode('utf-8')
```

---

## Métricas de Uso

### Tracking de Produtividade

**Antes da Automação (manual):**
```
Tempo por chamado: 6 min
Chamados/hora: 10
Chamados/dia (8h): 80
Erros/dia: 12 (15%)
```

**Depois da Automação:**
```
Tempo por chamado: 0.5 min
Chamados/hora: 120
Chamados/dia (8h): 960 (teórico)
Chamados/dia (real): 150 (com pausas)
Erros/dia: 2 (<2%)
```

**Ganho Real:**
```
Aumento de produtividade: 87.5%
Redução de erros: 83.3%
Tempo economizado/dia: 4.5 horas
```

---

## Feedback e Melhorias

Encontrou um caso de uso não coberto aqui? 

1. Abra uma [issue](https://github.com/seu-usuario/automacao-ge-yellowbelt/issues)
2. Descreva o cenário
3. Sugerir como documentar

Suas contribuições ajudam a melhorar este guia!

---

**Desenvolvido por:** Leonardo Mattana  
**Projeto:** Yellow Belt - Automação GE  
**Última atualização:** 2024
