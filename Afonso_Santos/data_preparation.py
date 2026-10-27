"""
Data preparation — Cybersecurity Network Logs: Anomaly Detection
==================================================================

Projeto: deteção de tráfego de rede malicioso (dataset Kaggle, aatmaca).
Fase: Data Preparation (CRISP-ML), a seguir ao Data Understanding / EDA.

Decisões tomadas e porquê (explicado em português simples):

1. Valores em falta / duplicados
   Nenhum encontrado no EDA (25 000 linhas, 0 nulos, 0 duplicados).
   Não há limpeza a fazer aqui, mas o passo fica no código para o caso
   de o dataset mudar (ex. nova extração de logs reais).

2. Outliers (valores "fora do normal")
   NÃO são removidos. Fui verificar e descobri que, em Packet_Size_Bytes,
   Failed_Logins e Geo_Distance_km, entre 45% e 65% dos pontos "fora do
   normal" são precisamente ligações maliciosas — não são erro de
   medição, são o sinal que o modelo tem de aprender a reconhecer.
   Se os removesse, estava a tirar ao modelo a informação mais útil.

3. Encoding (transformar texto em números)
   `Protocol` (TCP/UDP/ICMP) é uma categoria sem ordem entre elas (não
   faz sentido dizer que TCP "é maior" que UDP). Por isso uso one-hot
   encoding: cria uma coluna nova para cada protocolo, com 0 ou 1.

4. Escala (pôr todos os números "do mesmo tamanho")
   Aplico o StandardScaler às 4 variáveis numéricas. Isto é importante
   para a regressão logística, que é sensível a números com escalas
   muito diferentes (ex. 0-10 vs 0-10000); para modelos de árvore não
   faz diferença, mas também não faz mal nenhum. O "ajuste" da escala
   é feito só com os dados de treino, para não "espreitar" o teste.

5. Desequilíbrio de classes (só ~5% das linhas são maliciosas)
   Não uso SMOTE nem outras técnicas para "inventar" exemplos novos: a
   separação entre as duas classes já é bastante clara (visto na EDA) e
   inventar dados numa fronteira que já está limpa só traria ruído.
   Em vez disso, uso class_weight="balanced" no treino do modelo (isso
   fica no outro script, model_comparison.py), que dá mais peso aos
   casos maliciosos sem inventar nenhuma linha nova.

6. Divisão treino / validação / teste
   70% / 15% / 15%, mantendo sempre a mesma proporção de maliciosos em
   cada parte (chama-se "estratificado"). Com 1247 casos maliciosos no
   total, isto dá cerca de 187 em cada um dos conjuntos de validação e
   teste — número suficiente para uma métrica estável. Uso sempre a
   mesma "semente" aleatória (random_state=42) para que, se eu correr
   o script outra vez, dê sempre a mesma divisão.

Como usar:
    python data_preparation.py
O que o script produz, dentro da pasta ./prepared/:
    train.csv, val.csv, test.csv   → os 3 conjuntos, já prontos para o modelo
    scaler_mean_std.json           → guarda a escala usada, para aplicar aos mesmos dados no futuro
"""

import json
import os

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# ---------------------------------------------------------------------------
# Configurações gerais do script (é mais fácil mudar tudo aqui do que andar
# à procura destes valores espalhados pelo código)
# ---------------------------------------------------------------------------

RAW_PATH = "cybersecurity_network_logs.csv"  # onde está o CSV original
OUT_DIR = "prepared"  # pasta onde vão ficar os ficheiros já preparados
NUM_COLS = ["Packet_Size_Bytes", "Connection_Duration_ms", "Failed_Logins", "Geo_Distance_km"]  # as 4 colunas de números
CAT_COL = "Protocol"  # a única coluna que é texto (categoria)
TARGET = "Is_Malicious"  # a coluna que queremos prever (0 = normal, 1 = malicioso)
RANDOM_STATE = 42  # "semente" fixa, para a divisão dos dados dar sempre igual


def load_raw(path: str = RAW_PATH) -> pd.DataFrame:
    """Lê o CSV original e confirma que não há valores em falta nem duplicados."""
    df = pd.read_csv(path)  # abre o ficheiro CSV e põe numa tabela (DataFrame)

    n_missing = df.isna().sum().sum()  # conta quantas células estão vazias em toda a tabela
    n_dupes = df.duplicated().sum()  # conta quantas linhas estão repetidas

    if n_missing or n_dupes:
        # isto só deve aparecer se o dataset mudar; no CSV original não há nada disto
        print(f"[aviso] {n_missing} valores em falta, {n_dupes} duplicados — "
              f"decisões de limpeza no docstring assumiam 0 de cada.")

    df = df.drop_duplicates()  # remove linhas repetidas, caso existam
    return df


def encode_and_split(df: pd.DataFrame):
    """Transforma a coluna de texto (Protocol) em números, e divide os dados em
    treino / validação / teste, mantendo sempre a mesma % de maliciosos em cada parte."""

    # pd.get_dummies cria uma coluna nova para cada protocolo (ex. Protocol_TCP,
    # Protocol_UDP, Protocol_ICMP), com 0 ou 1 — é o "one-hot encoding"
    X = pd.get_dummies(df.drop(columns=[TARGET]), columns=[CAT_COL], drop_first=False)
    y = df[TARGET]  # y é só a coluna que queremos prever, separada do resto (X)

    # Primeiro separamos 30% dos dados para ficarem de fora do treino (temp).
    # stratify=y garante que a percentagem de maliciosos é igual nos dois lados.
    X_train, X_temp, y_train, y_temp = train_test_split(
        X, y, test_size=0.30, stratify=y, random_state=RANDOM_STATE
    )
    # Depois dividimos esses 30% ao meio: metade fica para validação, metade para teste.
    # No final: 70% treino, 15% validação, 15% teste.
    X_val, X_test, y_val, y_test = train_test_split(
        X_temp, y_temp, test_size=0.50, stratify=y_temp, random_state=RANDOM_STATE
    )
    return (X_train, y_train), (X_val, y_val), (X_test, y_test)


def scale(X_train, X_val, X_test):
    """Põe as 4 variáveis numéricas todas na mesma escala (média 0, desvio padrão 1)."""
    scaler = StandardScaler()

    # fazemos uma cópia para não alterar por acidente as tabelas originais
    X_train = X_train.copy()
    X_val = X_val.copy()
    X_test = X_test.copy()

    # fit_transform: calcula a escala (média e desvio padrão) e já aplica — mas SÓ no treino
    X_train[NUM_COLS] = scaler.fit_transform(X_train[NUM_COLS])
    # transform (sem fit): aplica a MESMA escala calculada no treino, sem recalcular nada
    # isto é importante — se recalculássemos a escala no teste, estaríamos a "fazer batota"
    X_val[NUM_COLS] = scaler.transform(X_val[NUM_COLS])
    X_test[NUM_COLS] = scaler.transform(X_test[NUM_COLS])

    # guardamos a média e o desvio padrão usados, para podermos aplicar a mesma escala
    # a dados novos no futuro (ex. ligações que cheguem depois do projeto)
    stats = {"mean": dict(zip(NUM_COLS, scaler.mean_.tolist())),
             "std": dict(zip(NUM_COLS, scaler.scale_.tolist()))}
    return X_train, X_val, X_test, stats


def main():
    os.makedirs(OUT_DIR, exist_ok=True)  # cria a pasta "prepared" se ainda não existir
    df = load_raw()  # passo 1: ler e confirmar os dados

    # passo 2: transformar o texto em números e dividir em treino/validação/teste
    (X_train, y_train), (X_val, y_val), (X_test, y_test) = encode_and_split(df)
    # passo 3: pôr as variáveis numéricas na mesma escala
    X_train, X_val, X_test, scaler_stats = scale(X_train, X_val, X_test)

    # passo 4: guardar cada conjunto num ficheiro CSV separado, e mostrar um resumo no terminal
    for name, X, y in [("train", X_train, y_train), ("val", X_val, y_val), ("test", X_test, y_test)]:
        out = X.copy()
        out[TARGET] = y.values  # juntamos de novo a coluna alvo (Is_Malicious) antes de guardar
        out.to_csv(os.path.join(OUT_DIR, f"{name}.csv"), index=False)
        rate = y.mean() * 100  # percentagem de maliciosos neste conjunto
        print(f"{name:>5}: {len(out):>6} linhas, {int(y.sum()):>4} maliciosos ({rate:.2f}%)")

    # passo 5: guardar a escala usada (média/desvio padrão), para reaproveitar depois
    with open(os.path.join(OUT_DIR, "scaler_mean_std.json"), "w") as f:
        json.dump(scaler_stats, f, indent=2)

    print(f"\nFicheiros escritos em ./{OUT_DIR}/")


# isto só corre quando executamos o ficheiro diretamente (python data_preparation.py),
# não corre se outro script fizer "import data_preparation"
if __name__ == "__main__":
    main()
