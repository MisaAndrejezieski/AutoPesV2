"""
Interface Dark Mode com Neon - Centralizada
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
        self.root.geometry("700x600")
        self.root.minsize(650, 550)
        
        # Cores Dark Mode + Neon
        self.cores = {
            'bg': '#0D0D0D',
            'bg_card': '#1A1A1A',
            'border': '#2A2A2A',
            'neon_cyan': '#00FFD1',
            'neon_pink': '#FF007F',
            'neon_green': '#39FF14',
            'neon_yellow': '#FFE600',
            'neon_purple': '#B300FF',
            'text': '#E0E0E0',
            'text_dim': '#808080',
            'input_bg': '#2A2A2A',
        }
        
        self.root.configure(bg=self.cores['bg'])
        
        # Centralizar
        self.root.eval('tk::PlaceWindow . center')
    
    def criar_card(self, parent, titulo, cor_neon):
        """Cria card com borda neon"""
        card = tk.Frame(parent, bg=self.cores['bg_card'], relief='flat', bd=0)
        card.pack(fill='x', pady=10, padx=40)
        
        # Borda neon superior
        border = tk.Frame(card, bg=cor_neon, height=2)
        border.pack(fill='x')
        
        # Título centralizado
        title_frame = tk.Frame(card, bg=self.cores['bg_card'])
        title_frame.pack(fill='x', padx=20, pady=(15, 10))
        
        tk.Label(title_frame, text=titulo, 
                font=('Consolas', 12, 'bold'),
                bg=self.cores['bg_card'], fg=cor_neon).pack(anchor='center')
        
        return card
    
    def setup_widgets(self):
        # Container principal
        main = tk.Frame(self.root, bg=self.cores['bg'])
        main.pack(fill='both', expand=True, padx=20, pady=20)
        
        # ===== HEADER CENTRALIZADO =====
        header = tk.Frame(main, bg=self.cores['bg'])
        header.pack(fill='x', pady=(0, 20))
        
        logo_frame = tk.Frame(header, bg=self.cores['bg'])
        logo_frame.pack(anchor='center')
        
        # Ícone neon
        self.icon_label = tk.Label(logo_frame, text="⚡", 
                                   font=('Consolas', 48),
                                   bg=self.cores['bg'], fg=self.cores['neon_cyan'])
        self.icon_label.pack()
        
        # Título
        tk.Label(logo_frame, text="AutoPes V2", 
                font=('Consolas', 28, 'bold'),
                bg=self.cores['bg'], fg=self.cores['neon_pink']).pack()
        
        # Linha decorativa
        deco = tk.Label(logo_frame, text="═" * 35, 
                       font=('Consolas', 8),
                       bg=self.cores['bg'], fg=self.cores['neon_purple'])
        deco.pack(pady=10)
        
        # ===== CARD CONFIGURAÇÕES =====
        config_card = self.criar_card(main, "[ CONFIGURAÇÕES ]", self.cores['neon_cyan'])
        
        # Frame dos inputs centralizado
        inputs_frame = tk.Frame(config_card, bg=self.cores['bg_card'])
        inputs_frame.pack(fill='x', padx=20, pady=20)
        
        # Linha 1: Temas
        row1 = tk.Frame(inputs_frame, bg=self.cores['bg_card'])
        row1.pack(pady=8)
        
        tk.Label(row1, text="TEMAS:", 
                font=('Consolas', 10, 'bold'),
                bg=self.cores['bg_card'], fg=self.cores['neon_yellow']).pack(side='left', padx=(0, 15))
        
        self.num_temas = tk.Spinbox(row1, from_=1, to=10, width=8,
                                    font=('Consolas', 11),
                                    bg=self.cores['input_bg'], fg=self.cores['neon_green'],
                                    relief='flat', highlightthickness=0,
                                    buttonbackground=self.cores['border'])
        self.num_temas.pack(side='left')
        self.num_temas.delete(0, 'end')
        self.num_temas.insert(0, "2")
        
        # Linha 2: Perguntas
        row2 = tk.Frame(inputs_frame, bg=self.cores['bg_card'])
        row2.pack(pady=8)
        
        tk.Label(row2, text="PERGUNTAS POR TEMA:", 
                font=('Consolas', 10, 'bold'),
                bg=self.cores['bg_card'], fg=self.cores['neon_yellow']).pack(side='left', padx=(0, 15))
        
        self.num_perguntas = tk.Spinbox(row2, from_=1, to=6, width=8,
                                        font=('Consolas', 11),
                                        bg=self.cores['input_bg'], fg=self.cores['neon_green'],
                                        relief='flat', highlightthickness=0,
                                        buttonbackground=self.cores['border'])
        self.num_perguntas.pack(side='left')
        self.num_perguntas.delete(0, 'end')
        self.num_perguntas.insert(0, "2")
        
        # ===== CARD CONTROLES =====
        controle_card = self.criar_card(main, "[ CONTROLES ]", self.cores['neon_pink'])
        
        btn_frame = tk.Frame(controle_card, bg=self.cores['bg_card'])
        btn_frame.pack(pady=25)
        
        # Botão Iniciar
        self.btn_iniciar = tk.Button(btn_frame, text="▶ INICIAR", 
                                     command=self.iniciar,
                                     bg='#1A1A1A', fg=self.cores['neon_green'],
                                     font=('Consolas', 11, 'bold'),
                                     padx=35, pady=10,
                                     relief='flat', cursor='hand2',
                                     activebackground='#2A2A2A',
                                     activeforeground=self.cores['neon_green'])
        self.btn_iniciar.pack(side='left', padx=15)
        
        # Botão Parar
        self.btn_parar = tk.Button(btn_frame, text="⏹ PARAR", 
                                   command=self.parar,
                                   bg='#1A1A1A', fg=self.cores['neon_pink'],
                                   font=('Consolas', 11, 'bold'),
                                   padx=35, pady=10,
                                   relief='flat', cursor='hand2',
                                   activebackground='#2A2A2A',
                                   activeforeground=self.cores['neon_pink'],
                                   state='disabled')
        self.btn_parar.pack(side='left', padx=15)
        
        # ===== CARD LOG =====
        log_card = self.criar_card(main, "[ LOG ]", self.cores['neon_purple'])
        
        log_container = tk.Frame(log_card, bg=self.cores['bg_card'])
        log_container.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        # Scrollbar
        scrollbar = tk.Scrollbar(log_container, bg=self.cores['bg_card'])
        scrollbar.pack(side='right', fill='y')
        
        # Área de log
        self.log_text = tk.Text(log_container, height=10,
                                font=('Consolas', 9),
                                bg=self.cores['bg'], fg=self.cores['text'],
                                relief='flat', bd=0,
                                yscrollcommand=scrollbar.set,
                                wrap='word')
        self.log_text.pack(side='left', fill='both', expand=True)
        scrollbar.config(command=self.log_text.yview)
        
        # Cores neon para as tags
        self.log_text.tag_config('info', foreground=self.cores['neon_cyan'])
        self.log_text.tag_config('error', foreground=self.cores['neon_pink'])
        self.log_text.tag_config('warning', foreground=self.cores['neon_yellow'])
        self.log_text.tag_config('success', foreground=self.cores['neon_green'])
        
        # ===== FOOTER (RODAPÉ) =====
        footer = tk.Frame(main, bg=self.cores['bg'], height=40)
        footer.pack(fill='x', side='bottom')
        footer.pack_propagate(False)
        
        # Linha decorativa
        line = tk.Label(footer, text="═" * 40, 
                       font=('Consolas', 8),
                       bg=self.cores['bg'], fg=self.cores['neon_purple'])
        line.pack()
        
        # Créditos
        credit_frame = tk.Frame(footer, bg=self.cores['bg'])
        credit_frame.pack(pady=5)
        
        tk.Label(credit_frame, text="produzido por", 
                font=('Consolas', 8),
                bg=self.cores['bg'], fg=self.cores['text_dim']).pack(side='left')
        
        tk.Label(credit_frame, text=" Misa ", 
                font=('Consolas', 9, 'bold'),
                bg=self.cores['bg'], fg=self.cores['neon_green']).pack(side='left')
        
        tk.Label(credit_frame, text="|", 
                font=('Consolas', 8),
                bg=self.cores['bg'], fg=self.cores['text_dim']).pack(side='left', padx=5)
        
        tk.Label(credit_frame, text=" v2.0 ", 
                font=('Consolas', 8),
                bg=self.cores['bg'], fg=self.cores['neon_cyan']).pack(side='left')
        
        # Status bar no canto direito
        status_frame = tk.Frame(footer, bg=self.cores['bg'])
        status_frame.pack(side='right', padx=10)
        
        self.status_led = tk.Label(status_frame, text="●", 
                                   font=('Consolas', 10),
                                   bg=self.cores['bg'], fg=self.cores['neon_green'])
        self.status_led.pack(side='left', padx=(0, 5))
        
        self.status_var = tk.StringVar(value="ready")
        status_label = tk.Label(status_frame, textvariable=self.status_var,
                                font=('Consolas', 8),
                                bg=self.cores['bg'], fg=self.cores['neon_cyan'])
        status_label.pack(side='left')
        
        # Animação
        self.animar_icone()
    
    def animar_icone(self):
        icones = ["⚡", "▶", "❯", "$"]
        if hasattr(self, 'icon_index'):
            self.icon_index = (self.icon_index + 1) % len(icones)
        else:
            self.icon_index = 0
        
        self.icon_label.config(text=icones[self.icon_index])
        self.root.after(1500, self.animar_icone)
    
    def log(self, msg, tipo='info'):
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        prefixos = {
            'info': '[INFO]',
            'error': '[ERRO]',
            'warning': '[WARN]',
            'success': '[ OK ]'
        }
        
        prefixo = prefixos.get(tipo, '[???]')
        self.log_text.insert(tk.END, f"[{timestamp}] {prefixo} {msg}\n", tipo)
        self.log_text.see(tk.END)
        self.root.update_idletasks()
    
    def atualizar_status_ui(self, tipo, *args):
        if tipo == "progresso":
            idx, total = args
            percent = (idx / total) * 100
            self.status_var.set(f"running {idx}/{total}")
            self.status_led.config(fg=self.cores['neon_yellow'])
            self.log(f"Processando {idx}/{total}", 'info')
        elif tipo == "info":
            self.log(args[0], 'info')
        elif tipo == "erro":
            self.log(args[0], 'error')
            self.status_led.config(fg=self.cores['neon_pink'])
    
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
            self.log("═" * 40, 'info')
            self.log("Iniciando AutoPes V2", 'success')
            self.log("═" * 40, 'info')
            self.log("Abrindo navegador...", 'info')
            
            self.status_var.set("booting")
            self.status_led.config(fg=self.cores['neon_yellow'])
            
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
            self.log("═" * 40, 'success')
            self.log("Automação concluída com sucesso!", 'success')
            self.log("═" * 40, 'success')
            self.status_var.set("completed")
            self.status_led.config(fg=self.cores['neon_green'])
            messagebox.showinfo("Sucesso", "✅ Automação finalizada!")
        else:
            self.log("═" * 40, 'warning')
            self.log("Automação concluída com falhas", 'warning')
            self.log("═" * 40, 'warning')
            self.status_var.set("errors")
            self.status_led.config(fg=self.cores['neon_pink'])
            messagebox.showwarning("Atenção", "⚠️ Algumas falhas ocorreram")
    
    def parar(self):
        if hasattr(self, 'automacao') and self.automacao.executando:
            self.automacao.parar()
            self.log("Parada solicitada", 'warning')
            self.status_var.set("stopping")
    
    def run(self):
        self.root.mainloop()