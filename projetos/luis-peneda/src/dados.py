"""Leitura do CSV preservado e divisão reproduzível por utilizador."""

from hashlib import sha256
from pathlib import Path

import pandas as pd
from sklearn.model_selection import GroupShuffleSplit

RAIZ = Path(__file__).resolve().parents[1]
CSV = RAIZ / "data" / "raw" / "cybercrime_forensic_dataset.csv"
SHA256 = "6f7355d0a563822cd1c8995a2b9a0bb1f9a249b7ee388a4db25c787e5c5c0264"
SEMENTE = 42
COLUNAS = [
    "Timestamp", "User_ID", "IP_Address", "Activity_Type", "Resource_Accessed",
    "File_Name", "Action", "Login_Attempts", "File_Size", "Anomaly_Type", "Label",
]


def validar_dados(df):
    """Recusa esquemas, rótulos ou identificadores incompatíveis."""
    if list(df.columns) != COLUNAS:
        raise ValueError("O esquema do dataset difere das 11 colunas esperadas.")
    if set(df["Label"].unique()) != {"Normal", "Suspicious"}:
        raise ValueError("O dataset deve conter apenas as duas classes esperadas.")
    if df["User_ID"].isna().any() or not df.index.is_unique:
        raise ValueError("Utilizadores ausentes ou índices repetidos impedem uma divisão segura.")
    if df.duplicated().any():
        raise ValueError("Foram detetados registos integralmente duplicados.")
    pd.to_datetime(df["Timestamp"], errors="raise")


def carregar_dados():
    """Carrega a versão identificada, sem confundir categorias com ausências."""
    if sha256(CSV.read_bytes()).hexdigest() != SHA256:
        raise ValueError("O CSV original foi alterado; rever a versão antes de reproduzir experiências.")
    df = pd.read_csv(CSV, keep_default_na=False, na_values=[""])
    validar_dados(df)
    return df


def dividir_dados(df):
    """Reserva 20% dos utilizadores para teste e 20% para validação."""
    validar_dados(df)
    divisor = GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=SEMENTE)
    desenvolvimento, teste = next(divisor.split(df, groups=df["User_ID"]))
    dev = df.iloc[desenvolvimento]
    divisor_validacao = GroupShuffleSplit(n_splits=1, test_size=0.25, random_state=SEMENTE)
    treino, validacao = next(divisor_validacao.split(dev, groups=dev["User_ID"]))
    conjuntos = {
        "treino": dev.iloc[treino].copy(),
        "validacao": dev.iloc[validacao].copy(),
        "teste": df.iloc[teste].copy(),
    }
    for nome, parte in conjuntos.items():
        if set(parte["Label"].unique()) != {"Normal", "Suspicious"}:
            raise ValueError(f"O conjunto {nome} não contém ambas as classes; rever o protocolo.")
    for a, b in [("treino", "validacao"), ("treino", "teste"), ("validacao", "teste")]:
        if set(conjuntos[a]["User_ID"]) & set(conjuntos[b]["User_ID"]):
            raise AssertionError("Existe sobreposição de utilizadores entre conjuntos.")
        if set(conjuntos[a].index) & set(conjuntos[b].index):
            raise AssertionError("Existe sobreposição de linhas entre conjuntos.")
    return conjuntos


def resumo_divisao(conjuntos):
    """Descreve a divisão sem experimentar modelos no teste."""
    return pd.DataFrame([
        {"Conjunto": nome, "Registos": len(df), "Utilizadores": df["User_ID"].nunique(),
         "Normal": int((df["Label"] == "Normal").sum()),
         "Suspicious": int((df["Label"] == "Suspicious").sum()),
         "% Suspicious": round(100 * (df["Label"] == "Suspicious").mean(), 2)}
        for nome, df in conjuntos.items()
    ]).set_index("Conjunto")
