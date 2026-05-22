"""
Gerenciador de CSV
"""

import csv
from pathlib import Path
from datetime import datetime

class CSVManager:
    def __init__(self):
        self.pasta = Path(__file__).parent.parent.parent / "data" / "resultados"
        self.pasta.mkdir(parents=True, exist_ok=True)
    
    def salvar(self, resultados):
        if not resultados:
            return False
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        arquivo = self.pasta / f"resultados_{timestamp}.csv"
        
        with open(arquivo, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['tema', 'pergunta', 'status'])
            writer.writeheader()
            writer.writerows(resultados)
        
        print(f"✅ Resultados salvos: {arquivo}")
        return True