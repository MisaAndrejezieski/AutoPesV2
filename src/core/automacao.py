"""Serviço de automação de pesquisas executado fora da thread da interface."""

from __future__ import annotations

import json
import os
import random
import subprocess
import threading
from dataclasses import dataclass
from pathlib import Path
from typing import Callable
from urllib.parse import quote_plus

import pyautogui
import requests

from src.utils.csv_manager import CSVManager
from src.utils.logger import get_logger
from src.utils.paths import RESOURCE_DIR, data_dir


Callback = Callable[..., None]


@dataclass(frozen=True)
class RelatorioExecucao:
    """Resumo imutável devolvido ao fim de uma execução."""

    concluida: bool
    cancelada: bool
    sucesso: int
    falha: int
    arquivo_csv: Path | None = None


class Automacao:
    def __init__(self) -> None:
        self.logger = get_logger()
        self.csv_manager = CSVManager()
        self.config = self._load_config()
        self.resultados: list[dict[str, str]] = []
        self.executando = False
        self._parar_evento = threading.Event()
        self._processo_edge: subprocess.Popen | None = None
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.05

    def _load_config(self) -> dict:
        caminho = RESOURCE_DIR / "config" / "settings.json"
        try:
            with caminho.open("r", encoding="utf-8") as arquivo:
                config = json.load(arquivo)
            self._validar_config(config)
            return config
        except (OSError, json.JSONDecodeError, ValueError) as erro:
            self.logger.warning("Configuração inválida (%s). Usando valores padrão.", erro)
            return {
                "timeouts": {"abrir_navegador": 3, "entre_teclas": 0.05,
                             "minimo_pagina": 8, "entre_pesquisas": [5, 10]},
                "temas": ["tecnologia", "saúde"],
                "perguntas": ["O que é {tema}?"],
            }

    @staticmethod
    def _validar_config(config: dict) -> None:
        if not isinstance(config, dict):
            raise ValueError("A configuração deve ser um objeto JSON")
        timeouts = config.get("timeouts", {})
        intervalo = timeouts.get("entre_pesquisas", [])
        obrigatorios = {"abrir_navegador", "entre_teclas", "minimo_pagina"}
        if not isinstance(timeouts, dict) or not obrigatorios.issubset(timeouts):
            raise ValueError("Tempos de execução incompletos")
        if not config.get("temas") or not config.get("perguntas"):
            raise ValueError("'temas' e 'perguntas' não podem estar vazios")
        if len(intervalo) != 2 or any(float(valor) < 0 for valor in intervalo):
            raise ValueError("'entre_pesquisas' deve conter dois tempos não negativos")
        if float(intervalo[0]) > float(intervalo[1]):
            raise ValueError("O intervalo mínimo não pode ser maior que o máximo")

    def gerar_pesquisas(self, num_temas: int, num_perguntas: int) -> list[dict[str, str]]:
        if num_temas < 1 or num_perguntas < 1:
            raise ValueError("A quantidade de temas e perguntas deve ser maior que zero.")

        temas = self.config["temas"]
        perguntas_base = self.config["perguntas"]
        temas_escolhidos = random.sample(temas, min(num_temas, len(temas)))
        pesquisas = []
        for tema in temas_escolhidos:
            # A ordem configurada forma uma trilha de estudo, dos fundamentos a pratica.
            for pergunta in perguntas_base[:min(num_perguntas, len(perguntas_base))]:
                pesquisas.append({"tema": tema, "pergunta": pergunta.format(tema=tema)})
        return pesquisas

    def verificar_internet(self) -> bool:
        try:
            resposta = requests.get("https://www.bing.com", timeout=5)
            resposta.raise_for_status()
            return True
        except requests.RequestException as erro:
            self.logger.warning("Não foi possível verificar a conexão: %s", erro)
            return False

    @staticmethod
    def _localizar_edge() -> str:
        candidatos = [
            Path(os.environ.get("PROGRAMFILES", r"C:\Program Files")) / "Microsoft" / "Edge" / "Application" / "msedge.exe",
            Path(os.environ.get("PROGRAMFILES(X86)", r"C:\Program Files (x86)")) / "Microsoft" / "Edge" / "Application" / "msedge.exe",
            Path(os.environ.get("LOCALAPPDATA", "")) / "Microsoft" / "Edge" / "Application" / "msedge.exe",
        ]
        for caminho in candidatos:
            if caminho.is_file():
                return str(caminho)
        return "msedge.exe"

    def _esperar(self, segundos: float) -> bool:
        """Espera de modo cancelável; retorna False se o usuário pediu parada."""
        return not self._parar_evento.wait(max(0, segundos))

    def abrir_edge(self) -> bool:
        try:
            if self._processo_edge is not None and self._processo_edge.poll() is None:
                self.fechar_edge()
            perfil = data_dir() / "edge-profile"
            perfil.mkdir(parents=True, exist_ok=True)
            flags = getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0)
            self._processo_edge = subprocess.Popen(
                [self._localizar_edge(), "--new-window", "--no-first-run", "--no-default-browser-check",
                 f"--user-data-dir={perfil}", "https://www.bing.com"],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, creationflags=flags,
            )
            self.logger.info("Edge iniciado em perfil isolado (PID %s).", self._processo_edge.pid)
            return self._esperar(float(self.config["timeouts"]["abrir_navegador"]))
        except OSError:
            self.logger.exception("Falha ao iniciar o Microsoft Edge.")
            return False

    def fazer_pesquisa(self, pergunta: str) -> tuple[bool, str]:
        """Pesquisa por URL codificada, inclusive para consultas com acentos."""
        try:
            if self._parar_evento.is_set():
                return False, "Cancelada pelo usuário"
            url = self.url_pesquisa(pergunta)
            pyautogui.hotkey("ctrl", "l")
            pyautogui.write(url, interval=float(self.config["timeouts"].get("entre_teclas", 0.05)))
            pyautogui.press("enter")
            if not self._esperar(float(self.config["timeouts"]["minimo_pagina"])):
                return False, "Cancelada pelo usuário"
            return True, ""
        except pyautogui.PyAutoGUIException as erro:
            self.logger.exception("Falha ao realizar pesquisa: %s", pergunta)
            return False, str(erro)

    @staticmethod
    def url_pesquisa(pergunta: str) -> str:
        return f"https://www.bing.com/search?q={quote_plus(pergunta)}"

    def fechar_edge(self) -> None:
        processo = self._processo_edge
        self._processo_edge = None
        if processo is None or processo.poll() is not None:
            return
        try:
            # Encerra somente a árvore iniciada por este aplicativo, nunca o Edge do usuário.
            subprocess.run(["taskkill", "/PID", str(processo.pid), "/T", "/F"],
                           capture_output=True, check=False, timeout=10)
        except (OSError, subprocess.TimeoutExpired):
            self.logger.exception("Não foi possível encerrar o Edge isolado.")
        else:
            self.logger.info("Edge isolado fechado.")

    @staticmethod
    def _notificar(callback: Callback | None, tipo: str, *args: object) -> None:
        if callback:
            callback(tipo, *args)

    def executar(self, num_temas: int, num_perguntas: int, callback: Callback | None = None) -> RelatorioExecucao:
        self.executando = True
        self._parar_evento.clear()
        self.resultados = []
        manter_edge_aberto = False
        try:
            pesquisas = self.gerar_pesquisas(num_temas, num_perguntas)
            if not self.verificar_internet():
                self._notificar(callback, "erro", "Sem conexão com a internet.")
                return RelatorioExecucao(False, False, 0, 0)
            self._notificar(callback, "info", "Abrindo navegador em perfil isolado...")
            if not self.abrir_edge():
                cancelada = self._parar_evento.is_set()
                self._notificar(callback, "erro", "Execução cancelada." if cancelada else "Não foi possível abrir o Edge.")
                return RelatorioExecucao(False, cancelada, 0, 0)

            for indice, pesquisa in enumerate(pesquisas, start=1):
                if self._parar_evento.is_set():
                    break
                self._notificar(callback, "progresso", indice, len(pesquisas))
                sucesso, erro = self.fazer_pesquisa(pesquisa["pergunta"])
                self.resultados.append({
                    **pesquisa,
                    "url": self.url_pesquisa(pesquisa["pergunta"]),
                    "status": "OK" if sucesso else "FALHA",
                    "erro": erro,
                })
                if indice < len(pesquisas) and not self._parar_evento.is_set():
                    minimo, maximo = self.config["timeouts"]["entre_pesquisas"]
                    if not self._esperar(random.uniform(float(minimo), float(maximo))):
                        break

            cancelada = self._parar_evento.is_set()
            arquivo = self.csv_manager.salvar(self.resultados)
            sucesso = sum(item["status"] == "OK" for item in self.resultados)
            falha = len(self.resultados) - sucesso
            if cancelada:
                self._notificar(callback, "info", "Execução cancelada. Resultados parciais foram salvos.")
            manter_edge_aberto = not cancelada and falha == 0
            return RelatorioExecucao(manter_edge_aberto, cancelada, sucesso, falha, arquivo)
        except (ValueError, KeyError, TypeError) as erro:
            self.logger.exception("Configuração ou parâmetros inválidos.")
            self._notificar(callback, "erro", str(erro))
            return RelatorioExecucao(False, False, 0, 0)
        finally:
            if manter_edge_aberto:
                self._notificar(callback, "info", "Edge mantido aberto na ultima pagina pesquisada.")
            else:
                self.fechar_edge()
            self.executando = False

    def parar(self) -> None:
        self._parar_evento.set()
