"""Preparacao inicial do dataset de ataques ciberneticos."""
from pathlib import Path
import sys

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler

TARGET = "attack_type"
SEED = 42


def load_data():
    project_dir = Path(__file__).resolve().parent
    csv_path = Path(sys.argv[1]) if len(sys.argv) > 1 else project_dir / "data" / "cyber_attack_dataset_100000.csv"
    if not csv_path.is_file():
        raise FileNotFoundError(f"Dataset nao encontrado: {csv_path}")
    return pd.read_csv(csv_path)


def main():
    data = load_data()
    print("Dimensao original:", data.shape)
    print("Valores nulos por coluna:\n", data.isna().sum())
    print("Distribuicao das classes:\n", data[TARGET].value_counts(normalize=True).round(4))

    duplicate_count = int(data.duplicated().sum())
    data = data.drop_duplicates().reset_index(drop=True)
    print("Duplicados removidos:", duplicate_count)

    features = data.drop(columns=TARGET)
    labels = data[TARGET]
    numeric_columns = features.select_dtypes(include="number").columns.tolist()
    categorical_columns = features.select_dtypes(exclude="number").columns.tolist()
    encoder = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
    preprocessor = ColumnTransformer([
        ("numeric", StandardScaler(), numeric_columns),
        ("categorical", encoder, categorical_columns),
    ])
    train_features, test_features, train_labels, test_labels = train_test_split(
        features, labels, test_size=0.20, random_state=SEED, stratify=labels
    )
    print("Treino/teste:", train_features.shape, test_features.shape)
    print("Pre-processador configurado:", preprocessor)
    print("Classes no treino:", train_labels.nunique(), "; no teste:", test_labels.nunique())


if __name__ == "__main__":
    main()