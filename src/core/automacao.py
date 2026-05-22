"""
Automação principal
"""

import random
import time
import json
import subprocess
from pathlib import Path

import pyautogui
import requests

from src.utils.logger import get_logger
from src.utils.csv_manager import CSVManager

class Automacao:
    def __init__(self):
        self.logger = get_logger()
        self.csv_manager = CSVManager()
        self.config = self._load_config()
        self.resultados = []
        self.executando = False
        
        pyautogui.FAILSAFE = True
    
    def _load_config(self):
        config_path = Path(__file__).parent.parent.parent / "config" / "settings.json"
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {
                "timeouts": {"abrir_navegador": 3, "minimo_pagina": 8, "entre_pesquisas": [5, 10]},
                "temas": ["tecnologia", "saude"],
                "perguntas": ["O que é {tema}?"]
            }
    
    def gerar_pesquisas(self, num_temas, num_perguntas):
        temas = self.config.get("temas", [])
        perguntas_base = self.config.get("perguntas", [])
        
        num_temas = min(num_temas, len(temas))
        num_perguntas = min(num_perguntas, len(perguntas_base))
        
        temas_escolhidos = random.sample(temas, num_temas)
        pesquisas = []
        
        for tema in temas_escolhidos:
            perguntas = random.sample(perguntas_base, num_perguntas)
            for pergunta in perguntas:
                pesquisas.append({
                    'tema': tema,
                    'pergunta': pergunta.format(tema=tema)
                })
        
        return pesquisas
    
    def verificar_internet(self):
        try:
            requests.get('https://www.google.com', timeout=5)
            return True
        except:
            return False
    
    def abrir_edge(self):
        try:
            subprocess.run(['taskkill', '/IM', 'msedge.exe', '/F'], capture_output=True)
            time.sleep(1)
            subprocess.Popen(['start', 'msedge'], shell=True)
            time.sleep(self.config['timeouts']['abrir_navegador'])
            return True
        except:
            return False
    
    def fazer_pesquisa(self, pergunta):
        try:
            pyautogui.hotkey('ctrl', 't')
            time.sleep(1)
            pyautogui.write(pergunta)
            time.sleep(0.5)
            pyautogui.press('enter')
            time.sleep(self.config['timeouts']['minimo_pagina'])
            pyautogui.hotkey('ctrl', 'w')
            return True
        except:
            return False
    
    def fechar_edge(self):
        try:
            subprocess.run(['taskkill', '/IM', 'msedge.exe', '/F'], capture_output=True)
            self.logger.info("Edge fechado")
        except:
            pass
    
    def executar(self, num_temas, num_perguntas, callback=None):
        self.executando = True
        self.resultados = []
        
        if not self.verificar_internet():
            if callback: callback("erro", "Sem internet")
            return False
        
        if not self.abrir_edge():
            if callback: callback("erro", "Não abriu Edge")
            return False
        
        try:
            pesquisas = self.gerar_pesquisas(num_temas, num_perguntas)
            total = len(pesquisas)
            
            for idx, p in enumerate(pesquisas, 1):
                if not self.executando:
                    break
                
                if callback:
                    callback("progresso", idx, total)
                
                sucesso = self.fazer_pesquisa(p['pergunta'])
                
                self.resultados.append({
                    'tema': p['tema'],
                    'pergunta': p['pergunta'],
                    'status': 'OK' if sucesso else 'FALHA'
                })
                
                if idx < total:
                    intervalo = random.uniform(*self.config['timeouts']['entre_pesquisas'])
                    time.sleep(intervalo)
            
            self.csv_manager.salvar(self.resultados)
            return True
            
        finally:
            self.fechar_edge()
            self.executando = False
    
    def parar(self):
        self.executando = False