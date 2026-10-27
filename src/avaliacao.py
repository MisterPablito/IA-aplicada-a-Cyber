"""Métricas binárias com Suspicious=1 e contagens explícitas de erros."""

import numpy as np
from sklearn.metrics import (
    accuracy_score, average_precision_score, confusion_matrix,
    f1_score, precision_score, recall_score, roc_auc_score,
)


def pontuacoes(modelo, X):
    if hasattr(modelo, "predict_proba"):
        posicao = list(modelo.classes_).index(1)
        return modelo.predict_proba(X)[:, posicao]
    if hasattr(modelo, "decision_function"):
        return modelo.decision_function(X)
    raise ValueError("O modelo não fornece pontuações para ROC-AUC ou Average Precision.")


def calcular_metricas(y, previsoes, scores):
    y, previsoes, scores = np.asarray(y), np.asarray(previsoes), np.asarray(scores, dtype=float)
    if not (y.ndim == previsoes.ndim == scores.ndim == 1) or not (len(y) == len(previsoes) == len(scores)) or not len(y):
        raise ValueError("Alvo, previsões e pontuações devem ser vetores não vazios de igual dimensão.")
    if not set(np.unique(y)).issubset({0, 1}) or not set(np.unique(previsoes)).issubset({0, 1}):
        raise ValueError("A avaliação exige Normal=0 e Suspicious=1.")
    if not np.isfinite(scores).all():
        raise ValueError("As pontuações contêm valores inválidos.")
    tn, fp, fn, tp = confusion_matrix(y, previsoes, labels=[0, 1]).ravel()
    ambas = len(np.unique(y)) == 2
    return {
        "accuracy": float(accuracy_score(y, previsoes)),
        "precision": float(precision_score(y, previsoes, zero_division=0)),
        "recall": float(recall_score(y, previsoes, zero_division=0)),
        "f1": float(f1_score(y, previsoes, zero_division=0)),
        "roc_auc": float(roc_auc_score(y, scores)) if ambas else None,
        "average_precision": float(average_precision_score(y, scores)) if ambas else None,
        "tn": int(tn), "fp": int(fp), "fn": int(fn), "tp": int(tp),
        "registos": len(y), "sem_previsoes_positivas": bool(tp + fp == 0),
    }
