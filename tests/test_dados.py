"""Testes de integridade e da separação entre conjuntos."""

import unittest

from src.dados import carregar_dados, dividir_dados, validar_dados


class TestarDados(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.df = carregar_dados()
        cls.partes = dividir_dados(cls.df)

    def test_integridade_e_classes(self):
        self.assertEqual(self.df.shape, (7400, 11))
        self.assertEqual(int((self.df.Label == "Suspicious").sum()), 1233)
        self.assertIn("N/A", set(self.df.Action))
        self.assertIn("None", set(self.df.Anomaly_Type))

    def test_sem_sobreposicao_de_utilizadores_ou_linhas(self):
        partes = list(self.partes.values())
        for i, a in enumerate(partes):
            for b in partes[i + 1:]:
                self.assertFalse(set(a.User_ID) & set(b.User_ID))
                self.assertFalse(set(a.index) & set(b.index))
        self.assertEqual(set().union(*(set(p.index) for p in partes)), set(self.df.index))

    def test_divisao_reproduzivel(self):
        outra = dividir_dados(self.df)
        for nome in outra:
            self.assertEqual(list(outra[nome].index), list(self.partes[nome].index))

    def test_rotulo_inesperado_recusado(self):
        alterado = self.df.copy()
        alterado.loc[0, "Label"] = "desconhecido"
        with self.assertRaises(ValueError):
            validar_dados(alterado)


if __name__ == "__main__":
    unittest.main()
