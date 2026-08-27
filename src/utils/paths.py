"""Caminhos de recursos e dados, compatíveis com execução Python e PyInstaller."""

import os
import sys
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parents[2]
RESOURCE_DIR = Path(getattr(sys, "_MEIPASS", PROJECT_DIR))


def data_dir() -> Path:
    """Retorna um diretório gravável e persistente para logs, CSVs e perfil isolado."""
    if getattr(sys, "frozen", False):
        base = Path(os.environ.get("LOCALAPPDATA", str(PROJECT_DIR))) / "AutoPesV2"
    else:
        base = PROJECT_DIR / "data"
    base.mkdir(parents=True, exist_ok=True)
    return base
