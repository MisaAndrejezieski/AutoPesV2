"""
Interface Dark Mode com Neon - Centralizada com Rodapé
"""

import tkinter as tk
from tkinter import messagebox
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
        self.root.geometry("600x580")
        self.root.minsize(550, 530)
        
        self.cores = {
            'bg': '#0D0D0D',
            'bg_card': '#1A1A1A',
            'neon_cyan': '#00FFD1',
            'neon_pink': '#FF007F',
            'neon_green': '#39FF14',
            'neon_yellow': '#FFE600',
            'neon_purple': '#B300FF',
            'text': '#E0E0E0',
            'input_bg': '#2A2A2A',
        }
        
        self.root.configure(bg=self.cores['bg'])
        self.root.eval('tk::PlaceWindow . center')
    
    def setup_widgets(self):
        # Container principal
        main = tk.Frame(self.root, bg=self.cores['bg'])
        main.pack(fill='both', expand=True)
        
        # Conteúdo centralizado
        content = tk.Frame(main, bg=self.cores['bg'])
        content.pack(expand=True, fill='both')
        
        # Título
        tk.Label(content, text="AutoPes V2", 
                font=('Consolas', 26, 'bold'),
                bg=self.cores['bg'], fg=self.cores['neon_pink']).pack(pady=(20, 5))
        
        # Linha
        tk.Label(content, text="═" * 30, 
                font=('Consolas', 8),
                bg=self.cores['bg'], fg=self.cores['neon_purple']).pack(pady=5)
        
        # ===== CARD CONFIGURAÇÕES =====
        config_card = tk.Frame(content, bg=self.cores['bg_card'])
        config_card.pack(pady=10, padx=40, fill='x')
        
        tk.Frame(config_card, bg=self.cores['neon_cyan'], height=2).pack(fill='x')
        
        tk.Label(config_card, text="[ CONFIGURAÇÕES ]", 
                font=('Consolas', 11, 'bold'),
                bg=self.cores['bg_card'], fg=self.cores['neon_cyan']).pack(pady=(12, 12))
        
        # Temas
        row1 = tk.Frame(config_card, bg=self.cores['bg_card'])
        row1.pack(pady=4)
        tk.Label(row1, text="TEMAS:", font=('Consolas', 10, 'bold'),
                bg=self.cores['bg_card'], fg=self.cores['neon_yellow']).pack(side='left', padx=(0, 15))
        self.num_temas = tk.Spinbox(row1, from_=1, to=10, width=6,
                                    font=('Consolas', 11),
                                    bg=self.cores['input_bg'], fg=self.cores['neon_green'],
                                    relief='flat')
        self.num_temas.pack(side='left')
        self.num_temas.delete(0, 'end')
        self.num_temas.insert(0, "1")
        
        # Perguntas
        row2 = tk.Frame(config_card, bg=self.cores['bg_card'])
        row2.pack(pady=8)
        tk.Label(row2, text="PERGUNTAS POR TEMA:", font=('Consolas', 10, 'bold'),
                bg=self.cores['bg_card'], fg=self.cores['neon_yellow']).pack(side='left', padx=(0, 15))
        self.num_perguntas = tk.Spinbox(row2, from_=1, to=6, width=6,
                                        font=('Consolas', 11),
                                        bg=self.cores['input_bg'], fg=self.cores['neon_green'],
                                        relief='flat')
        self.num_perguntas.pack(side='left')
        self.num_perguntas.delete(0, 'end')
        self.num_perguntas.insert(0, "6")
        
        tk.Frame(config_card, bg=self.cores['bg_card'], height=8).pack()
        
        # ===== CARD CONTROLES =====
        control_card = tk.Frame(content, bg=self.cores['bg_card'])
        control_card.pack(pady=8, padx=40, fill='x')
        
        tk.Frame(control_card, bg=self.cores['neon_pink'], height=2).pack(fill='x')
        
        tk.Label(control_card, text="[ CONTROLES ]", 
                font=('Consolas', 11, 'bold'),
                bg=self.cores['bg_card'], fg=self.cores['neon_pink']).pack(pady=(12, 12))
        
        btn_frame = tk.Frame(control_card, bg=self.cores['bg_card'])
        btn_frame.pack(pady=8)
        
        self.btn_iniciar = tk.Button(btn_frame, text="▶ INICIAR", 
                                     command=self.iniciar,
                                     bg='#1A1A1A', fg=self.cores['neon_green'],
                                     font=('Consolas', 10, 'bold'),
                                     padx=22, pady=7,
                                     relief='flat', cursor='hand2')
        self.btn_iniciar.pack(side='left', padx=10)
        
        self.btn_parar = tk.Button(btn_frame, text="⏹ PARAR", 
                                   command=self.parar,
                                   bg='#1A1A1A', fg=self.cores['neon_pink'],
                                   font=('Consolas', 10, 'bold'),
                                   padx=22, pady=7,
                                   relief='flat', cursor='hand2',
                                   state='disabled')
        self.btn_parar.pack(side='left', padx=10)
        
        tk.Frame(control_card, bg=self.cores['bg_card'], height=12).pack()
        
        # ===== CARD LOG =====
        log_card = tk.Frame(content, bg=self.cores['bg_card'])
        log_card.pack(pady=8, padx=40, fill='x')
        
        tk.Frame(log_card, bg=self.cores['neon_purple'], height=2).pack(fill='x')
        
        tk.Label(log_card, text="[ LOG ]", 
                font=('Consolas', 11, 'bold'),
                bg=self.cores['bg_card'], fg=self.cores['neon_purple']).pack(pady=(12, 8))
        
        # Log
        self.log_text = tk.Text(log_card, height=7,
                                font=('Consolas', 9),
                                bg=self.cores['bg'], fg=self.cores['text'],
                                relief='flat', bd=0,
                                wrap='word')
        self.log_text.pack(fill='both', expand=True, padx=15, pady=(0, 15))
        
        self.log_text.tag_config('info', foreground=self.cores['neon_cyan'])
        self.log_text.tag_config('error', foreground=self.cores['neon_pink'])
        self.log_text.tag_config('warning', foreground=self.cores['neon_yellow'])
        self.log_text.tag_config('success', foreground=self.cores['neon_green'])
        
        # ===== RODAPÉ (CRÉDITOS) =====
        footer = tk.Frame(main, bg=self.cores['bg'], height=50)
        footer.pack(fill='x', side='bottom')
        footer.pack_propagate(False)
        
        # Linha decorativa
        tk.Label(footer, text="═" * 35, 
                font=('Consolas', 8),
                bg=self.cores['bg'], fg=self.cores['neon_purple']).pack()
        
        # Créditos
        credit_frame = tk.Frame(footer, bg=self.cores['bg'])
        credit_frame.pack(pady=8)
        
        tk.Label(credit_frame, text="produzido por", 
                font=('Consolas', 8),
                bg=self.cores['bg'], fg='#808080').pack(side='left')
        
        tk.Label(credit_frame, text=" Misa ", 
                font=('Consolas', 9, 'bold'),
                bg=self.cores['bg'], fg=self.cores['neon_green']).pack(side='left')
        
        tk.Label(credit_frame, text="| v2.0", 
                font=('Consolas', 8),
                bg=self.cores['bg'], fg=self.cores['neon_cyan']).pack(side='left')
        
        # Status
        self.status_var = tk.StringVar(value="ready")
        tk.Label(footer, textvariable=self.status_var,
                font=('Consolas', 8),
                bg=self.cores['bg'], fg=self.cores['neon_cyan']).pack(side='right', padx=15)
    
    def log(self, msg, tipo='info'):
        timestamp = datetime.now().strftime("%H:%M:%S")
        prefixos = {'info': '[INFO]', 'error': '[ERRO]', 'warning': '[WARN]', 'success': '[ OK ]'}
        self.log_text.insert(tk.END, f"[{timestamp}] {prefixos[tipo]} {msg}\n", tipo)
        self.log_text.see(tk.END)
    
    def atualizar_status_ui(self, tipo, *args):
        if tipo == "progresso":
            idx, total = args
            self.status_var.set(f"running {idx}/{total}")
            self.log(f"Pesquisa {idx}/{total}", 'info')
        elif tipo == "info":
            self.log(args[0], 'info')
        elif tipo == "erro":
            self.log(args[0], 'error')
    
    def iniciar(self):
        try:
            num_temas = int(self.num_temas.get())
            num_perguntas = int(self.num_perguntas.get())
            
            self.btn_iniciar.config(state='disabled')
            self.btn_parar.config(state='normal')
            self.num_temas.config(state='disabled')
            self.num_perguntas.config(state='disabled')
            
            self.log_text.delete(1.0, tk.END)
            self.log("═" * 35, 'info')
            self.log("Iniciando AutoPes V2", 'success')
            self.log("═" * 35, 'info')
            
            self.status_var.set("booting...")
            
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
            self.log("═" * 35, 'success')
            self.log("Automação concluída!", 'success')
            self.status_var.set("completed")
            messagebox.showinfo("Sucesso", "Automação finalizada!")
        else:
            self.log("═" * 35, 'warning')
            self.log("Concluída com falhas", 'warning')
            self.status_var.set("errors")
            messagebox.showwarning("Atenção", "Falhas ocorreram")
    
    def parar(self):
        if hasattr(self, 'automacao') and self.automacao.executando:
            self.automacao.parar()
            self.log("Parando...", 'warning')
    
    def run(self):
        self.root.mainloop()