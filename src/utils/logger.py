"""Configuração centralizada de logs da aplicação."""

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from src.utils.paths import data_dir

_logger: logging.Logger | None = None


def setup_logger() -> logging.Logger:
    global _logger
    logger = logging.getLogger("AutoPesV2")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    if not logger.handlers:
        pasta = data_dir() / "logs"
        pasta.mkdir(parents=True, exist_ok=True)
        formato = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")
        arquivo = RotatingFileHandler(pasta / "autopes.log", maxBytes=1_000_000, backupCount=5, encoding="utf-8")
        arquivo.setFormatter(formato)
        logger.addHandler(arquivo)
    _logger = logger
    return logger


def get_logger() -> logging.Logger:
    return _logger or setup_logger()
