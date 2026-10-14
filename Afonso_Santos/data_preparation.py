"""
Data preparation — Cybersecurity Network Logs: Anomaly Detection
==================================================================

Projeto: deteção de tráfego de rede malicioso (dataset Kaggle, aatmaca).
Fase: Data Preparation (CRISP-ML), a seguir ao Data Understanding / EDA.

Decisões tomadas e porquê:

1. Valores em falta / duplicados
   Nenhum encontrado no EDA (25 000 linhas, 0 nulos, 0 duplicados).
   Não há limpeza a fazer aqui, mas o passo fica no pipeline para o caso
   de o dataset mudar (ex. nova extração de logs reais).

2. Outliers
   NÃO são removidos. Verificação: em Packet_Size_Bytes, Failed_Logins e
   Geo_Distance_km, entre 45% e 65% dos pontos fora do intervalo IQR são
   precisamente ligações maliciosas — não são erro de medição, são o
   sinal que o modelo tem de aprender a reconhecer. Remover isto
   destruiria o problema.

3. Encoding
   `Protocol` (TCP/UDP/ICMP) é nominal, sem ordem. One-hot encoding,
   sem remover a primeira categoria (drop_first=False), porque com
   modelos de árvore (HistGradientBoosting) isso não custa nada e
   evita perder informação se um dia se usar um modelo linear
   regularizado. Guarda-se a lista de colunas geradas para aplicar a
   mesma transformação em dados novos.

4. Escala
   Aplicado StandardScaler às 4 variáveis numéricas. Necessário para
   regressão logística (sensível à escala); inofensivo para modelos
   de árvore. O scaler é ajustado SÓ no treino, para não vazar
   informação do teste.

5. Desequilíbrio de classes (≈5% positivos)
   Não se faz over/undersampling (ex. SMOTE) para já: a separação já é
   forte (ver EDA) e sintetizar exemplos numa fronteira que já é limpa
   arrisca introduzir ruído artificial. Em vez disso: manter a
   proporção original nos splits (stratify) e usar class_weight="balanced"
   como opção no treino do modelo, ajustando o limiar de decisão a
   partir da curva precisão-recall (não usar 0.5 por defeito).

6. Divisão treino / validação / teste
   70% / 15% / 15%, estratificada pela classe. Com 1247 positivos no
   total, isto dá ~187 positivos em cada um de validação e teste —
   acima do mínimo de 30 eventos referido no canvas para uma métrica
   estável. Split fixo com random_state=42 para reprodutibilidade.

Uso:
    python data_preparation.py
Produz, em ./prepared/:
    train.csv, val.csv, test.csv   (com as features já codificadas e escaladas)
    scaler_mean_std.json           (para aplicar a mesma escala em dados novos)
"""

import json
import os

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

RAW_PATH = r"C:\Users\Afonso Santos\Documents\IAAC\IA-aplicada-a-Cyber\Afonso_Santos\cybersecurity_network_logs.csv"
OUT_DIR = "prepared"
NUM_COLS = ["Packet_Size_Bytes", "Connection_Duration_ms", "Failed_Logins", "Geo_Distance_km"]
CAT_COL = "Protocol"
TARGET = "Is_Malicious"
RANDOM_STATE = 42


def load_raw(path: str = RAW_PATH) -> pd.DataFrame:
    df = pd.read_csv(path)
    n_missing = df.isna().sum().sum()
    n_dupes = df.duplicated().sum()
    if n_missing or n_dupes:
        print(f"[aviso] {n_missing} valores em falta, {n_dupes} duplicados — "
              f"decisões de limpeza no docstring assumiam 0 de cada.")
    df = df.drop_duplicates()
    return df


def encode_and_split(df: pd.DataFrame):
    X = pd.get_dummies(df.drop(columns=[TARGET]), columns=[CAT_COL], drop_first=False)
    y = df[TARGET]

    # 70/15/15 estratificado: primeiro separa o teste, depois treino/validação
    X_train, X_temp, y_train, y_temp = train_test_split(
        X, y, test_size=0.30, stratify=y, random_state=RANDOM_STATE
    )
    X_val, X_test, y_val, y_test = train_test_split(
        X_temp, y_temp, test_size=0.50, stratify=y_temp, random_state=RANDOM_STATE
    )
    return (X_train, y_train), (X_val, y_val), (X_test, y_test)


def scale(X_train, X_val, X_test):
    scaler = StandardScaler()
    X_train = X_train.copy()
    X_val = X_val.copy()
    X_test = X_test.copy()
    X_train[NUM_COLS] = scaler.fit_transform(X_train[NUM_COLS])
    X_val[NUM_COLS] = scaler.transform(X_val[NUM_COLS])
    X_test[NUM_COLS] = scaler.transform(X_test[NUM_COLS])
    stats = {"mean": dict(zip(NUM_COLS, scaler.mean_.tolist())),
             "std": dict(zip(NUM_COLS, scaler.scale_.tolist()))}
    return X_train, X_val, X_test, stats


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    df = load_raw()

    (X_train, y_train), (X_val, y_val), (X_test, y_test) = encode_and_split(df)
    X_train, X_val, X_test, scaler_stats = scale(X_train, X_val, X_test)

    for name, X, y in [("train", X_train, y_train), ("val", X_val, y_val), ("test", X_test, y_test)]:
        out = X.copy()
        out[TARGET] = y.values
        out.to_csv(os.path.join(OUT_DIR, f"{name}.csv"), index=False)
        rate = y.mean() * 100
        print(f"{name:>5}: {len(out):>6} linhas, {int(y.sum()):>4} maliciosos ({rate:.2f}%)")

    with open(os.path.join(OUT_DIR, "scaler_mean_std.json"), "w") as f:
        json.dump(scaler_stats, f, indent=2)

    print(f"\nFicheiros escritos em ./{OUT_DIR}/")


if __name__ == "__main__":
    main()
