"""Persistência dos resultados em CSV compatível com Excel."""

import csv
from datetime import datetime
from pathlib import Path

from src.utils.paths import data_dir


class CSVManager:
    def __init__(self) -> None:
        self.pasta = data_dir() / "resultados"
        self.pasta.mkdir(parents=True, exist_ok=True)

    def salvar(self, resultados: list[dict[str, str]]) -> Path | None:
        if not resultados:
            return None
        arquivo = self.pasta / f"resultados_{datetime.now():%Y%m%d_%H%M%S}.csv"
        with arquivo.open("w", newline="", encoding="utf-8-sig") as destino:
            escritor = csv.DictWriter(destino, fieldnames=["tema", "pergunta", "status", "erro"], extrasaction="ignore")
            escritor.writeheader()
            escritor.writerows(resultados)
        return arquivo
