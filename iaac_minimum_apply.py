"""Preparacao inicial do dataset de ataques ciberneticos."""
from pathlib import Path
import sys

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import HistGradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import StratifiedKFold, cross_validate, train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, StandardScaler
from sklearn.svm import LinearSVC
from sklearn.tree import DecisionTreeClassifier

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
    labels = LabelEncoder().fit_transform(data[TARGET])
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
    print("Classes no treino:", len(set(train_labels)), "; no teste:", len(set(test_labels)))

    models = {
        "Baseline": DummyClassifier(strategy="most_frequent"),
        "Regressao logistica": LogisticRegression(max_iter=1000),
        "Arvore de decisao": DecisionTreeClassifier(random_state=SEED),
        "k-NN": KNeighborsClassifier(n_neighbors=5),
        "Gaussian Naive Bayes": GaussianNB(),
        "SVM linear": LinearSVC(random_state=SEED, max_iter=5000),
        "Random Forest": RandomForestClassifier(n_estimators=120, random_state=SEED, n_jobs=-1),
    }
    try:
        from xgboost import XGBClassifier

        models["XGBoost"] = XGBClassifier(
            n_estimators=120, max_depth=6, learning_rate=0.1,
            eval_metric="mlogloss", random_state=SEED, n_jobs=-1,
        )
    except ImportError:
        models["Gradient Boosting (Hist)"] = HistGradientBoostingClassifier(random_state=SEED)

    folds = StratifiedKFold(n_splits=3, shuffle=True, random_state=SEED)
    comparison = []
    for model_name, model in models.items():
        pipeline = Pipeline([("preprocessor", preprocessor), ("classifier", model)])
        scores = cross_validate(
            pipeline, train_features, train_labels, cv=folds,
            scoring={"macro_f1": "f1_macro", "accuracy": "accuracy"}, n_jobs=1,
        )
        comparison.append({
            "model": model_name,
            "macro_f1": scores["test_macro_f1"].mean(),
            "accuracy": scores["test_accuracy"].mean(),
        })

    comparison.sort(key=lambda result: result["macro_f1"], reverse=True)
    print("\nComparacao por validacao cruzada no treino:")
    for result in comparison:
        print(
            f"{result['model']}: macro-F1={result['macro_f1']:.4f}; "
            f"accuracy={result['accuracy']:.4f}"
        )
    selected_model = comparison[0]["model"]
    print("Candidato selecionado para avaliacao posterior:", selected_model)


if __name__ == "__main__":
    main()