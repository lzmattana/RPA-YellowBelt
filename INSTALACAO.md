# 🚀 Guia de Instalação e Setup

Guia completo para configurar o ambiente de desenvolvimento e produção da Automação GE.

---

## 📑 Índice

1. [Instalação para Usuários Finais](#instalação-para-usuários-finais)
2. [Instalação para Desenvolvedores](#instalação-para-desenvolvedores)
3. [Configuração do ChromeDriver](#configuração-do-chromedriver)
4. [Build do Executável](#build-do-executável)
5. [Troubleshooting](#troubleshooting)

---

## Instalação para Usuários Finais

### Opção 1: Executável Standalone (Recomendado)

#### Requisitos Mínimos
- Windows 10/11 (64-bit)
- Google Chrome instalado
- 4 GB RAM
- 100 MB espaço em disco

#### Passo a Passo

**1. Download dos Arquivos**
```
Acesse: https://github.com/seu-usuario/automacao-ge-yellowbelt/releases
Baixe:
  - AutomacaoGE.exe
  - chromedriver.exe
```

**2. Organize os Arquivos**
```
Crie uma pasta (ex: C:\AutomacaoGE\)
Coloque ambos os arquivos na mesma pasta:

C:\AutomacaoGE\
├── AutomacaoGE.exe
└── chromedriver.exe
```

**3. Configure o ChromeDriver**
```
⚠️ IMPORTANTE: A versão do ChromeDriver deve ser compatível com seu Chrome!

Verificar versão do Chrome:
1. Abra o Chrome
2. Digite: chrome://version
3. Anote o número da versão (ex: 120.0.6099.109)

Baixar ChromeDriver compatível:
https://chromedriver.chromium.org/downloads
Escolha a versão correspondente ao seu Chrome
```

**4. Execute**
```
Duplo clique em AutomacaoGE.exe
```

### Opção 2: Atalho na Área de Trabalho

**1. Criar Atalho**
```
Botão direito em AutomacaoGE.exe → Enviar para → Área de trabalho
```

**2. Personalizar Ícone (Opcional)**
```
Botão direito no atalho → Propriedades → Alterar Ícone
```

---

## Instalação para Desenvolvedores

### Requisitos

#### Sistema Operacional
- Windows 10/11, Linux (Ubuntu 20.04+), ou macOS 11+

#### Software Necessário
- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)
- Git
- Google Chrome
- Editor de código (VS Code recomendado)

### Setup Completo

#### 1. Verificar Python

**Windows:**
```cmd
python --version
# Deve mostrar: Python 3.8.x ou superior

pip --version
# Deve mostrar versão do pip
```

**Linux/Mac:**
```bash
python3 --version
pip3 --version
```

**Se Python não estiver instalado:**
```
Download: https://www.python.org/downloads/
Durante instalação, marque "Add Python to PATH"
```

#### 2. Clonar o Repositório

```bash
# Via HTTPS
git clone https://github.com/seu-usuario/automacao-ge-yellowbelt.git

# Ou via SSH
git clone git@github.com:seu-usuario/automacao-ge-yellowbelt.git

# Navegar para o diretório
cd automacao-ge-yellowbelt
```

#### 3. Criar Ambiente Virtual

**Windows:**
```cmd
# Criar
python -m venv venv

# Ativar
venv\Scripts\activate

# Prompt deve mostrar: (venv) C:\...\automacao-ge-yellowbelt>
```

**Linux/Mac:**
```bash
# Criar
python3 -m venv venv

# Ativar
source venv/bin/activate

# Prompt deve mostrar: (venv) user@host:~/automacao-ge-yellowbelt$
```

#### 4. Instalar Dependências

```bash
# Atualizar pip
pip install --upgrade pip

# Instalar dependências do projeto
pip install -r requirements.txt

# Verificar instalação
pip list
```

**Saída esperada:**
```
Package         Version
--------------- -------
selenium        4.x.x
...
```

#### 5. Configurar ChromeDriver

**Opção A: Download Manual**
```bash
1. Visite: https://chromedriver.chromium.org/downloads
2. Baixe versão compatível com seu Chrome
3. Coloque chromedriver.exe na raiz do projeto
```

**Opção B: Script Automático (Windows)**
```cmd
# Criar script download_chromedriver.bat

@echo off
echo Baixando ChromeDriver...
curl -L -o chromedriver.zip https://chromedriver.storage.googleapis.com/LATEST_RELEASE/chromedriver_win32.zip
tar -xf chromedriver.zip
del chromedriver.zip
echo ChromeDriver instalado!
pause
```

#### 6. Verificar Estrutura

```bash
automacao-ge-yellowbelt/
├── automacao_ge.py
├── chromedriver.exe         ← Deve estar aqui
├── requirements.txt
├── README.md
├── LICENSE
├── .gitignore
└── venv/                    ← Pasta do ambiente virtual
```

#### 7. Executar Aplicação

```bash
# Com ambiente virtual ativado
python automacao_ge.py
```

**Primeira execução bem-sucedida:**
```
✅ Interface gráfica abre
✅ Campos visíveis e funcionais
✅ Sem erros no console
```

---

## Configuração do ChromeDriver

### Compatibilidade de Versões

| Chrome Version | ChromeDriver Version | Download Link |
|----------------|---------------------|---------------|
| 120.x | 120.0.6099.x | [Link](https://chromedriver.storage.googleapis.com/index.html?path=120.0.6099.109/) |
| 119.x | 119.0.6045.x | [Link](https://chromedriver.storage.googleapis.com/index.html?path=119.0.6045.105/) |
| 118.x | 118.0.5993.x | [Link](https://chromedriver.storage.googleapis.com/index.html?path=118.0.5993.70/) |

### Verificação de Compatibilidade

**Script de Teste:**
```python
# test_chromedriver.py
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

service = Service('chromedriver.exe')
driver = webdriver.Chrome(service=service)
print(f"✅ ChromeDriver funcionando! Versão: {driver.capabilities['browserVersion']}")
driver.quit()
```

**Executar:**
```bash
python test_chromedriver.py
```

### Troubleshooting ChromeDriver

**Erro: "This version of ChromeDriver only supports Chrome version X"**
```
Solução:
1. Verificar versão do Chrome instalado
2. Baixar ChromeDriver compatível
3. Substituir chromedriver.exe
```

**Erro: "chromedriver.exe is not a valid Win32 application"**
```
Solução:
Baixe a versão correta para sua arquitetura:
- chromedriver_win32.zip → 32-bit
- chromedriver_win64.zip → 64-bit (mais comum)
```

**Erro: "ChromeDriver não encontrado"**
```
Solução:
Verificar que chromedriver.exe está em:
- Mesma pasta que AutomacaoGE.exe (produção)
- Raiz do projeto (desenvolvimento)
```

---

## Build do Executável

### Usando PyInstaller

#### 1. Instalar PyInstaller

```bash
# Com ambiente virtual ativado
pip install pyinstaller
```

#### 2. Criar Executável

**Build Básico:**
```bash
pyinstaller --onefile automacao_ge.py
```

**Build Otimizado:**
```bash
pyinstaller --onefile --windowed --icon=icon.ico --name=AutomacaoGE automacao_ge.py
```

**Parâmetros:**
- `--onefile`: Gera um único executável
- `--windowed`: Sem console (apenas GUI)
- `--icon=icon.ico`: Define ícone customizado
- `--name=AutomacaoGE`: Nome do executável

#### 3. Localizar Executável

```bash
dist/
└── AutomacaoGE.exe    ← Seu executável
```

#### 4. Preparar para Distribuição

```bash
# Criar pasta de distribuição
mkdir release
copy dist\AutomacaoGE.exe release\
copy chromedriver.exe release\

# Compactar
# Use WinRAR, 7-Zip, ou:
tar -a -c -f AutomacaoGE-v1.0.zip release
```

### Build Script Automatizado

**build.bat (Windows):**
```batch
@echo off
echo =================================
echo Build Automacao GE
echo =================================

echo.
echo [1/5] Limpando builds anteriores...
rmdir /s /q build dist
del /q *.spec

echo.
echo [2/5] Executando PyInstaller...
pyinstaller --onefile --windowed --icon=icon.ico --name=AutomacaoGE automacao_ge.py

echo.
echo [3/5] Criando pasta de release...
mkdir release
copy dist\AutomacaoGE.exe release\
copy chromedriver.exe release\
copy README.md release\

echo.
echo [4/5] Compactando...
tar -a -c -f AutomacaoGE-v1.0.zip release

echo.
echo [5/5] Build concluído!
echo Executável: release\AutomacaoGE.exe
echo Arquivo ZIP: AutomacaoGE-v1.0.zip
pause
```

**Executar:**
```bash
build.bat
```

---

## Troubleshooting

### Problemas Comuns

#### 1. "Python não é reconhecido como comando"

**Solução:**
```
1. Reinstalar Python
2. Marcar "Add Python to PATH" durante instalação
3. Ou adicionar manualmente ao PATH:
   - Windows: Painel de Controle → Sistema → Variáveis de Ambiente
   - Adicionar: C:\Python3X\ e C:\Python3X\Scripts\
```

#### 2. "pip install falha com erro SSL"

**Solução:**
```bash
# Proxy corporativo
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org selenium

# Ou configurar proxy
pip install --proxy=http://usuario:senha@proxy:porta selenium
```

#### 3. "ModuleNotFoundError: No module named 'selenium'"

**Solução:**
```bash
# Verificar que ambiente virtual está ativado
# Reinstalar selenium
pip uninstall selenium
pip install selenium
```

#### 4. "Tkinter não encontrado"

**Solução:**
```
Tkinter vem com Python, mas pode estar ausente em algumas instalações Linux:

Ubuntu/Debian:
sudo apt-get install python3-tk

Fedora/RHEL:
sudo yum install python3-tkinter
```

#### 5. "Executável não abre / Fecha imediatamente"

**Solução:**
```
1. Executar via prompt para ver erros:
   cmd → cd pasta → AutomacaoGE.exe

2. Verificar que chromedriver.exe está presente

3. Verificar antivírus (pode bloquear)
```

#### 6. "Erro ao conectar ao SIGTM"

**Checklist:**
```
✓ Conectado à rede corporativa?
✓ VPN ativa (se necessário)?
✓ Chrome atualizado?
✓ ChromeDriver compatível?
✓ Credenciais corretas?
✓ Firewall permitindo conexão?
```

### Logs de Debug

**Habilitar logs detalhados:**
```python
# Adicionar no início de automacao_ge.py
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='automacao_ge.log'
)
```

**Verificar logs:**
```bash
type automacao_ge.log    # Windows
cat automacao_ge.log     # Linux/Mac
```

---

## Configurações Avançadas

### Desenvolvimento com Hot Reload

**watchdog para auto-reload:**
```bash
pip install watchdog

# Criar script watch.py
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
import subprocess

class ChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith('.py'):
            print(f"Mudança detectada: {event.src_path}")
            subprocess.run(['python', 'automacao_ge.py'])

observer = Observer()
observer.schedule(ChangeHandler(), path='.', recursive=False)
observer.start()
```

### VS Code Configuration

**.vscode/settings.json:**
```json
{
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "python.formatting.provider": "black",
    "python.linting.pylintArgs": [
        "--disable=C0111"
    ],
    "files.exclude": {
        "**/__pycache__": true,
        "**/*.pyc": true
    }
}
```

**.vscode/launch.json:**
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Automacao GE",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/automacao_ge.py",
            "console": "integratedTerminal"
        }
    ]
}
```

---

## Suporte

### Recursos

- 📖 [Documentação Principal](README.md)
- 🏗️ [Arquitetura Técnica](ARQUITETURA.md)
- 🐛 [Issues no GitHub](https://github.com/seu-usuario/automacao-ge-yellowbelt/issues)

### Contato

- **Desenvolvedor:** Leonardo Mattana
- **Email:** seu.email@exemplo.com
- **GitHub:** [@seu-usuario](https://github.com/seu-usuario)

---

**Última atualização:** 2024  
**Versão do Guia:** 1.0
