"""
Interface gráfica moderna e colorida
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
from datetime import datetime

class Interface:
    def __init__(self, automacao):
        self.automacao = automacao
        self.root = tk.Tk()
        self.setup_janela()
        self.setup_widgets()
    
    def setup_janela(self):
        self.root.title("AutoPes V2 - Automação de Pesquisas")
        self.root.geometry("700x600")
        self.root.resizable(False, False)
        
        # Cor de fundo principal
        self.root.configure(bg='#1a1a2e')
        
        # Centralizar na tela
        self.root.eval('tk::PlaceWindow . center')
    
    def setup_widgets(self):
        # Container principal com gradiente (simulado)
        main = tk.Frame(self.root, bg='#1a1a2e')
        main.pack(fill='both', expand=True)
        
        # Header com gradiente
        header = tk.Frame(main, bg='#16213e', height=120)
        header.pack(fill='x', pady=(0, 20))
        header.pack_propagate(False)
        
        # Ícone e título
        icon_label = tk.Label(header, text="🤖", font=('Segoe UI Emoji', 48), bg='#16213e', fg='#e94560')
        icon_label.pack(pady=(20, 5))
        
        title_label = tk.Label(header, text="AutoPes V2", 
                               font=('Arial', 24, 'bold'), 
                               bg='#16213e', fg='#ffffff')
        title_label.pack()
        
        subtitle_label = tk.Label(header, text="Automação de Pesquisas Inteligente", 
                                  font=('Arial', 10), 
                                  bg='#16213e', fg='#a0a0a0')
        subtitle_label.pack()
        
        # Frame de configuração (card)
        config_card = tk.Frame(main, bg='#0f3460', relief='flat', bd=0)
        config_card.pack(pady=20, padx=40, fill='x')
        
        # Título do card
        tk.Label(config_card, text="⚙️ CONFIGURAÇÕES", 
                font=('Arial', 12, 'bold'), 
                bg='#0f3460', fg='#e94560').pack(pady=(15, 10))
        
        # Frame interno das configurações
        config_inner = tk.Frame(config_card, bg='#0f3460')
        config_inner.pack(pady=10)
        
        # Temas
        tk.Label(config_inner, text="📚 Número de Temas:", 
                font=('Arial', 10), bg='#0f3460', fg='#ffffff').grid(row=0, column=0, padx=10, pady=10, sticky='e')
        
        self.num_temas = tk.Spinbox(config_inner, from_=1, to=10, width=15,
                                    font=('Arial', 10), bg='#1a1a2e', fg='#ffffff',
                                    buttonbackground='#e94560', relief='flat')
        self.num_temas.grid(row=0, column=1, padx=10, pady=10)
        self.num_temas.delete(0, 'end')
        self.num_temas.insert(0, "2")
        
        # Perguntas
        tk.Label(config_inner, text="❓ Perguntas por Tema:", 
                font=('Arial', 10), bg='#0f3460', fg='#ffffff').grid(row=1, column=0, padx=10, pady=10, sticky='e')
        
        self.num_perguntas = tk.Spinbox(config_inner, from_=1, to=5, width=15,
                                        font=('Arial', 10), bg='#1a1a2e', fg='#ffffff',
                                        buttonbackground='#e94560', relief='flat')
        self.num_perguntas.grid(row=1, column=1, padx=10, pady=10)
        self.num_perguntas.delete(0, 'end')
        self.num_perguntas.insert(0, "2")
        
        # Botões
        btn_frame = tk.Frame(main, bg='#1a1a2e')
        btn_frame.pack(pady=20)
        
        # Estilo dos botões customizados
        self.btn_iniciar = tk.Button(btn_frame, text="▶ INICIAR AUTOMAÇÃO", 
                                     command=self.iniciar,
                                     bg='#e94560', fg='#ffffff',
                                     font=('Arial', 11, 'bold'),
                                     padx=30, pady=10,
                                     relief='flat', cursor='hand2')
        self.btn_iniciar.pack(side='left', padx=10)
        
        self.btn_parar = tk.Button(btn_frame, text="⏹ PARAR", 
                                   command=self.parar,
                                   bg='#533483', fg='#ffffff',
                                   font=('Arial', 11, 'bold'),
                                   padx=30, pady=10,
                                   relief='flat', cursor='hand2',
                                   state='disabled')
        self.btn_parar.pack(side='left', padx=10)
        
        # Frame do log (card)
        log_card = tk.Frame(main, bg='#0f3460', relief='flat', bd=0)
        log_card.pack(pady=10, padx=40, fill='both', expand=True)
        
        tk.Label(log_card, text="📋 LOG DE EXECUÇÃO", 
                font=('Arial', 10, 'bold'), 
                bg='#0f3460', fg='#e94560').pack(pady=(10, 5))
        
        # Frame para o texto do log com scroll
        log_frame = tk.Frame(log_card, bg='#0f3460')
        log_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        scrollbar = tk.Scrollbar(log_frame, bg='#0f3460')
        scrollbar.pack(side='right', fill='y')
        
        self.log_text = tk.Text(log_frame, height=10,
                                font=('Consolas', 9),
                                bg='#1a1a2e', fg='#00ff9d',
                                relief='flat', bd=0,
                                yscrollcommand=scrollbar.set)
        self.log_text.pack(side='left', fill='both', expand=True)
        scrollbar.config(command=self.log_text.yview)
        
        # Configurar cores das tags (tipos de mensagem)
        self.log_text.tag_config('info', foreground='#00ff9d')
        self.log_text.tag_config('error', foreground='#ff4444')
        self.log_text.tag_config('warning', foreground='#ffaa00')
        self.log_text.tag_config('success', foreground='#00ff9d')
        
        # Status bar
        status_frame = tk.Frame(main, bg='#16213e', height=35)
        status_frame.pack(fill='x', side='bottom')
        status_frame.pack_propagate(False)
        
        self.status_var = tk.StringVar(value="✅ Pronto para iniciar")
        status_label = tk.Label(status_frame, textvariable=self.status_var,
                                font=('Arial', 9), bg='#16213e', fg='#a0a0a0')
        status_label.pack(side='left', padx=20, pady=8)
        
        # Indicador de conexão (simulado)
        self.conexao_label = tk.Label(status_frame, text="🌐 Online", 
                                      font=('Arial', 9), bg='#16213e', fg='#00ff9d')
        self.conexao_label.pack(side='right', padx=20, pady=8)
        
        # Efeito hover nos botões
        self.btn_iniciar.bind('<Enter>', lambda e: self.btn_iniciar.config(bg='#ff6b6b'))
        self.btn_iniciar.bind('<Leave>', lambda e: self.btn_iniciar.config(bg='#e94560'))
        
        self.btn_parar.bind('<Enter>', lambda e: self.btn_parar.config(bg='#6c4ab6'))
        self.btn_parar.bind('<Leave>', lambda e: self.btn_parar.config(bg='#533483'))
    
    def log(self, msg, tipo='info'):
        """Adiciona mensagem ao log com cor"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Ícones para cada tipo
        icones = {
            'info': 'ℹ️',
            'error': '❌',
            'warning': '⚠️',
            'success': '✅'
        }
        
        icon = icones.get(tipo, '📌')
        self.log_text.insert(tk.END, f"[{timestamp}] {icon} {msg}\n", tipo)
        self.log_text.see(tk.END)
        
        # Atualizar status bar se for importante
        if tipo == 'error':
            self.status_var.set(f"❌ Erro: {msg[:50]}")
        elif tipo == 'success':
            self.status_var.set(f"✅ {msg[:50]}")
    
    def atualizar_status(self, tipo, *args):
        """Callback para atualizar interface durante execução"""
        if tipo == "progresso":
            idx, total = args
            percent = (idx / total) * 100
            self.status_var.set(f"🔄 Progresso: {idx}/{total} ({percent:.0f}%)")
            self.log(f"Pesquisa {idx}/{total} concluída", 'info')
        elif tipo == "info":
            self.log(args[0], 'info')
        elif tipo == "erro":
            self.log(args[0], 'error')
    
    def iniciar(self):
        try:
            num_temas = int(self.num_temas.get())
            num_perguntas = int(self.num_perguntas.get())
            
            if num_temas < 1 or num_temas > 10:
                messagebox.showerror("Erro", "Número de temas inválido (1-10)")
                return
            
            if num_perguntas < 1 or num_perguntas > 5:
                messagebox.showerror("Erro", "Número de perguntas inválido (1-5)")
                return
            
            # Desabilitar controles
            self.btn_iniciar.config(state='disabled', bg='#999999')
            self.btn_parar.config(state='normal', bg='#533483')
            self.num_temas.config(state='disabled')
            self.num_perguntas.config(state='disabled')
            
            # Limpar log e iniciar
            self.log_text.delete(1.0, tk.END)
            self.log("🚀 Iniciando AutoPes V2...", 'info')
            self.log("⚙️ Preparando automação...", 'info')
            self.log("🌐 Verificando conexão...", 'info')
            
            # Mudar cor do status
            self.conexao_label.config(fg='#ffaa00', text="🔄 Verificando...")
            
            # Iniciar thread
            thread = threading.Thread(target=self._executar, args=(num_temas, num_perguntas), daemon=True)
            thread.start()
            
        except ValueError:
            messagebox.showerror("Erro", "Digite números válidos")
    
    def _executar(self, num_temas, num_perguntas):
        sucesso = self.automacao.executar(num_temas, num_perguntas, self.atualizar_status)
        self.root.after(0, self._finalizar, sucesso)
    
    def _finalizar(self, sucesso):
        # Restaurar controles
        self.btn_iniciar.config(state='normal', bg='#e94560')
        self.btn_parar.config(state='disabled', bg='#533483')
        self.num_temas.config(state='normal')
        self.num_perguntas.config(state='normal')
        self.conexao_label.config(fg='#00ff9d', text="🌐 Online")
        
        if sucesso:
            self.log("🎉 Automação concluída com sucesso!", 'success')
            self.status_var.set("✅ Automação finalizada com sucesso!")
            messagebox.showinfo("Sucesso", "✅ Automação finalizada!\n\nOs resultados foram salvos em CSV.")
        else:
            self.log("⚠️ Automação concluída com falhas", 'warning')
            self.status_var.set("⚠️ Automação concluída com falhas")
            messagebox.showwarning("Atenção", "⚠️ Algumas pesquisas falharam.\n\nVerifique o log.")
    
    def parar(self):
        if hasattr(self, 'automacao') and self.automacao.executando:
            self.automacao.parar()
            self.log("⏹️ Parando automação...", 'warning')
            self.status_var.set("⏹️ Parando automação...")
    
    def run(self):
        self.root.mainloop()