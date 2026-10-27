"""Confirma a integridade da decisão anterior ao teste sem avaliar o teste."""

import copy
import unittest

from src.avaliacao_final import ASSINATURA_DECISAO, assinatura_decisao, carregar_decisao


class TestarDecisao(unittest.TestCase):
    def test_decisao_congelada_antes_do_teste(self):
        decisao = carregar_decisao()
        self.assertFalse(decisao["teste_utilizado"])
        self.assertEqual(assinatura_decisao(decisao), ASSINATURA_DECISAO)
        alterada = copy.deepcopy(decisao)
        alterada["selecionado"]["familia"] = "outro_modelo"
        self.assertNotEqual(assinatura_decisao(alterada), ASSINATURA_DECISAO)


if __name__ == "__main__":
    unittest.main()
