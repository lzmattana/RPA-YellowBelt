# 🏗️ Arquitetura Técnica - Automação GE

## Visão Geral da Arquitetura

Este documento detalha a arquitetura técnica do sistema de automação, explicando decisões de design, padrões implementados e fluxos de dados.

---

## Índice

1. [Stack Tecnológica](#stack-tecnológica)
2. [Padrões de Design](#padrões-de-design)
3. [Componentes do Sistema](#componentes-do-sistema)
4. [Fluxo de Dados](#fluxo-de-dados)
5. [Gerenciamento de Estado](#gerenciamento-de-estado)
6. [Threading e Concorrência](#threading-e-concorrência)
7. [Tratamento de Erros](#tratamento-de-erros)
8. [Segurança](#segurança)

---

## Stack Tecnológica

### Linguagem Core
**Python 3.8+**
- Escolha baseada em: produtividade, bibliotecas ricas, facilidade de manutenção
- Type hints utilizados para melhor documentação
- Compatível com Windows (ambiente corporativo)

### Framework de Automação
**Selenium WebDriver 4.0+**
- Automação de navegador multiplataforma
- Suporte a JavaScript dinâmico
- API robusta para localização de elementos
- WebDriverWait para sincronização

### Interface Gráfica
**Tkinter (Python Standard Library)**
- Nativa do Python (sem dependências extras)
- Cross-platform
- Leve e responsiva
- Customizável com ttk

### Browser Driver
**ChromeDriver**
- Compatível com Google Chrome
- Protocolo WebDriver W3C
- Versionamento alinhado com Chrome

---

## Padrões de Design

### 1. Single Responsibility Principle (SRP)

Cada módulo tem uma responsabilidade única:

```python
# Módulo de Interface
setup_styles()           # Apenas estilos
setup_main_interface()   # Apenas construção UI

# Módulo de Conexão
connect_sigtm()          # Apenas autenticação
_connect_sigtm_thread()  # Apenas conexão assíncrona

# Módulo de Busca
search_ticket()          # Apenas orquestração
extract_ticket_data()    # Apenas extração
```

### 2. Separation of Concerns

```
┌─────────────────────────────────────┐
│      Presentation Layer             │  ← Tkinter UI
├─────────────────────────────────────┤
│      Business Logic Layer           │  ← Processamento
├─────────────────────────────────────┤
│      Data Access Layer              │  ← Selenium
├─────────────────────────────────────┤
│      External System                │  ← SIGTM
└─────────────────────────────────────┘
```

### 3. Facade Pattern

A classe `SIGTMApp` atua como fachada:

```python
class SIGTMApp:
    """
    Fachada que simplifica interação com:
    - Selenium WebDriver
    - Tkinter GUI
    - Threading
    - Data Processing
    """
```

### 4. Template Method Pattern

Geração de carimbos usa template:

```python
template = """***** CARIMBO GESTAO DE EXPECTATIVA TOP *****
TASK: {task}
SFA: {sfa}
...
"""
# Método preenche template com dados
```

### 5. Dependency Injection

WebDriver injetado como dependência:

```python
self.driver = webdriver.Chrome(service=service, options=options)
self.wait = WebDriverWait(self.driver, 15)
```

---

## Componentes do Sistema

### Diagrama de Classes

```
┌────────────────────────────────────────┐
│          SIGTMApp                      │
├────────────────────────────────────────┤
│ - root: tk.Tk                          │
│ - driver: WebDriver                    │
│ - wait: WebDriverWait                  │
│ - is_logged_in: bool                   │
│ - colors: dict                         │
│ - UI widgets: Entry, Button, Text      │
├────────────────────────────────────────┤
│ + __init__()                           │
│ + setup_styles()                       │
│ + show_main_application()              │
│ + setup_main_interface()               │
│ + make_context_menu()                  │
│ + connect_sigtm()                      │
│ + _connect_sigtm_thread()              │
│ + search_ticket()                      │
│ + _search_ticket_thread()              │
│ + extract_ticket_data()                │
│ + safe_find_value()                    │
│ + calcular_escalonamento()             │
│ + generate_stamp()                     │
│ + copy_stamp()                         │
│ + copy_input_data()                    │
│ + clear_result()                       │
│ + update_status()                      │
│ + logout()                             │
│ + run()                                │
└────────────────────────────────────────┘
```

### Componentes Detalhados

#### 1. Interface Module

**Responsabilidade**: Gerenciar toda a camada de apresentação

```python
# Estrutura de Widgets
main_frame (TFrame)
├── header_frame
│   ├── title_label
│   ├── status_label
│   └── logout_btn
├── controls_frame
│   ├── login_section (LabelFrame)
│   │   ├── sigtm_user_entry
│   │   ├── sigtm_pass_entry
│   │   └── connect_btn
│   └── search_section (LabelFrame)
│       ├── bd_entry
│       ├── task_entry
│       ├── sfa_entry
│       └── search_btn
├── result_frame (LabelFrame)
│   ├── result_text (ScrolledText)
│   └── action_buttons
└── footer_frame
```

#### 2. Connection Module

**Responsabilidade**: Gerenciar conexão com SIGTM

```python
Fluxo de Conexão:
1. Validar credenciais
2. Iniciar ChromeDriver
3. Navegar para login
4. Preencher formulário
5. Submeter e validar
6. Navegar para busca
7. Atualizar estado
```

#### 3. Search Module

**Responsabilidade**: Buscar e extrair dados

```python
Campos Extraídos:
- data_criacao         (input[id$=':DataCriacao'])
- razao_social         (input[id$=':tisClienteTitular'])
- cnpj                 (input[id$=':tisClienteCnpj'])
- contato_nome         (input[id$=':tqiContatoNome'])
- tel1, tel2           (input[id$=':tqiReclamanteTelefone'])
- designador           (input[id$=':ddrtisClienteTerminal'])
- reclamacao           (input[id$=':reiNome'])
```

**Estratégia de Busca**: Múltiplos seletores com fallback

```python
# Exemplo: CNPJ tem 3 possíveis localizações
cnpj = safe_find_value("input[id$=':tisClienteCnpj']")
if cnpj == "Não encontrado":
    cnpj = safe_find_value("input[id$=':tisClienteCnpj01']")
if cnpj == "Não encontrado":
    cnpj = safe_find_value("input[id$=':ddrtisClienteNumNrf']")
```

#### 4. Processing Module

**Responsabilidade**: Processar e formatar dados

```python
Pipeline de Processamento:
1. Receber dados brutos
2. Calcular escalonamento (+4h)
3. Limpar valores "Não encontrado"
4. Preencher template
5. Formatar saída
```

---

## Fluxo de Dados

### Fluxo Completo End-to-End

```
┌─────────────┐
│   Usuário   │
└──────┬──────┘
       │ 1. Insere credenciais
       ▼
┌─────────────────────────────┐
│   Interface (Tkinter)        │
└──────┬──────────────────────┘
       │ 2. Valida entrada
       ▼
┌─────────────────────────────┐
│   Connection Thread          │
│   (Threading)                │
└──────┬──────────────────────┘
       │ 3. Inicia WebDriver
       ▼
┌─────────────────────────────┐
│   Selenium WebDriver         │
└──────┬──────────────────────┘
       │ 4. HTTP Request
       ▼
┌─────────────────────────────┐
│   Sistema SIGTM              │
│   (Aplicação Web)            │
└──────┬──────────────────────┘
       │ 5. Retorna HTML
       ▼
┌─────────────────────────────┐
│   Data Extraction            │
│   (CSS Selectors)            │
└──────┬──────────────────────┘
       │ 6. Dados estruturados
       ▼
┌─────────────────────────────┐
│   Business Logic             │
│   (Processamento)            │
└──────┬──────────────────────┘
       │ 7. Carimbo formatado
       ▼
┌─────────────────────────────┐
│   Interface (Display)        │
└──────┬──────────────────────┘
       │ 8. Exibe resultado
       ▼
┌─────────────┐
│   Usuário   │
└─────────────┘
```

### Fluxo de Estados

```
[INICIAL]
    │
    ├─> [CONECTANDO]
    │       │
    │       ├─> [ERRO_LOGIN] ─> [INICIAL]
    │       │
    │       └─> [CONECTADO]
    │               │
    │               ├─> [BUSCANDO]
    │               │       │
    │               │       ├─> [ERRO_BUSCA] ─> [CONECTADO]
    │               │       │
    │               │       └─> [DADOS_EXTRAIDOS]
    │               │               │
    │               │               └─> [CARIMBO_GERADO] ─> [CONECTADO]
    │               │
    │               └─> [DESCONECTADO] ─> [INICIAL]
```

---

## Gerenciamento de Estado

### Variáveis de Estado

```python
class SIGTMApp:
    # Estados principais
    self.driver: WebDriver | None      # Instância do navegador
    self.wait: WebDriverWait | None    # Gerenciador de espera
    self.is_logged_in: bool            # Status de autenticação
    
    # Estados de UI
    self.root: tk.Tk                   # Janela principal
    self.status_label: ttk.Label       # Label de status
    self.search_btn: ttk.Button        # Botão de busca
    self.connect_btn: ttk.Button       # Botão de conexão
```

### Transições de Estado

```python
# Exemplo: Transição de Desconectado → Conectado
def _connect_sigtm_thread():
    # Estado: CONECTANDO
    self.connect_btn.config(state='disabled')
    
    # Operação
    self.driver = webdriver.Chrome(...)
    # ... login logic ...
    
    # Estado: CONECTADO
    self.is_logged_in = True
    self.search_btn.config(state='normal')
    self.connect_btn.config(text="RECONECTAR", state='normal')
```

---

## Threading e Concorrência

### Modelo de Threading

**Main Thread (GUI)**
- Gerencia interface Tkinter
- Responde a eventos do usuário
- Atualiza widgets

**Worker Threads**
- Executam operações bloqueantes
- Interagem com Selenium
- Processam dados

### Pattern: Thread-Safe UI Updates

```python
# INCORRETO - Atualizar UI de thread worker
def worker():
    messagebox.showinfo(...)  # ❌ Pode causar crash

# CORRETO - Usar root.after()
def worker():
    self.root.after(0, lambda: messagebox.showinfo(...))  # ✅
```

### Exemplo de Threading Seguro

```python
def connect_sigtm(self):
    """Método chamado pela UI (Main Thread)"""
    # Validação leve na main thread
    username = self.sigtm_user_entry.get().strip()
    password = self.sigtm_pass_entry.get().strip()
    
    if not username or not password:
        messagebox.showerror(...)  # OK - na main thread
        return
    
    # Delega trabalho pesado para worker thread
    threading.Thread(
        target=self._connect_sigtm_thread,
        args=(username, password),
        daemon=True
    ).start()

def _connect_sigtm_thread(self, username, password):
    """Worker thread - operações bloqueantes"""
    try:
        # Atualiza UI via root.after (thread-safe)
        self.root.after(0, lambda: self.update_status("Conectando..."))
        
        # Operação bloqueante (OK em worker thread)
        self.driver = webdriver.Chrome(...)
        self.driver.get("http://...")
        
        # Atualiza UI novamente
        self.root.after(0, lambda: self.search_btn.config(state='normal'))
    except Exception as e:
        # Exibe erro via root.after
        self.root.after(0, lambda: messagebox.showerror(...))
```

### Daemon Threads

```python
threading.Thread(..., daemon=True).start()
```
- **daemon=True**: Thread morre quando programa principal termina
- Evita threads "órfãs" bloqueando o encerramento
- Apropriado para operações de background

---

## Tratamento de Erros

### Hierarquia de Exceções

```
Exception
├── TimeoutException (Selenium)
│   └── Elemento não encontrado no tempo limite
├── NoSuchElementException (Selenium)
│   └── Elemento não existe no DOM
├── WebDriverException (Selenium)
│   └── Erro geral do WebDriver
└── ValueError (Python)
    └── Erro ao processar data
```

### Estratégias de Tratamento

#### 1. Graceful Degradation

```python
def safe_find_value(self, selector):
    """Retorna valor ou 'Não encontrado' sem falhar"""
    try:
        WebDriverWait(self.driver, 2).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, selector))
        )
        return self.driver.find_element(...).get_attribute("value")
    except (NoSuchElementException, TimeoutException):
        return "Não encontrado"  # Degradação graciosa
```

#### 2. Retry with Fallback

```python
# Tenta 3 seletores diferentes para CNPJ
cnpj = safe_find_value("input[id$=':tisClienteCnpj']")
if cnpj == "Não encontrado":
    cnpj = safe_find_value("input[id$=':tisClienteCnpj01']")
if cnpj == "Não encontrado":
    cnpj = safe_find_value("input[id$=':ddrtisClienteNumNrf']")
```

#### 3. User Feedback

```python
try:
    # Operação crítica
    self.driver.get(url)
except Exception as e:
    # Informa usuário com detalhes
    messagebox.showerror(
        "Erro",
        f"❌ Erro ao conectar: {str(e)}"
    )
```

#### 4. Cleanup em Finally

```python
try:
    # Operações
    ...
except Exception as e:
    # Tratamento
    ...
finally:
    # Sempre executa cleanup
    if len(self.driver.window_handles) > 1:
        self.driver.close()
        self.driver.switch_to.window(original_window)
```

---

## Segurança

### 1. Credenciais

**❌ NÃO armazenadas em:**
- Código-fonte
- Arquivos de configuração versionados
- Logs

**✅ Solicitadas em runtime:**
```python
# Usuário insere credenciais na UI
username = self.sigtm_user_entry.get().strip()
password = self.sigtm_pass_entry.get().strip()
```

**Campo de senha ofuscado:**
```python
self.sigtm_pass_entry = ttk.Entry(..., show='*')
```

### 2. Firewall Corporativo

**Desabilitação de verificação SSL (apenas para ChromeDriver download):**
```python
os.environ['WDM_SSL_VERIFY'] = '0'
```
⚠️ Nota: Apenas para contornar proxy corporativo, não afeta segurança da aplicação

### 3. Sessões

**Não persistidas:**
- Sessão encerrada ao fechar aplicação
- Sem cookies salvos
- WebDriver destruído no logout

```python
def logout(self):
    if self.driver:
        self.driver.quit()  # Encerra sessão completamente
    self.root.destroy()
```

### 4. Inputs

**Validação básica:**
```python
if not username or not password:
    messagebox.showerror("Erro", "Preencha todos os campos!")
    return
```

**Sanitização:**
```python
username = self.sigtm_user_entry.get().strip()  # Remove espaços
```

---

## Considerações de Performance

### 1. WebDriverWait vs time.sleep

**✅ Preferir WebDriverWait (inteligente):**
```python
self.wait.until(EC.presence_of_element_located((By.ID, "elemento")))
```
- Aguarda condição específica
- Retorna assim que satisfeita
- Não desperdiça tempo

**⚠️ Evitar time.sleep (fixo):**
```python
time.sleep(3)  # Sempre espera 3s, mesmo se pronto em 1s
```
- Usado apenas quando necessário (ex: após submit)

### 2. Localizadores CSS

**Rápidos e eficientes:**
```python
By.CSS_SELECTOR, "input[id$=':DataCriacao']"
```
- Nativamente suportados por navegadores
- Mais rápidos que XPath em muitos casos

### 3. Minimizar DOM Queries

**Cache de elementos quando possível:**
```python
# Busca uma vez
campo_tiquete = self.wait.until(
    EC.presence_of_element_located((By.ID, "formLocalizar:tqiCodigo"))
)
# Reutiliza
campo_tiquete.clear()
campo_tiquete.send_keys(numero_bd)
```

---

## Deployment

### Build do Executável

**PyInstaller configuração:**
```bash
pyinstaller --onefile --windowed --icon=icon.ico automacao_ge.py
```

**Estrutura do bundle:**
```
dist/
└── AutomacaoGE.exe       # Executável standalone
```

**Incluir chromedriver:**
```python
if getattr(sys, 'frozen', False):
    # Executável PyInstaller
    application_path = os.path.dirname(sys.executable)
else:
    # Script Python
    application_path = os.path.dirname(os.path.abspath(__file__))

chrome_driver_path = os.path.join(application_path, 'chromedriver.exe')
```

---

## Manutenibilidade

### Código Auto-documentado

```python
def calcular_escalonamento(self, data_criacao_str):
    """
    Calcula horário de escalonamento (+4h da criação).
    
    Args:
        data_criacao_str: Data no formato "dd/mm/yy HH:MM"
    
    Returns:
        String formatada "dd/mm/yy HH:MM" ou "Erro ao calcular"
    """
    try:
        data_criacao = datetime.strptime(data_criacao_str, "%d/%m/%y %H:%M")
        escalonamento = data_criacao + timedelta(hours=4)
        return escalonamento.strftime("%d/%m/%y %H:%M")
    except ValueError:
        return "Erro ao calcular"
```

### Constantes vs Magic Numbers

**❌ Magic numbers:**
```python
WebDriverWait(self.driver, 15)  # O que é 15?
```

**✅ Constantes nomeadas (melhoria futura):**
```python
WEBDRIVER_TIMEOUT = 15
ESCALONAMENTO_HORAS = 4

WebDriverWait(self.driver, WEBDRIVER_TIMEOUT)
```

---

## Conclusão

Esta arquitetura foi projetada para:
- ✅ **Simplicidade**: Fácil de entender e manter
- ✅ **Robustez**: Tratamento de erros extensivo
- ✅ **Performance**: Threading e otimizações
- ✅ **Segurança**: Sem exposição de credenciais
- ✅ **Escalabilidade**: Base sólida para futuras melhorias

**Desenvolvido por:** Leonardo Mattana  
**Projeto:** Yellow Belt - Automação GE  
**Última atualização:** 2024
