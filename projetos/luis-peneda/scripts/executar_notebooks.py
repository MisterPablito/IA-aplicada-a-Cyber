"""Executa notebooks num kernel novo, usando o mesmo Python deste comando."""

import argparse
import json
import os
from pathlib import Path
import sys

RAIZ = Path(__file__).resolve().parents[1]
for variavel, pasta in {
    "JUPYTER_RUNTIME_DIR": "jupyter",
    "IPYTHONDIR": "ipython",
    "MPLCONFIGDIR": "matplotlib",
}.items():
    destino = RAIZ / ".venv" / "runtime" / pasta
    destino.mkdir(parents=True, exist_ok=True)
    os.environ.setdefault(variavel, str(destino))

import nbformat
from nbclient import NotebookClient
from jupyter_client import KernelManager


def executar(caminho):
    """Devolve o notebook executado; uma falha interrompe a validação."""
    caminho = Path(caminho).resolve()
    notebook = nbformat.read(caminho, as_version=4)
    nbformat.validate(notebook)
    gestor = KernelManager(kernel_name="python3")
    gestor.kernel_spec.argv = [
        sys.executable, "-m", "ipykernel_launcher", "-f", "{connection_file}"
    ]
    cliente = NotebookClient(
        notebook, km=gestor, timeout=1200, allow_errors=False,
        record_timing=False, resources={"metadata": {"path": str(caminho.parent)}},
    )
    cliente.execute(cleanup_kc=True)
    nbformat.validate(notebook)
    return notebook


def guardar(notebook, caminho):
    """Mantém a indentação do notebook original e evita gravações parciais."""
    caminho = Path(caminho)
    temporario = caminho.with_suffix(".ipynb.tmp")
    dados = json.loads(nbformat.writes(notebook))
    temporario.write_text(
        json.dumps(dados, ensure_ascii=False, indent=1) + "\n", encoding="utf-8"
    )
    temporario.replace(caminho)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("notebooks", nargs="+", type=Path)
    parser.add_argument("--gravar", action="store_true", help="Guardar saídas reais após sucesso.")
    args = parser.parse_args()
    for caminho in args.notebooks:
        resultado = executar(caminho)
        if args.gravar:
            guardar(resultado, caminho)
        print(f"VALIDADO: {caminho} — kernel novo, execução integral sem erros.")


if __name__ == "__main__":
    main()
