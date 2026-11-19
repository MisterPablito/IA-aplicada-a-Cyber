"""Verifica serialização, reprodução e contrato das entradas de previsão."""

import tempfile
from pathlib import Path
import unittest

import pandas as pd

from src.dados import RAIZ, carregar_dados, dividir_dados
from src.preparacao import selecionar_entradas
from src.previsoes import carregar_artefacto, prever_batch, treinar_artefacto


class TestarPrevisoes(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temporario = tempfile.TemporaryDirectory(dir=RAIZ / ".venv", prefix="teste-previsoes-")
        cls.caminho = Path(cls.temporario.name) / "modelo.joblib"
        cls.artefacto = treinar_artefacto(cls.caminho)
        cls.X = selecionar_entradas(dividir_dados(carregar_dados())["treino"].head(3))

    @classmethod
    def tearDownClass(cls):
        if not Path(cls.temporario.name).resolve().is_relative_to((RAIZ / ".venv").resolve()):
            raise AssertionError("Pasta temporária fora do espaço previsto.")
        cls.temporario.cleanup()

    def test_serializacao_e_reproducao(self):
        antes = prever_batch(self.X, self.artefacto)
        depois = prever_batch(self.X, carregar_artefacto(self.caminho))
        pd.testing.assert_frame_equal(antes, depois)
        self.assertEqual(len(depois), len(self.X))
        self.assertEqual(list(depois.Previsao), ["Suspicious"] * len(self.X))

    def test_campos_proibidos_recusados(self):
        for coluna in ["Label", "Label_bin", "Anomaly_Type"]:
            with self.subTest(coluna=coluna), self.assertRaises(ValueError):
                prever_batch(self.X.assign(**{coluna: 1}), self.artefacto)

    def test_campos_em_falta_e_batch_vazio(self):
        for X in [self.X.drop(columns="Timestamp"), self.X.iloc[:0]]:
            with self.assertRaises(ValueError):
                prever_batch(X, self.artefacto)


if __name__ == "__main__":
    unittest.main()
