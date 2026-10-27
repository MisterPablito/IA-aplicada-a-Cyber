"""Demonstração académica de treino local e previsões batch reproduzíveis."""

import argparse
import importlib.metadata
from pathlib import Path

import joblib
import numpy as np
import pandas as pd

from src.avaliacao import pontuacoes
from src.avaliacao_final import ASSINATURA_DECISAO, carregar_decisao
from src.dados import CSV, RAIZ, SHA256, carregar_dados, dividir_dados
from src.otimizacao import construir_modelo
from src.preparacao import ENTRADAS, PROIBIDAS, obter_alvo, selecionar_entradas

MODELO_LOCAL = RAIZ / "artefactos" / "modelo_final.joblib"


def treinar_artefacto(destino=MODELO_LOCAL):
    """Reconstitui a decisão fixada usando apenas o desenvolvimento."""
    destino = Path(destino)
    if destino.resolve() == CSV.resolve() or destino.suffix != ".joblib":
        raise ValueError("O artefacto deve ser um ficheiro .joblib distinto dos dados originais.")
    decisao = carregar_decisao()
    partes = dividir_dados(carregar_dados())
    desenvolvimento = pd.concat([partes["treino"], partes["validacao"]])
    modelo = construir_modelo(decisao["selecionado"]).fit(
        selecionar_entradas(desenvolvimento), obter_alvo(desenvolvimento)
    )
    artefacto = {
        "modelo": modelo, "familia": decisao["selecionado"]["familia"],
        "assinatura_decisao": ASSINATURA_DECISAO, "sha256_dados": SHA256,
        "entradas": list(ENTRADAS), "classe_positiva": "Suspicious",
        "versao_sklearn": importlib.metadata.version("scikit-learn"),
        "uso_operacional_recomendado": False,
    }
    destino.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(artefacto, destino, compress=3)
    return artefacto


def carregar_artefacto(caminho=MODELO_LOCAL):
    """Carrega o artefacto local produzido pelo comando de treino."""
    artefacto = joblib.load(caminho)
    if artefacto.get("assinatura_decisao") != ASSINATURA_DECISAO or artefacto.get("sha256_dados") != SHA256:
        raise ValueError("O artefacto não corresponde à decisão e dados fixados.")
    if artefacto.get("versao_sklearn") != importlib.metadata.version("scikit-learn"):
        raise ValueError("A versão de scikit-learn difere; recriar o artefacto no ambiente documentado.")
    return artefacto


def prever_batch(df, artefacto):
    if PROIBIDAS & set(df.columns):
        raise ValueError("O ficheiro de previsão contém campos que revelam o alvo.")
    if set(df.columns) != set(ENTRADAS) or df.empty:
        raise ValueError(f"Fornecer pelo menos um registo e apenas os campos {list(ENTRADAS)}.")
    X = selecionar_entradas(df)
    modelo = artefacto["modelo"]
    previsoes, scores = modelo.predict(X), pontuacoes(modelo, X)
    if not set(np.unique(previsoes)).issubset({0, 1}) or not np.isfinite(scores).all():
        raise ValueError("O modelo produziu uma saída inválida.")
    return pd.DataFrame({
        "Registo": np.arange(1, len(df) + 1),
        "Previsao": np.where(previsoes == 1, "Suspicious", "Normal"),
        "PontuacaoSuspicious": scores,
    }, index=df.index)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    comandos = parser.add_subparsers(dest="comando", required=True)
    treino = comandos.add_parser("treinar", help="Recriar o artefacto local da decisão fixada.")
    treino.add_argument("--modelo", type=Path, default=MODELO_LOCAL)
    previsao = comandos.add_parser("prever", help="Classificar registos compatíveis de um CSV.")
    previsao.add_argument("entrada", type=Path)
    previsao.add_argument("--modelo", type=Path, default=MODELO_LOCAL)
    previsao.add_argument("--saida", type=Path, default=RAIZ / "artefactos/previsoes.csv")
    args = parser.parse_args()
    if args.comando == "treinar":
        artefacto = treinar_artefacto(args.modelo)
        print(f"Artefacto local criado: {args.modelo}. Família: {artefacto['familia']}.")
    else:
        if args.saida.resolve() in {args.entrada.resolve(), CSV.resolve()}:
            parser.error("A saída não pode substituir o ficheiro de entrada nem o CSV original.")
        entradas = pd.read_csv(args.entrada, keep_default_na=False, na_values=[""])
        saidas = prever_batch(entradas, carregar_artefacto(args.modelo))
        args.saida.parent.mkdir(parents=True, exist_ok=True)
        saidas.to_csv(args.saida, index=False, encoding="utf-8")
        print(saidas.to_string(index=False))
        print(f"Previsões guardadas: {args.saida}.")
    print("Demonstração académica: a regra selecionada sinaliza tudo e não é recomendada para utilização operacional.")


if __name__ == "__main__":
    main()
