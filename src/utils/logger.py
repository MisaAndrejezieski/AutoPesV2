"""
Sistema de logging simplificado
"""

import logging
from pathlib import Path
from datetime import datetime

_logger = None

def setup_logger():
    global _logger
    
    # Pasta de logs
    log_dir = Path(__file__).parent.parent.parent / "data" / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    
    # Arquivo de log do dia
    log_file = log_dir / f"automacao_{datetime.now().strftime('%Y%m%d')}.log"
    
    # Configurar
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    
    _logger = logging.getLogger('AutoPesV2')
    return _logger

def get_logger():
    global _logger
    if _logger is None:
        return setup_logger()
    return _logger