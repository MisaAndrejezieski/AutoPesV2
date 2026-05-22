"""
Interface gráfica com psicologia das cores - Versão corrigida
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
        self.root.title("AutoPes V2")
        self.root.geometry("750x650")
        self.root.minsize(700, 600)
        
        # Cores psicologicamente agradáveis
        self.cores = {
            'fundo': '#F8F9FA',
            'primary': '#4361EE',
            'success': '#06D6A0',
            'danger': '#EF476F',
            'warning': '#FFD166',
            'dark': '#2B2D42',
            'gray': '#8D99AE',
            'light': '#EDF2F4',
            'white': '#FFFFFF',
        }
        
        self.root.configure(bg=self.cores['fundo'])
        
        # Centralizar na tela
        self.root.eval('tk::PlaceWindow . center')
    
    def criar_card(self, parent, titulo, cor_borda=None):
        """Cria um card estilizado"""
        if cor_borda is None:
            cor_borda = self.cores['primary']
        
        card = tk.Frame(parent, bg=self.cores['white'], relief='flat', bd=0)
        card.pack(fill='x', pady=10, padx=30)
        
        # Borda superior colorida
        border = tk.Frame(card, bg=cor_borda, height=4)
        border.pack(fill='x')
        
        # Título do card
        title_frame = tk.Frame(card, bg=self.cores['white'])
        title_frame.pack(fill='x', padx=20, pady=(15, 10))
        
        tk.Label(title_frame, text=titulo, 
                font=('Segoe UI', 13, 'bold'),
                bg=self.cores['white'], fg=self.cores['dark']).pack(side='left')
        
        return card
    
    def criar_input_estilizado(self, parent, label_text, default_value="2", from_=1, to=10):
        """Cria campo de entrada estilizado"""
        frame = tk.Frame(parent, bg=self.cores['white'])
        frame.pack(fill='x', padx=20, pady=10)
        
        # Label
        label = tk.Label(frame, text=label_text, 
                        font=('Segoe UI', 11),
                        bg=self.cores['white'], fg=self.cores['dark'])
        label.pack(anchor='w')
        
        # Frame do input
        input_frame = tk.Frame(frame, bg=self.cores['light'], height=45)
        input_frame.pack(fill='x', pady=(5, 0))
        input_frame.pack_propagate(False)
        
        # Spinbox estilizado
        spinbox = tk.Spinbox(input_frame, from_=from_, to=to, width=10,
                             font=('Segoe UI', 12),
                             bg=self.cores['white'], fg=self.cores['dark'],
                             relief='flat', highlightthickness=0,
                             buttonbackground=self.cores['primary'])
        spinbox.pack(pady=8, padx=10, anchor='w')
        spinbox.delete(0, 'end')
        spinbox.insert(0, default_value)
        
        return spinbox
    
    def criar_botao(self, parent, texto, comando, tipo='primary', estado='normal'):
        """Cria botão estilizado"""
        cores = {
            'primary': {'bg': self.cores['primary'], 'hover': '#3A56D4', 'fg': self.cores['white']},
            'success': {'bg': self.cores['success'], 'hover': '#05B58C', 'fg': self.cores['dark']},
            'danger': {'bg': self.cores['danger'], 'hover': '#D63E62', 'fg': self.cores['white']},
        }
        
        cor = cores.get(tipo, cores['primary'])
        
        btn = tk.Button(parent, text=texto, command=comando,
                       bg=cor['bg'], fg=cor['fg'],
                       font=('Segoe UI', 11, 'bold'),
                       padx=25, pady=10,
                       relief='flat', cursor='hand2',
                       state=estado)
        
        def on_enter(e):
            if btn['state'] == 'normal':
                btn.configure(bg=cor['hover'])
        
        def on_leave(e):
            if btn['state'] == 'normal':
                btn.configure(bg=cor['bg'])
        
        btn.bind('<Enter>', on_enter)
        btn.bind('<Leave>', on_leave)
        
        return btn
    
    def setup_widgets(self):
        # Container principal
        main = tk.Frame(self.root, bg=self.cores['fundo'])
        main.pack(fill='both', expand=True, padx=20, pady=20)
        
        # ===== HEADER =====
        header = tk.Frame(main, bg=self.cores['fundo'])
        header.pack(fill='x', pady=(0, 20))
        
        logo_frame = tk.Frame(header, bg=self.cores['fundo'])
        logo_frame.pack()
        
        # Ícone
        self.icon_label = tk.Label(logo_frame, text="🤖", 
                                   font=('Segoe UI', 52),
                                   bg=self.cores['fundo'])
        self.icon_label.pack()
        
        # Título
        tk.Label(logo_frame, text="AutoPes V2", 
                font=('Segoe UI', 28, 'bold'),
                bg=self.cores['fundo'], fg=self.cores['dark']).pack()
        
        # Subtítulo
        tk.Label(logo_frame, text="Automação de Pesquisas Inteligente", 
                font=('Segoe UI', 11),
                bg=self.cores['fundo'], fg=self.cores['gray']).pack(pady=(5, 0))
        
        # ===== CARD CONFIGURAÇÕES =====
        config_card = self.criar_card(main, "⚙️ Configurações", self.cores['primary'])
        
        inputs_frame = tk.Frame(config_card, bg=self.cores['white'])
        inputs_frame.pack(fill='x', padx=20, pady=20)
        
        # Linha 1
        row1 = tk.Frame(inputs_frame, bg=self.cores['white'])
        row1.pack(fill='x', pady=5)
        
        # Temas
        tk.Label(row1, text="📚 Temas:", font=('Segoe UI', 11),
                bg=self.cores['white'], fg=self.cores['dark']).pack(side='left', padx=(0, 10))
        
        self.num_temas = tk.Spinbox(row1, from_=1, to=10, width=8,
                                    font=('Segoe UI', 11), relief='flat')
        self.num_temas.pack(side='left')
        self.num_temas.delete(0, 'end')
        self.num_temas.insert(0, "2")
        
        # Espaço
        tk.Label(row1, text=" " * 15, bg=self.cores['white']).pack(side='left')
        
        # Perguntas
        tk.Label(row1, text="❓ Perguntas:", font=('Segoe UI', 11),
                bg=self.cores['white'], fg=self.cores['dark']).pack(side='left', padx=(0, 10))
        
        self.num_perguntas = tk.Spinbox(row1, from_=1, to=6, width=8,
                                        font=('Segoe UI', 11), relief='flat')
        self.num_perguntas.pack(side='left')
        self.num_perguntas.delete(0, 'end')
        self.num_perguntas.insert(0, "2")
        
        # ===== CARD AÇÃO =====
        acao_card = self.criar_card(main, "🎮 Controles", self.cores['warning'])
        
        btn_frame = tk.Frame(acao_card, bg=self.cores['white'])
        btn_frame.pack(pady=25)
        
        self.btn_iniciar = self.criar_botao(btn_frame, "▶ INICIAR", 
                                             self.iniciar, 'success')
        self.btn_iniciar.pack(side='left', padx=10)
        
        self.btn_parar = self.criar_botao(btn_frame, "⏹ PARAR", 
                                          self.parar, 'danger', 'disabled')
        self.btn_parar.pack(side='left', padx=10)
        
        # ===== CARD LOG =====
        log_card = self.criar_card(main, "📋 Log de Execução", self.cores['gray'])
        
        log_container = tk.Frame(log_card, bg=self.cores['white'])
        log_container.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        scrollbar = tk.Scrollbar(log_container, bg=self.cores['light'])
        scrollbar.pack(side='right', fill='y')
        
        self.log_text = tk.Text(log_container, height=12,
                                font=('Consolas', 10),
                                bg=self.cores['light'], fg=self.cores['dark'],
                                relief='flat', bd=0,
                                yscrollcommand=scrollbar.set,
                                wrap='word')
        self.log_text.pack(side='left', fill='both', expand=True)
        scrollbar.config(command=self.log_text.yview)
        
        # Cores do log
        self.log_text.tag_config('info', foreground=self.cores['primary'])
        self.log_text.tag_config('error', foreground=self.cores['danger'])
        self.log_text.tag_config('warning', foreground='#F18F01')
        self.log_text.tag_config('success', foreground=self.cores['success'])
        
        # ===== STATUS BAR =====
        status_bar = tk.Frame(main, bg=self.cores['light'], height=40)
        status_bar.pack(fill='x', side='bottom')
        status_bar.pack_propagate(False)
        
        self.status_var = tk.StringVar(value="✨ Pronto para começar")
        status_label = tk.Label(status_bar, textvariable=self.status_var,
                                font=('Segoe UI', 9),
                                bg=self.cores['light'], fg=self.cores['gray'])
        status_label.pack(side='left', padx=15, pady=10)
        
        # Indicador
        self.status_icon = tk.Label(status_bar, text="●", 
                                    font=('Segoe UI', 10),
                                    bg=self.cores['light'], fg=self.cores['success'])
        self.status_icon.pack(side='right', padx=15, pady=10)
        
        # Dica
        dica = tk.Label(status_bar, text="💡 Edge será aberto e fechado automaticamente",
                       font=('Segoe UI', 8),
                       bg=self.cores['light'], fg=self.cores['gray'])
        dica.pack(side='right', padx=15, pady=10)
        
        # Animação ícone
        self.animar_icone()
    
    def animar_icone(self):
        icones = ["🤖", "🔍", "⚡", "🚀"]
        if hasattr(self, 'icon_index'):
            self.icon_index = (self.icon_index + 1) % len(icones)
        else:
            self.icon_index = 0
        
        self.icon_label.config(text=icones[self.icon_index])
        self.root.after(2000, self.animar_icone)
    
    def log(self, msg, tipo='info'):
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        icones = {'info': 'ℹ️', 'error': '❌', 'warning': '⚠️', 'success': '✅'}
        icon = icones.get(tipo, '📌')
        
        self.log_text.insert(tk.END, f"[{timestamp}] {icon} {msg}\n", tipo)
        self.log_text.see(tk.END)
        self.root.update_idletasks()
    
    def atualizar_status_ui(self, tipo, *args):
        if tipo == "progresso":
            idx, total = args
            percent = (idx / total) * 100
            self.status_var.set(f"🔄 Progresso: {idx}/{total} ({percent:.0f}%)")
            self.status_icon.config(fg=self.cores['warning'], text="▶")
            self.log(f"Pesquisa {idx}/{total}", 'info')
        elif tipo == "info":
            self.log(args[0], 'info')
        elif tipo == "erro":
            self.log(args[0], 'error')
            self.status_icon.config(fg=self.cores['danger'], text="●")
    
    def iniciar(self):
        try:
            num_temas = int(self.num_temas.get())
            num_perguntas = int(self.num_perguntas.get())
            
            if num_temas < 1 or num_temas > 10:
                messagebox.showerror("Erro", "Temas inválido (1-10)")
                return
            
            if num_perguntas < 1 or num_perguntas > 6:
                messagebox.showerror("Erro", "Perguntas inválido (1-6)")
                return
            
            self.btn_iniciar.config(state='disabled')
            self.btn_parar.config(state='normal')
            self.num_temas.config(state='disabled')
            self.num_perguntas.config(state='disabled')
            
            self.log_text.delete(1.0, tk.END)
            self.log("🚀 Iniciando AutoPes V2...", 'info')
            self.log("📡 Abrindo navegador...", 'info')
            
            self.status_var.set("🔄 Executando...")
            self.status_icon.config(fg=self.cores['warning'], text="▶")
            
            thread = threading.Thread(target=self._executar, args=(num_temas, num_perguntas), daemon=True)
            thread.start()
            
        except ValueError:
            messagebox.showerror("Erro", "Digite números válidos")
    
    def _executar(self, num_temas, num_perguntas):
        sucesso = self.automacao.executar(num_temas, num_perguntas, self.atualizar_status_ui)
        self.root.after(0, self._finalizar, sucesso)
    
    def _finalizar(self, sucesso):
        self.btn_iniciar.config(state='normal')
        self.btn_parar.config(state='disabled')
        self.num_temas.config(state='normal')
        self.num_perguntas.config(state='normal')
        
        if sucesso:
            self.log("🎉 Automação concluída!", 'success')
            self.status_var.set("✅ Concluído!")
            self.status_icon.config(fg=self.cores['success'], text="●")
            messagebox.showinfo("Sucesso", "Automação finalizada!")
        else:
            self.log("⚠️ Concluído com falhas", 'warning')
            self.status_var.set("⚠️ Concluído com falhas")
            self.status_icon.config(fg=self.cores['danger'], text="●")
            messagebox.showwarning("Atenção", "Algumas falhas ocorreram")
    
    def parar(self):
        if hasattr(self, 'automacao') and self.automacao.executando:
            self.automacao.parar()
            self.log("⏹️ Parando...", 'warning')
            self.status_var.set("⏹️ Parando...")
    
    def run(self):
        self.root.mainloop()