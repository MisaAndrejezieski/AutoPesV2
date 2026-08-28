import threading
import unittest
from pathlib import Path
from unittest.mock import Mock

from src.core.automacao import Automacao


class AutomacaoTests(unittest.TestCase):
    def setUp(self):
        self.automacao = Automacao()
        self.automacao.config = {
            "timeouts": {"abrir_navegador": 0, "entre_teclas": 0, "minimo_pagina": 0,
                         "entre_pesquisas": [0, 0]},
            "temas": ["tecnologia", "saúde"],
            "perguntas": ["O que é {tema}?", "Futuro do {tema}"],
        }

    def test_gera_quantidade_esperada(self):
        pesquisas = self.automacao.gerar_pesquisas(2, 2)
        self.assertEqual(len(pesquisas), 4)
        self.assertTrue(all("{" not in item["pergunta"] for item in pesquisas))
        for inicio in range(0, len(pesquisas), 2):
            self.assertTrue(pesquisas[inicio]["pergunta"].startswith("O que"))
            self.assertTrue(pesquisas[inicio + 1]["pergunta"].startswith("Futuro"))

    def test_rejeita_quantidades_invalidas(self):
        with self.assertRaises(ValueError):
            self.automacao.gerar_pesquisas(0, 1)

    def test_execucao_cria_relatorio_sem_abrir_navegador_real(self):
        self.automacao.verificar_internet = Mock(return_value=True)
        self.automacao.abrir_edge = Mock(return_value=True)
        self.automacao.fazer_pesquisa = Mock(return_value=(True, ""))
        self.automacao.fechar_edge = Mock()
        self.automacao.csv_manager.salvar = Mock(return_value=Path("resultado.csv"))

        relatorio = self.automacao.executar(1, 1)

        self.assertTrue(relatorio.concluida)
        self.assertEqual((relatorio.sucesso, relatorio.falha), (1, 0))
        self.automacao.csv_manager.salvar.assert_called_once()

    def test_espera_e_interrompida_pelo_evento(self):
        self.automacao._parar_evento = threading.Event()
        self.automacao._parar_evento.set()
        self.assertFalse(self.automacao._esperar(10))


if __name__ == "__main__":
    unittest.main()
