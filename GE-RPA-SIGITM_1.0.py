import os
import time
import getpass
import threading
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
# from webdriver_manager.chrome import ChromeDriverManager # <-- MUDEI: COMENTEI/REMOVI ESTA LINHA
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, Menu
import json
import sys # Adicionado para lidar com caminhos no executável PyInstaller

# Configuração para contornar o firewall corporativo (se ainda necessário)
os.environ['WDM_SSL_VERIFY'] = '0'

class SIGTMApp:
    def __init__(self):
        self.root = tk.Tk()
        self.driver = None
        self.wait = None
        self.is_logged_in = False
        self.setup_styles()
        # MODIFICAÇÃO 1: Remover a chamada da tela de login e ir direto para a principal
        self.show_main_application()

    def setup_styles(self):
        """Configura o tema escuro personalizado com cores da Vivo e novos estilos"""
        self.root.configure(bg='#1a1a1a')
        
        # Cores
        self.colors = {
            'bg_primary': '#1a1a1a',
            'bg_secondary': '#2d2d2d',
            'vivo_purple': '#660099',
            'vivo_yellow': '#ffcc00',
            'text_primary': '#ffffff',
            'text_secondary': '#cccccc',
            'success': '#00cc44',
            'error': '#ff3333',
            'border': '#404040'
        }
        
        # Estilo personalizado
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure('Dark.TFrame', background=self.colors['bg_primary'])
        style.configure('Secondary.TFrame', background=self.colors['bg_secondary'])
        
        style.configure('Title.TLabel',
                        background=self.colors['bg_primary'],
                        foreground=self.colors['vivo_purple'],
                        font=('Arial', 18, 'bold'))
        
        style.configure('Dark.TLabel',
                        background=self.colors['bg_secondary'],
                        foreground=self.colors['text_primary'],
                        font=('Arial', 10))

        style.configure('Status.TLabel',
                        background=self.colors['bg_primary'],
                        foreground=self.colors['text_secondary'],
                        font=('Arial', 9))
        
        style.configure('Author.TLabel',
                         background=self.colors['bg_primary'],
                         foreground=self.colors['text_secondary'],
                         font=('Arial', 8))

        style.configure('Card.TLabelframe',
                         background=self.colors['bg_secondary'],
                         relief='solid',
                         borderwidth=1,
                         bordercolor=self.colors['border'])
        style.configure('Card.TLabelframe.Label',
                         foreground=self.colors['vivo_yellow'],
                         background=self.colors['bg_secondary'],
                         font=('Arial', 12, 'bold'))
        
        style.configure('Vivo.TButton',
                        background=self.colors['vivo_purple'],
                        foreground=self.colors['text_primary'],
                        font=('Arial', 10, 'bold'),
                        borderwidth=0,
                        focuscolor='none')
                
        style.map('Vivo.TButton',
                  background=[('active', self.colors['vivo_yellow']),
                              ('pressed', '#cc9900')])
        
        style.configure('Dark.TEntry',
                         fieldbackground=self.colors['bg_secondary'],
                        foreground=self.colors['text_primary'],
                         borderwidth=1,
                         bordercolor=self.colors['border'],
                         insertcolor=self.colors['text_primary'])

    def show_main_application(self):
        """Mostra a aplicação principal"""
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        self.root.minsize(800, 600)
        self.root.title("🤖 Automação GE 🤖 - Yellow Belt ")
        
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (900 // 2)
        y = (self.root.winfo_screenheight() // 2) - (700 // 2)
        self.root.geometry(f"900x700+{x}+{y}")
        
        self.setup_main_interface()

    # MODIFICAÇÃO 2: Adicionar função para criar menu de contexto (copiar/colar)
    def make_context_menu(self, widget):
        """Cria um menu de contexto para os widgets de texto (Entry, Text)"""
        context_menu = Menu(widget, tearoff=0, bg=self.colors['bg_secondary'], fg=self.colors['text_primary'])
        context_menu.add_command(label="Recortar", command=lambda: widget.event_generate("<<Cut>>"))
        context_menu.add_command(label="Copiar", command=lambda: widget.event_generate("<<Copy>>"))
        context_menu.add_command(label="Colar", command=lambda: widget.event_generate("<<Paste>>"))
        widget.bind("<Button-3>", lambda e: context_menu.tk_popup(e.x_root, e.y_root))

    def setup_main_interface(self):
        """Configura a interface principal da aplicação"""
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        main_frame = ttk.Frame(self.root, style='Dark.TFrame', padding=15)
        main_frame.grid(row=0, column=0, sticky='nsew')
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)

        header_frame = ttk.Frame(main_frame, style='Dark.TFrame')
        header_frame.grid(row=0, column=0, sticky='ew', pady=(0, 10))
        header_frame.columnconfigure(1, weight=1)

        title_label = ttk.Label(header_frame, text="🤖 AUTOMAÇÃO GE 🤖", style='Title.TLabel')
        title_label.grid(row=0, column=0, sticky='w')
        
        self.status_label = ttk.Label(header_frame, text="Sistema Pronto", style='Status.TLabel')
        self.status_label.grid(row=0, column=1, sticky='e', padx=20)

        logout_btn = ttk.Button(header_frame, text="SAIR", style='Vivo.TButton',
                                 command=self.logout, width=8)
        logout_btn.grid(row=0, column=2, sticky='e')
        
        controls_frame = ttk.Frame(main_frame, style='Dark.TFrame')
        controls_frame.grid(row=1, column=0, sticky='ew', pady=(0, 10))
        controls_frame.columnconfigure(0, weight=1)

        login_section = ttk.LabelFrame(controls_frame, text="🔐 Login SIGTM", style='Card.TLabelframe', padding=15)
        login_section.grid(row=0, column=0, sticky='ew', pady=(0, 10))
        login_section.columnconfigure(1, weight=1)
        login_section.columnconfigure(3, weight=1)
        
        ttk.Label(login_section, text="Usuário SIGTM:", style='Dark.TLabel').grid(row=0, column=0, sticky='w', pady=5)
        self.sigtm_user_entry = ttk.Entry(login_section, style='Dark.TEntry', width=25)
        self.sigtm_user_entry.grid(row=0, column=1, padx=(10, 20), pady=5, sticky='ew')
        
        ttk.Label(login_section, text="Senha SIGTM:", style='Dark.TLabel').grid(row=0, column=2, sticky='w', pady=5)
        self.sigtm_pass_entry = ttk.Entry(login_section, style='Dark.TEntry', width=25, show='*')
        self.sigtm_pass_entry.grid(row=0, column=3, padx=(10, 0), pady=5, sticky='ew')
        
        self.connect_btn = ttk.Button(login_section, text="CONECTAR SIGTM", style='Vivo.TButton',
                                         command=self.connect_sigtm, width=25)
        self.connect_btn.grid(row=1, column=0, columnspan=4, pady=(15, 5))
        
        search_section = ttk.LabelFrame(controls_frame, text="🔍 Buscar Chamado", style='Card.TLabelframe', padding=15)
        search_section.grid(row=1, column=0, sticky='ew', pady=10)
        search_section.columnconfigure(1, weight=1)
        search_section.columnconfigure(3, weight=1)
        
        ttk.Label(search_section, text="Número do BD:", style='Dark.TLabel').grid(row=0, column=0, sticky='w', pady=5)
        self.bd_entry = ttk.Entry(search_section, style='Dark.TEntry', width=25)
        self.bd_entry.grid(row=0, column=1, padx=(10, 20), pady=5, sticky='ew')
        
        ttk.Label(search_section, text="TASK:", style='Dark.TLabel').grid(row=0, column=2, sticky='w', pady=5)
        self.task_entry = ttk.Entry(search_section, style='Dark.TEntry', width=25)
        self.task_entry.grid(row=0, column=3, padx=(10, 0), pady=5, sticky='ew')
        
        ttk.Label(search_section, text="SFA:", style='Dark.TLabel').grid(row=1, column=0, sticky='w', pady=5)
        self.sfa_entry = ttk.Entry(search_section, style='Dark.TEntry', width=25)
        self.sfa_entry.grid(row=1, column=1, padx=(10, 20), pady=5, sticky='ew')

        search_buttons_frame = ttk.Frame(search_section, style='Secondary.TFrame')
        search_buttons_frame.grid(row=2, column=0, columnspan=4, pady=(15, 5))
        
        self.search_btn = ttk.Button(search_buttons_frame, text="BUSCAR CHAMADO", style='Vivo.TButton',
                                         command=self.search_ticket, width=20, state='disabled')
        self.search_btn.pack(side='left', padx=5)

        self.copy_btn_top = ttk.Button(search_buttons_frame, text="COPIAR ENTRADA", style='Vivo.TButton',
                                          command=self.copy_input_data, width=20)
        self.copy_btn_top.pack(side='left', padx=5)
        
        result_frame = ttk.LabelFrame(main_frame, text="📋 Carimbo Gerado", style='Card.TLabelframe', padding=15)
        result_frame.grid(row=2, column=0, sticky='nsew')
        result_frame.rowconfigure(0, weight=1)
        result_frame.columnconfigure(0, weight=1)

        self.result_text = scrolledtext.ScrolledText(result_frame,
                                                      wrap=tk.WORD,
                                                      height=10,
                                                      bg=self.colors['bg_secondary'],
                                                      fg=self.colors['text_primary'],
                                                      insertbackground=self.colors['text_primary'],
                                                      font=('Courier', 10),
                                                      borderwidth=0,
                                                      relief='flat')
        self.result_text.grid(row=0, column=0, sticky='nsew', pady=(0, 10))
        
        action_frame = ttk.Frame(result_frame, style='Secondary.TFrame')
        action_frame.grid(row=1, column=0, sticky='w')
        
        ttk.Button(action_frame, text="COPIAR CARIMBO", style='Vivo.TButton',
                   command=self.copy_stamp, width=18).pack(side='left', padx=(0, 10))
        
        ttk.Button(action_frame, text="LIMPAR", style='Vivo.TButton',
                   command=self.clear_result, width=18).pack(side='left')
        
        footer_frame = ttk.Frame(main_frame, style='Dark.TFrame')
        footer_frame.grid(row=3, column=0, sticky='ew', pady=(15, 0))
                
        ttk.Label(footer_frame, text="Yellow Belt Project - Automação GE | Desenvolvido por Leonardo Mattana",
                  style='Author.TLabel').pack(anchor='center')

        # MODIFICAÇÃO 2: Aplicar o menu de contexto aos campos
        self.make_context_menu(self.sigtm_user_entry)
        self.make_context_menu(self.sigtm_pass_entry)
        self.make_context_menu(self.bd_entry)
        self.make_context_menu(self.task_entry)
        self.make_context_menu(self.sfa_entry)
        self.make_context_menu(self.result_text)

    def connect_sigtm(self):
        """Conecta ao sistema SIGTM"""
        username = self.sigtm_user_entry.get().strip()
        password = self.sigtm_pass_entry.get().strip()
        
        if not username or not password:
            messagebox.showerror("Erro", "Por favor, preencha usuário e senha do SIGTM!")
            return
        
        threading.Thread(target=self._connect_sigtm_thread, args=(username, password), daemon=True).start()
        
    def _connect_sigtm_thread(self, username, password):
        """Thread para conectar ao SIGTM"""
        try:
            self.root.after(0, lambda: self.update_status("Conectando ao SIGTM..."))
            self.root.after(0, lambda: self.connect_btn.config(state='disabled'))
            
            # --- MODIFICAÇÃO CHAVE AQUI PARA USAR chromedriver.exe EMPACOTADO ---
            # Determina o caminho para o chromedriver.exe dentro do ambiente do PyInstaller
            if getattr(sys, 'frozen', False):
                application_path = os.path.dirname(sys.executable)
            else:
                application_path = os.path.dirname(os.path.abspath(__file__))
            
            chrome_driver_path = os.path.join(application_path, 'chromedriver.exe')

            if not os.path.exists(chrome_driver_path):
                self.root.after(0, lambda: messagebox.showerror("Erro de Driver", f"chromedriver.exe não encontrado em: {chrome_driver_path}\nPor favor, garanta que ele esteja na mesma pasta do executável."))
                self.root.after(0, lambda: self.connect_btn.config(state='normal'))
                return

            service = Service(chrome_driver_path) # <-- AGORA USAMOS O CAMINHO DIRETO
            options = webdriver.ChromeOptions()
            # options.add_argument("--headless") # Descomente se quiser o Chrome invisível
            self.driver = webdriver.Chrome(service=service, options=options)
            # --- FIM DA MODIFICAÇÃO CHAVE ---

            self.wait = WebDriverWait(self.driver, 15)
            
            self.driver.get("http://10.240.59.14/SIGITMWeb/login.jsp")
            
            self.wait.until(EC.presence_of_element_located((By.ID, "usuario"))).send_keys(username)
            self.driver.find_element(By.ID, "password").send_keys(password)
            self.driver.find_element(By.ID, "submitLogin").click()
            time.sleep(3)
            
            if "login" in self.driver.current_url.lower():
                self.root.after(0, lambda: messagebox.showerror("Erro", "❌ Falha no login! Verifique suas credenciais."))
                self.root.after(0, lambda: self.connect_btn.config(state='normal'))
                if self.driver:
                    self.driver.quit()
                    self.driver = None
                return
            
            self.root.after(0, lambda: self.update_status("✅ Login realizado com sucesso!"))
            
            self.root.after(0, lambda: self.update_status("Navegando para a página de busca..."))
            script_navegacao = "document.forms['navigation']['navigation:j_idcl'].value='navigation:localizar'; document.forms['navigation'].submit();"
            self.driver.execute_script(script_navegacao)
            self.wait.until(EC.presence_of_element_located((By.ID, "formLocalizar:tqiCodigo")))
            
            self.is_logged_in = True
            self.root.after(0, lambda: self.update_status("✅ Pronto para buscar chamados!"))
            self.root.after(0, lambda: self.search_btn.config(state='normal'))
            self.root.after(0, lambda: self.connect_btn.config(text="RECONECTAR", state='normal'))
                            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Erro", f"❌ Erro ao conectar: {str(e)}"))
            self.root.after(0, lambda: self.connect_btn.config(state='normal'))
            if self.driver:
                self.driver.quit()
                self.driver = None
            
    def search_ticket(self):
        """Busca o chamado no SIGTM"""
        if not self.is_logged_in or not self.driver:
            messagebox.showerror("Erro", "Conecte-se ao SIGTM primeiro!")
            return
        
        bd_number = self.bd_entry.get().strip()
        task = self.task_entry.get().strip()
        sfa = self.sfa_entry.get().strip()
        
        if not bd_number:
            messagebox.showerror("Erro", "Por favor, informe o número do BD!")
            return
        
        threading.Thread(target=self._search_ticket_thread, args=(bd_number, task, sfa), daemon=True).start()
        
    def _search_ticket_thread(self, bd_number, task, sfa):
        """Thread para buscar o chamado"""
        try:
            self.root.after(0, lambda: self.update_status("Buscando chamado..."))
            self.root.after(0, lambda: self.search_btn.config(state='disabled'))
            
            dados = self.extract_ticket_data(bd_number)
            
            if dados:
                stamp = self.generate_stamp(dados, task, sfa)
                self.root.after(0, lambda: self.result_text.delete(1.0, tk.END))
                self.root.after(0, lambda: self.result_text.insert(tk.END, stamp))
                self.root.after(0, lambda: self.update_status("Carimbo gerado com sucesso!"))
            else:
                self.root.after(0, lambda: messagebox.showerror("Erro", "Não foi possível extrair dados do chamado!"))
                
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Erro", f"Erro na busca: {str(e)}"))
        finally:
            self.root.after(0, lambda: self.search_btn.config(state='normal'))
            
    def extract_ticket_data(self, numero_bd):
        """Extrai dados do chamado"""
        janela_original = self.driver.current_window_handle
        
        try:
            campo_tiquete = self.wait.until(EC.presence_of_element_located((By.ID, "formLocalizar:tqiCodigo")))
            campo_tiquete.clear()
            campo_tiquete.send_keys(numero_bd)
            
            botao_pesquisar = self.wait.until(EC.element_to_be_clickable((By.ID, "formLocalizar:buttonLocalizar")))
            botao_pesquisar.click()
            
            self.wait.until(EC.number_of_windows_to_be(2))
            for handle in self.driver.window_handles:
                if handle != janela_original:
                    self.driver.switch_to.window(handle)
                    break
            
            self.wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
            time.sleep(1.5)
            
            dados = {}
            
            data_criacao = self.safe_find_value("input[id$=':DataCriacao']")
            dados['data_criacao'] = data_criacao
            dados['escalonamento_estimado'] = self.calcular_escalonamento(data_criacao)
            
            razao_social = self.safe_find_value("input[id$=':tisClienteTitular']")
            if razao_social == "Não encontrado":
                razao_social = self.safe_find_value("input[id$=':ddrtisClienteTitular']")
            dados['razao_social'] = razao_social
            
            cnpj = self.safe_find_value("input[id$=':tisClienteCnpj']")
            if cnpj == "Não encontrado":
                cnpj = self.safe_find_value("input[id$=':tisClienteCnpj01']")
            if cnpj == "Não encontrado":
                cnpj = self.safe_find_value("input[id$=':ddrtisClienteNumNrf']")
            dados['cnpj'] = cnpj
            
            contato_nome = self.safe_find_value("input[id$=':tqiContatoNome']")
            tel1 = self.safe_find_value("input[id$=':tqiReclamanteTelefone']")
            tel2 = self.safe_find_value("input[id$=':tqiContatoTelefone']")
            
            dados['contato_nome'] = contato_nome
            dados['tel1'] = tel1
            dados['tel2'] = tel2
            
            designador = self.safe_find_value("input[id$=':ddrtisClienteTerminal']")
            if designador == "Não encontrado":
                designador = self.safe_find_value("input[id$=':a4jInclClie1:tisLp']")
            if designador == "Não encontrado":
                designador = self.safe_find_value("input[id$=':a4jInclClie12:tisLp']")
            if designador == "Não encontrado":
                designador = self.safe_find_value("input[id$=':tisLp']")
            
            reclamacao = self.safe_find_value("input[id$=':reiNome']")
            dados['reclamacao'] = reclamacao
            designador_responsavel = f"{designador} {reclamacao}"
            dados['designador'] = designador_responsavel
            
            dados['sigtm'] = numero_bd
            
            return dados
            
        except Exception as e:
            print(f"❌ Ocorreu um erro inesperado durante a extração: {e}")
            return None
        finally:
            if len(self.driver.window_handles) > 1:
                self.driver.close()
                self.driver.switch_to.window(janela_original)
                    
    def safe_find_value(self, selector):
        """Função auxiliar que encontra um elemento de forma segura"""
        try:
            WebDriverWait(self.driver, 2).until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
            return self.driver.find_element(By.CSS_SELECTOR, selector).get_attribute("value")
        except (NoSuchElementException, TimeoutException):
            return "Não encontrado"
            
    def calcular_escalonamento(self, data_criacao_str):
        """Calcula o horário de escalonamento"""
        try:
            data_criacao = datetime.strptime(data_criacao_str, "%d/%m/%y %H:%M")
            escalonamento = data_criacao + timedelta(hours=4)
            return escalonamento.strftime("%d/%m/%y %H:%M")
        except ValueError:
            return "Erro ao calcular"
            
    def generate_stamp(self, dados, task, sfa):
        """Gera o carimbo final"""
        template = """***** CARIMBO GESTAO DE EXPECTATIVA TOP *****
TASK: {task}
SFA: {sfa}
SIGITM: {sigtm}
Nome do Cliente: {contato_nome}
Contato: {tel1} / {tel2}
CNPJ: {cnpj}
Razão Social: {razao_social}
Designador Responsável: {designador} {reclamacao}

***** CARIMBO GESTAO DE EXPECTATIVA TOP *****
TASK: {task}
SIGITM: {sigtm}

Ação Realizada / Tentativas de contato: 

--------------------------------------------------------
"""
        
        formatted_data = {k: (v if v != "Não encontrado" else "") for k, v in dados.items()}
        formatted_data['task'] = task if task else ""
        formatted_data['sfa'] = sfa if sfa else ""
        
        return template.format(**formatted_data)
        
    def copy_stamp(self):
        """Copia o carimbo gerado para a área de transferência"""
        content = self.result_text.get(1.0, tk.END).strip()
        if content:
            self.root.clipboard_clear()
            self.root.clipboard_append(content)
            messagebox.showinfo("Sucesso", "Carimbo copiado para a área de transferência!")
        else:
            messagebox.showwarning("Aviso", "Nenhum carimbo para copiar!")

    def copy_input_data(self):
        """Copia os dados de entrada para a área de transferência."""
        bd_number = self.bd_entry.get().strip()
        task = self.task_entry.get().strip()
        sfa = self.sfa_entry.get().strip()

        if not bd_number and not task and not sfa:
            messagebox.showwarning("Aviso", "Nenhuma informação de entrada para copiar!")
            return

        copy_text = f"BD: {bd_number}\nTASK: {task}\nSFA: {sfa}"
        
        self.root.clipboard_clear()
        self.root.clipboard_append(copy_text)
        messagebox.showinfo("Sucesso", "Dados de entrada copiados para a área de transferência!")

            
    def clear_result(self):
        """Limpa a área de resultado"""
        self.result_text.delete(1.0, tk.END)
        
    def update_status(self, message):
        """Atualiza o status da aplicação"""
        self.status_label.config(text=message)
        
    def logout(self):
        """Faz logout da aplicação"""
        if self.driver:
            try:
                self.driver.quit()
            except Exception as e:
                print(f"Erro ao fechar o driver: {e}")
        self.root.destroy()
        
    def run(self):
        """Executa a aplicação"""
        self.root.mainloop()

if __name__ == "__main__":
    app = SIGTMApp()
    app.run()