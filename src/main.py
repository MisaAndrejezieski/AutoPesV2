"""
Main - Orquestrador da aplicação
"""

import sys
from pathlib import Path

# Adiciona raiz ao path
ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))

from src.core.automacao import Automacao
from src.ui.interface import Interface

def main():
    """Ponto de entrada principal"""
    print("🚀 Iniciando AutoPes V2...")
    
    automacao = Automacao()
    app = Interface(automacao)
    app.run()

if __name__ == "__main__":
    main()