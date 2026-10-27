"""Verifica exclusões, ausências estruturais e ausência de aprendizagem na validação."""

import unittest
import numpy as np

from src.dados import carregar_dados, dividir_dados
from src.preparacao import PROIBIDAS, PrepararCaracteristicas, criar_preparacao, selecionar_entradas


class TestarPreparacao(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.partes = dividir_dados(carregar_dados())

    def test_colunas_proibidas_excluidas_e_recusadas(self):
        df = self.partes["treino"].copy()
        df["Label_bin"] = (df.Label == "Suspicious").astype(int)
        X = selecionar_entradas(df)
        self.assertFalse(PROIBIDAS & set(X.columns))
        with self.assertRaises(ValueError):
            PrepararCaracteristicas().fit(df)

    def test_validacao_nao_altera_categorias_ou_escala(self):
        treino = selecionar_entradas(self.partes["treino"])
        validacao = selecionar_entradas(self.partes["validacao"])
        preparacao = criar_preparacao().fit(treino)
        colunas = preparacao.named_steps["colunas"]
        escala = colunas.named_transformers_["numericas"].named_steps["escalar"]
        media = escala.mean_.copy()
        categorias = colunas.named_transformers_["categoricas"].named_steps["codificar"].categories_
        validacao.loc[:, "Resource_Accessed"] = "/apenas_na_validacao"
        matriz = preparacao.transform(validacao)
        self.assertTrue(np.isfinite(matriz).all())
        np.testing.assert_array_equal(media, escala.mean_)
        self.assertEqual(escala.n_samples_seen_, len(treino))
        self.assertFalse(any("/apenas_na_validacao" in set(c) for c in categorias))

    def test_ausencia_estrutural_e_desconhecida_distintas(self):
        X = selecionar_entradas(self.partes["treino"])
        preparado = PrepararCaracteristicas().fit_transform(X)
        sem_login = ~X.Activity_Type.isin(["Login", "Remote_Login"])
        self.assertTrue((preparado.loc[sem_login, "Login_Attempts"] == 0).all())
        desconhecido = X.loc[X.Activity_Type == "Login"].head(1).copy()
        desconhecido.loc[:, "Login_Attempts"] = np.nan
        with self.assertRaises(ValueError):
            PrepararCaracteristicas().fit_transform(desconhecido)

    def test_valores_invalidos_recusados(self):
        X = selecionar_entradas(self.partes["treino"])
        X = X.loc[X.Activity_Type == "Login"].head(1).copy()
        X.loc[:, "Login_Attempts"] = -1
        with self.assertRaises(ValueError):
            PrepararCaracteristicas().fit_transform(X)


if __name__ == "__main__":
    unittest.main()
