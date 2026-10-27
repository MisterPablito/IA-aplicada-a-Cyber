"""Evita regressões de codificação e ficheiros de notebook inválidos."""

from pathlib import Path
import re
import unittest

import nbformat

from src.dados import RAIZ


class TestarNotebooks(unittest.TestCase):
    def test_fontes_utf8_sem_substituicao_de_acentos(self):
        for caminho in (RAIZ / "notebooks").glob("*.ipynb"):
            with self.subTest(notebook=caminho.name):
                nb = nbformat.read(caminho, as_version=4)
                texto = "\n".join(c.source for c in nb.cells)
                self.assertNotIn("\ufffd", texto)
                self.assertIsNone(re.search(r"[A-Za-zÀ-ÿ]\?[A-Za-zÀ-ÿ]", texto))

    def test_esquema_e_saidas_sem_erros(self):
        for caminho in (RAIZ / "notebooks").glob("*.ipynb"):
            with self.subTest(notebook=caminho.name):
                nb = nbformat.read(caminho, as_version=4)
                nbformat.validate(nb)
                for celula in nb.cells:
                    if celula.cell_type == "code":
                        self.assertFalse(any(o.output_type == "error" for o in celula.outputs))


if __name__ == "__main__":
    unittest.main()
