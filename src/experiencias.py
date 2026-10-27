"""Protocolo comum: treino e validação por utilizador; nunca seleciona no teste."""

import json
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import make_scorer, precision_score
from sklearn.model_selection import StratifiedGroupKFold, cross_validate

from src.avaliacao import calcular_metricas, pontuacoes
from src.dados import RAIZ, SEMENTE, SHA256, carregar_dados, dividir_dados
from src.preparacao import criar_pipeline, obter_alvo, selecionar_entradas

MODELOS = {
    "gradient_boosting": lambda: GradientBoostingClassifier(n_estimators=100, learning_rate=0.05, max_depth=2, random_state=SEMENTE),
    "svm": lambda: SVC(C=1.0, kernel="rbf", class_weight="balanced", random_state=SEMENTE),
    "naive_bayes": lambda: GaussianNB(priors=[0.5, 0.5]),
    "knn": lambda: KNeighborsClassifier(n_neighbors=15, weights="uniform", n_jobs=1),
    "random_forest": lambda: RandomForestClassifier(n_estimators=100, max_depth=8, min_samples_leaf=5, class_weight="balanced", random_state=SEMENTE, n_jobs=1),
    "arvore": lambda: DecisionTreeClassifier(max_depth=5, min_samples_leaf=20, class_weight="balanced", random_state=SEMENTE),
    "logistica": lambda: LogisticRegression(C=1.0, max_iter=2000, class_weight="balanced", random_state=SEMENTE),
    "maioritaria": lambda: DummyClassifier(strategy="most_frequent"),
    "sempre_suspeita": lambda: DummyClassifier(strategy="constant", constant=1),
}


def criar_cv():
    return StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=SEMENTE)


def executar_experiencia(nome):
    """Cada fold ajusta uma Pipeline completa apenas à sua parte de treino."""
    conjuntos = dividir_dados(carregar_dados())
    treino, validacao = conjuntos["treino"], conjuntos["validacao"]
    X, y = selecionar_entradas(treino), obter_alvo(treino)
    Xv, yv = selecionar_entradas(validacao), obter_alvo(validacao)
    pipeline = criar_pipeline(MODELOS[nome]())
    cv = cross_validate(
        pipeline, X, y, groups=treino["User_ID"], cv=criar_cv(),
        scoring={"f1": "f1", "average_precision": "average_precision", "roc_auc": "roc_auc",
                 "precision": make_scorer(precision_score, zero_division=0), "recall": "recall"},
        n_jobs=1, error_score="raise", return_train_score=True,
    )
    pipeline.fit(X, y)
    resumo_cv = {}
    for metrica in ["f1", "average_precision", "roc_auc", "precision", "recall"]:
        valores = cv["test_" + metrica]
        resumo_cv[metrica + "_media"] = float(np.mean(valores))
        resumo_cv[metrica + "_desvio"] = float(np.std(valores, ddof=1))
        resumo_cv[metrica + "_folds"] = valores.tolist()
    resumo_cv["f1_treino_media"] = float(np.mean(cv["train_f1"]))
    return {
        "modelo": nome, "sha256_dados": SHA256, "semente": SEMENTE,
        "cv": resumo_cv,
        "treino": calcular_metricas(y, pipeline.predict(X), pontuacoes(pipeline, X)),
        "validacao": calcular_metricas(yv, pipeline.predict(Xv), pontuacoes(pipeline, Xv)),
    }


def tabela_resultados(resultados):
    return pd.DataFrame([
        {"Modelo": r["modelo"], "F1 CV": r["cv"]["f1_media"], "Desvio F1 CV": r["cv"]["f1_desvio"],
         "F1 treino": r["treino"]["f1"], "F1 validação": r["validacao"]["f1"],
         "Precision": r["validacao"]["precision"], "Recall": r["validacao"]["recall"],
         "Accuracy": r["validacao"]["accuracy"], "ROC-AUC": r["validacao"]["roc_auc"],
         "Average Precision": r["validacao"]["average_precision"],
         "FP": r["validacao"]["fp"], "FN": r["validacao"]["fn"]}
        for r in resultados
    ]).set_index("Modelo")


def guardar_resultados(resultados):
    pasta = RAIZ / "resultados"
    pasta.mkdir(exist_ok=True)
    (pasta / "desenvolvimento.json").write_text(
        json.dumps(resultados, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8"
    )
