"""Preparacao inicial do dataset de ataques ciberneticos."""
import json
from pathlib import Path
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from joblib import dump
from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import HistGradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    ConfusionMatrixDisplay,
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    roc_auc_score,
    roc_curve,
    auc as area_under_curve,
)
from sklearn.model_selection import RandomizedSearchCV, StratifiedKFold, cross_validate, train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, StandardScaler, label_binarize
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
    label_encoder = LabelEncoder()
    labels = label_encoder.fit_transform(data[TARGET])
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
    selected_score = comparison[0]["macro_f1"]

    tree_pipeline = Pipeline([
        ("preprocessor", preprocessor),
        ("classifier", DecisionTreeClassifier(random_state=SEED)),
    ])
    search = RandomizedSearchCV(
        tree_pipeline,
        {
            "classifier__max_depth": [4, 6, 8, 12, 16, None],
            "classifier__min_samples_leaf": [1, 2, 5, 10, 20],
            "classifier__criterion": ["gini", "entropy", "log_loss"],
        },
        n_iter=12, scoring="f1_macro", cv=folds, random_state=SEED, n_jobs=1,
    )
    search.fit(train_features, train_labels)
    print("Melhor arvore ajustada (CV):", f"{search.best_score_:.4f}", search.best_params_)

    if search.best_score_ > selected_score:
        selected_model = "Arvore de decisao ajustada"
        selected_score = search.best_score_
    print("Modelo selecionado apenas com dados de treino:", selected_model)
    print("Macro-F1 CV selecionado:", f"{selected_score:.4f}")

    if selected_model == "Arvore de decisao ajustada":
        final_pipeline = search.best_estimator_
    else:
        final_pipeline = Pipeline([
            ("preprocessor", preprocessor),
            ("classifier", models[selected_model]),
        ])
    final_pipeline.fit(train_features, train_labels)
    train_predictions = final_pipeline.predict(train_features)
    test_predictions = final_pipeline.predict(test_features)
    train_f1 = f1_score(train_labels, train_predictions, average="macro")
    test_f1 = f1_score(test_labels, test_predictions, average="macro")
    test_accuracy = accuracy_score(test_labels, test_predictions)
    class_report = classification_report(
        test_labels, test_predictions,
        labels=range(len(label_encoder.classes_)),
        target_names=label_encoder.classes_.astype(str),
        output_dict=True,
    )
    print("\nAvaliacao no teste retido:")
    print(f"Accuracy={test_accuracy:.4f}; macro-F1={test_f1:.4f}; treino={train_f1:.4f}")
    print(classification_report(
        test_labels, test_predictions,
        labels=range(len(label_encoder.classes_)),
        target_names=label_encoder.classes_.astype(str),
        digits=4,
    ))

    prediction_scores = final_pipeline.predict_proba(test_features)
    test_auc = roc_auc_score(
        test_labels, prediction_scores, multi_class="ovr", average="macro",
        labels=range(len(label_encoder.classes_)),
    )
    output_dir = Path(__file__).resolve().parent / "resultados"
    graphics_dir = output_dir / "graficos"
    graphics_dir.mkdir(parents=True, exist_ok=True)
    dump(final_pipeline, output_dir / "modelo_final.joblib")

    matrix = confusion_matrix(test_labels, test_predictions)
    figure, axis = plt.subplots(figsize=(7, 6))
    ConfusionMatrixDisplay(matrix, display_labels=label_encoder.classes_).plot(
        ax=axis, cmap="Blues", values_format="d", colorbar=False,
    )
    figure.tight_layout()
    figure.savefig(graphics_dir / "matriz_confusao_teste.png", dpi=160)
    plt.close(figure)

    figure, axes = plt.subplots(1, 2, figsize=(15, 6))
    axes[0].bar(
        [result["model"] for result in comparison],
        [result["macro_f1"] for result in comparison],
        color="#3977a8",
    )
    axes[0].set_title("Macro-F1 na validacao cruzada")
    axes[0].tick_params(axis="x", rotation=55)
    binary_labels = label_binarize(test_labels, classes=np.arange(len(label_encoder.classes_)))
    for index, class_name in enumerate(label_encoder.classes_):
        false_positive_rate, true_positive_rate, _ = roc_curve(
            binary_labels[:, index], prediction_scores[:, index],
        )
        axes[1].plot(
            false_positive_rate, true_positive_rate,
            label=f"{class_name} (AUC={area_under_curve(false_positive_rate, true_positive_rate):.3f})",
        )
    axes[1].plot([0, 1], [0, 1], linestyle="--", color="grey")
    axes[1].legend(loc="lower right", fontsize=8)
    axes[1].set(title="ROC one-vs-rest no teste", xlabel="False Positive Rate", ylabel="True Positive Rate")
    figure.tight_layout()
    figure.savefig(graphics_dir / "comparacao_e_roc.png", dpi=160)
    plt.close(figure)

    summary = {
        "modelo_final": selected_model,
        "macro_f1_cv": float(selected_score),
        "accuracy_teste": float(test_accuracy),
        "macro_f1_teste": float(test_f1),
        "roc_auc_ovr_macro_teste": float(test_auc),
        "linhas_apos_deduplicacao": int(len(data)),
        "linhas_duplicadas_removidas": duplicate_count,
        "classes": label_encoder.classes_.tolist(),
        "cv_comparison": comparison,
        "per_class_metrics": {
            name: {
                metric: float(class_report[name][metric])
                for metric in ("precision", "recall", "f1-score", "support")
            }
            for name in label_encoder.classes_.astype(str)
        },
    }
    (output_dir / "resumo_resultados.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8",
    )
    print("ROC-AUC macro OvR:", f"{test_auc:.4f}")
    print("Modelo, resumo e graficos guardados em:", output_dir)


if __name__ == "__main__":
    main()