"""Verifica a regra de seleção e a integração do limiar com o estimador."""

import unittest
import numpy as np
from sklearn.dummy import DummyClassifier

from src.otimizacao import ClassificadorComLimiar, selecionar_simples


class TestarOtimizacao(unittest.TestCase):
    def test_preferencia_por_simplicidade_dentro_de_um_erro_padrao(self):
        simples = {"familia": "sempre_suspeita", "f1_cv": 0.28, "desvio_f1_cv": 0.01, "ap_cv": 0.16}
        complexo = {"familia": "arvore", "f1_cv": 0.281, "desvio_f1_cv": 0.02, "ap_cv": 0.17}
        escolhido, _ = selecionar_simples([simples, complexo])
        self.assertEqual(escolhido["familia"], "sempre_suspeita")
        complexo["f1_cv"] = 0.5
        escolhido, _ = selecionar_simples([simples, complexo])
        self.assertEqual(escolhido["familia"], "arvore")

    def test_limiar_nao_altera_as_pontuacoes(self):
        X, y = np.zeros((4, 1)), [0, 0, 0, 1]
        baixo = ClassificadorComLimiar(DummyClassifier(strategy="prior"), limiar=0.0).fit(X, y)
        alto = ClassificadorComLimiar(DummyClassifier(strategy="prior"), limiar=0.5).fit(X, y)
        np.testing.assert_array_equal(baixo.predict(X), [1, 1, 1, 1])
        np.testing.assert_array_equal(alto.predict(X), [0, 0, 0, 0])
        np.testing.assert_array_equal(baixo.predict_proba(X), alto.predict_proba(X))


if __name__ == "__main__":
    unittest.main()
