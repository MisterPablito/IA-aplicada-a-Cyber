"""
Model comparison — Cybersecurity Network Logs: Anomaly Detection
==================================================================

Projeto IAAC. Fase: Modeling.

Compara três candidatos no conjunto de VALIDAÇÃO (prepared/val.csv),
treinados em prepared/train.csv. O conjunto de teste (prepared/test.csv)
não é tocado aqui — fica reservado para a história de Avaliação Final
(Luís), para não usarmos o mesmo conjunto para escolher o modelo e para
reportar o número final.

Candidatos:
  1. Regressão logística   (class_weight="balanced", simples, explicável)
  2. Random Forest         (class_weight="balanced", não-linear)
  3. HistGradientBoosting  (class_weight="balanced", não-linear, o mesmo
                             tipo usado no baseline do EDA)

Métricas: PR-AUC (a mais informativa com 5% de positivos), ROC-AUC, e
recall ao limiar que dá precisão >= 0.5 / 0.8 / 0.9 — para já dar uma
ideia de trade-off, sem ainda fixar o limiar de produção (isso é a
história de Impact Simulation, que precisa dos custos de FN/FP).

Uso:
    python model_comparison.py
Lê prepared/train.csv e prepared/val.csv (gerados por data_preparation.py).
"""

import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    average_precision_score,
    precision_recall_curve,
    roc_auc_score,
)

TARGET = "Is_Malicious"
PRECISION_TARGETS = (0.5, 0.8, 0.9)


def load_splits():
    train = pd.read_csv("prepared/train.csv")
    val = pd.read_csv("prepared/val.csv")
    X_train, y_train = train.drop(columns=[TARGET]), train[TARGET]
    X_val, y_val = val.drop(columns=[TARGET]), val[TARGET]
    return X_train, y_train, X_val, y_val


def recall_at_precision(y_true, y_score, target):
    precision, recall, _ = precision_recall_curve(y_true, y_score)
    ok = precision[:-1] >= target
    return recall[:-1][ok].max() if ok.any() else float("nan")


def evaluate(name, model, X_train, y_train, X_val, y_val, results):
    model.fit(X_train, y_train)
    scores = model.predict_proba(X_val)[:, 1]
    row = {
        "modelo": name,
        "PR-AUC": average_precision_score(y_val, scores),
        "ROC-AUC": roc_auc_score(y_val, scores),
    }
    for t in PRECISION_TARGETS:
        row[f"recall@P>={t}"] = recall_at_precision(y_val, scores, t)
    results.append(row)
    return model


def main():
    X_train, y_train, X_val, y_val = load_splits()
    print(f"treino: {len(X_train)} linhas ({y_train.sum()} maliciosos)")
    print(f"validação: {len(X_val)} linhas ({y_val.sum()} maliciosos)\n")

    results = []
    evaluate(
        "Regressão logística",
        LogisticRegression(max_iter=2000, class_weight="balanced"),
        X_train, y_train, X_val, y_val, results,
    )
    evaluate(
        "Random Forest",
        RandomForestClassifier(n_estimators=300, class_weight="balanced", random_state=42, n_jobs=-1),
        X_train, y_train, X_val, y_val, results,
    )
    evaluate(
        "HistGradientBoosting",
        HistGradientBoostingClassifier(class_weight="balanced", random_state=42),
        X_train, y_train, X_val, y_val, results,
    )

    df = pd.DataFrame(results).set_index("modelo").round(3)
    print(df.to_string())
    df.to_csv("prepared/model_comparison_val.csv")
    print("\nResultados guardados em prepared/model_comparison_val.csv")


if __name__ == "__main__":
    main()
