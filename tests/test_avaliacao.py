"""Exemplos conhecidos verificam o sentido das classes e as métricas."""

import unittest
import numpy as np

from src.avaliacao import calcular_metricas
from src.dados import carregar_dados, dividir_dados
from src.experiencias import criar_cv, executar_experiencia


class TestarAvaliacao(unittest.TestCase):
    def test_contagens_e_classe_positiva(self):
        m = calcular_metricas([0, 0, 1, 1], [0, 1, 0, 1], [0.1, 0.6, 0.4, 0.9])
        self.assertEqual([m[k] for k in ["tn", "fp", "fn", "tp"]], [1, 1, 1, 1])
        self.assertEqual(m["f1"], 0.5)
        self.assertEqual(m["recall"], 0.5)
        self.assertEqual(m["roc_auc"], 0.75)

    def test_pontuacoes_invalidas_recusadas(self):
        with self.assertRaises(ValueError):
            calcular_metricas([0, 1], [0, 1], [0, np.nan])

    def test_folds_sem_utilizadores_comuns(self):
        treino = dividir_dados(carregar_dados())["treino"]
        for a, b in criar_cv().split(treino, treino.Label, treino.User_ID):
            self.assertFalse(set(treino.iloc[a].User_ID) & set(treino.iloc[b].User_ID))

    def test_referencias(self):
        normal = executar_experiencia("maioritaria")["validacao"]
        suspeita = executar_experiencia("sempre_suspeita")["validacao"]
        self.assertEqual(normal["recall"], 0)
        self.assertEqual(normal["tp"], 0)
        self.assertTrue(normal["sem_previsoes_positivas"])
        self.assertEqual(suspeita["recall"], 1)
        self.assertEqual(suspeita["tn"], 0)
        self.assertEqual(suspeita["fp"], normal["tn"])


if __name__ == "__main__":
    unittest.main()
