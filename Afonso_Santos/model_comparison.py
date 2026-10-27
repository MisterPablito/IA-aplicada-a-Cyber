"""
Model comparison — Cybersecurity Network Logs: Anomaly Detection
==================================================================

Projeto IAAC. Fase: Modeling.

O que este script faz, em palavras simples: treina 3 "robôs" (modelos)
diferentes com os dados de treino, e depois testa os três no conjunto de
VALIDAÇÃO (prepared/val.csv), para ver qual deles acerta mais.

Importante: o conjunto de TESTE (prepared/test.csv) não é tocado aqui de
propósito. Fica guardado para mais tarde, para a avaliação final — se
usássemos o teste agora para escolher o modelo, estaríamos a "ver a
resposta" antes do exame a sério.

Os três modelos testados:
  1. Regressão logística   → o mais simples e mais fácil de explicar
  2. Random Forest         → várias "árvores de decisão" a votar
  3. HistGradientBoosting  → outro tipo de árvores, mais sofisticado

Os três usam class_weight="balanced", que diz ao modelo para dar mais
atenção aos casos maliciosos (só ~5% dos dados), já que não estamos a
inventar dados novos (ver decisão 5 em data_preparation.py).

Métricas usadas (porque "accuracy" sozinha engana com dados tão
desequilibrados — um modelo que dissesse sempre "normal" já acertava 95%):
  - PR-AUC: a métrica mais informativa aqui, porque olha só para o
    quão bem o modelo encontra os poucos casos maliciosos.
  - ROC-AUC: outra métrica parecida, mais comum na literatura.
  - recall a vários níveis de precisão: "se só quisermos poucos alarmes
    falsos (precisão alta), quantos ataques é que ainda conseguimos
    apanhar (recall)?" — isto ainda não fixa o limiar final, que depende
    dos custos de cada erro (isso é outra história, a da Impact
    Simulation).

Como usar:
    python model_comparison.py
Precisa que prepared/train.csv e prepared/val.csv já existam — ou seja,
correr primeiro o data_preparation.py.
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
PRECISION_TARGETS = (0.5, 0.8, 0.9)  # níveis de precisão que queremos testar


def load_splits():
    """Lê os ficheiros já preparados (treino e validação) e separa cada um
    em X (as variáveis que o modelo usa) e y (o que queremos prever)."""
    train = pd.read_csv("prepared/train.csv")
    val = pd.read_csv("prepared/val.csv")
    X_train, y_train = train.drop(columns=[TARGET]), train[TARGET]
    X_val, y_val = val.drop(columns=[TARGET]), val[TARGET]
    return X_train, y_train, X_val, y_val


def recall_at_precision(y_true, y_score, target):
    """Pergunta: 'se eu exigir pelo menos esta precisão, quantos casos
    maliciosos (recall) ainda consigo apanhar?' — devolve esse recall."""
    precision, recall, _ = precision_recall_curve(y_true, y_score)
    # a curva tem sempre um ponto a mais no fim (threshold=infinito); por
    # isso ignoramos o último valor com [:-1], que não corresponde a um
    # limiar real
    ok = precision[:-1] >= target
    return recall[:-1][ok].max() if ok.any() else float("nan")


def evaluate(name, model, X_train, y_train, X_val, y_val, results):
    """Treina um modelo com os dados de treino, testa-o na validação,
    e guarda os resultados numa lista para depois comparar todos juntos."""
    model.fit(X_train, y_train)  # aqui é onde o modelo "aprende"
    scores = model.predict_proba(X_val)[:, 1]  # probabilidade de cada ligação ser maliciosa (0 a 1)

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

    results = []  # aqui vão ficar os resultados dos 3 modelos, para comparar no fim

    # modelo 1: regressão logística — o mais simples dos três
    evaluate(
        "Regressão logística",
        LogisticRegression(max_iter=2000, class_weight="balanced"),
        X_train, y_train, X_val, y_val, results,
    )
    # modelo 2: random forest — várias árvores de decisão diferentes, a "votar"
    evaluate(
        "Random Forest",
        RandomForestClassifier(n_estimators=300, class_weight="balanced", random_state=42, n_jobs=-1),
        X_train, y_train, X_val, y_val, results,
    )
    # modelo 3: gradient boosting — árvores que vão corrigindo os erros umas das outras
    evaluate(
        "HistGradientBoosting",
        HistGradientBoostingClassifier(class_weight="balanced", random_state=42),
        X_train, y_train, X_val, y_val, results,
    )

    # juntar tudo numa tabela só, arredondar para 3 casas decimais e mostrar no terminal
    df = pd.DataFrame(results).set_index("modelo").round(3)
    print(df.to_string())

    # guardar também num CSV, para usar no relatório sem ter de copiar à mão
    df.to_csv("prepared/model_comparison_val.csv")
    print("\nResultados guardados em prepared/model_comparison_val.csv")


# só corre a função main() se o ficheiro for executado diretamente
if __name__ == "__main__":
    main()
