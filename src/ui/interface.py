"""
Interface gráfica
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
        self.root.geometry("600x500")
        self.root.resizable(False, False)
    
    def setup_widgets(self):
        main = ttk.Frame(self.root, padding="20")
        main.pack(fill='both', expand=True)
        
        # Título
        ttk.Label(main, text="🤖 AutoPes V2", font=('Arial', 18, 'bold')).pack(pady=10)
        ttk.Label(main, text="Automação de Pesquisas", font=('Arial', 10)).pack(pady=(0, 20))
        
        # Temas
        ttk.Label(main, text="Número de Temas:").pack(pady=(10, 0))
        self.num_temas = ttk.Spinbox(main, from_=1, to=10, width=20)
        self.num_temas.pack(pady=5)
        self.num_temas.delete(0, 'end')
        self.num_temas.insert(0, "2")
        
        # Perguntas
        ttk.Label(main, text="Perguntas por Tema:").pack(pady=(10, 0))
        self.num_perguntas = ttk.Spinbox(main, from_=1, to=5, width=20)
        self.num_perguntas.pack(pady=5)
        self.num_perguntas.delete(0, 'end')
        self.num_perguntas.insert(0, "2")
        
        # Botões
        btn_frame = ttk.Frame(main)
        btn_frame.pack(pady=20)
        
        self.btn_iniciar = ttk.Button(btn_frame, text="▶ Iniciar", command=self.iniciar)
        self.btn_iniciar.pack(side='left', padx=10)
        
        self.btn_parar = ttk.Button(btn_frame, text="⏹ Parar", command=self.parar, state='disabled')
        self.btn_parar.pack(side='left', padx=10)
        
        # Log
        ttk.Label(main, text="Log:").pack(pady=(10, 0))
        
        log_frame = ttk.Frame(main)
        log_frame.pack(fill='both', expand=True, pady=5)
        
        scroll = ttk.Scrollbar(log_frame)
        scroll.pack(side='right', fill='y')
        
        self.log_text = tk.Text(log_frame, height=12, font=('Consolas', 9), yscrollcommand=scroll.set)
        self.log_text.pack(side='left', fill='both', expand=True)
        scroll.config(command=self.log_text.yview)
        
        # Status
        self.status_var = tk.StringVar(value="Pronto")
        ttk.Label(main, textvariable=self.status_var, font=('Arial', 9, 'italic')).pack(pady=10)
    
    def log(self, msg):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {msg}\n")
        self.log_text.see(tk.END)
    
    def atualizar_status(self, tipo, *args):
        if tipo == "progresso":
            idx, total = args
            self.status_var.set(f"Progresso: {idx}/{total}")
            self.log(f"Pesquisa {idx}/{total}")
        elif tipo == "erro":
            self.log(f"ERRO: {args[0]}")
            self.status_var.set(f"Erro: {args[0][:50]}")
    
    def iniciar(self):
        try:
            num_temas = int(self.num_temas.get())
            num_perguntas = int(self.num_perguntas.get())
            
            self.btn_iniciar.config(state='disabled')
            self.btn_parar.config(state='normal')
            self.num_temas.config(state='disabled')
            self.num_perguntas.config(state='disabled')
            
            self.log_text.delete(1.0, tk.END)
            self.log("🚀 Iniciando automação...")
            
            thread = threading.Thread(target=self._executar, args=(num_temas, num_perguntas), daemon=True)
            thread.start()
            
        except ValueError:
            messagebox.showerror("Erro", "Digite números válidos")
    
    def _executar(self, num_temas, num_perguntas):
        sucesso = self.automacao.executar(num_temas, num_perguntas, self.atualizar_status)
        self.root.after(0, self._finalizar, sucesso)
    
    def _finalizar(self, sucesso):
        self.btn_iniciar.config(state='normal')
        self.btn_parar.config(state='disabled')
        self.num_temas.config(state='normal')
        self.num_perguntas.config(state='normal')
        
        if sucesso:
            self.log("✅ Automação concluída!")
            self.status_var.set("Concluído!")
            messagebox.showinfo("Sucesso", "Automação finalizada!")
        else:
            self.log("⚠️ Automação com falhas")
            self.status_var.set("Concluído com falhas")
    
    def parar(self):
        if hasattr(self, 'automacao'):
            self.automacao.parar()
            self.log("⏹ Parando...")
    
    def run(self):
        self.root.mainloop()