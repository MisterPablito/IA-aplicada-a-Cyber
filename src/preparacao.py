"""Características explícitas e transformações ajustadas apenas ao treino."""

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.utils.validation import check_is_fitted

PROIBIDAS = frozenset({"Label", "Label_bin", "Anomaly_Type"})
ENTRADAS = ("Timestamp", "Activity_Type", "Resource_Accessed", "Action", "Login_Attempts", "File_Size")
NUMERICAS = ("Login_Attempts", "File_Size", "Hora_sin", "Hora_cos", "Semana_sin", "Semana_cos")
CATEGORICAS = ("Activity_Type", "Resource_Accessed", "Action")
ATIVIDADES = frozenset({"Login", "Remote_Login", "File_Access", "File_Deletion", "File_Modification", "Network_Traffic", "USB_Insert"})


def selecionar_entradas(df):
    """Usa uma lista permitida, mesmo quando o dataset contém o alvo."""
    faltam = set(ENTRADAS) - set(df.columns)
    if faltam:
        raise ValueError(f"Faltam campos de entrada: {sorted(faltam)}")
    entradas = df.loc[:, list(ENTRADAS)].copy()
    if PROIBIDAS & set(entradas.columns):
        raise AssertionError("Uma coluna proibida foi incluída nas entradas.")
    return entradas


def obter_alvo(df):
    if not set(df["Label"].unique()).issubset({"Normal", "Suspicious"}):
        raise ValueError("Rótulo desconhecido no alvo.")
    return (df["Label"] == "Suspicious").astype(int)


class PrepararCaracteristicas(TransformerMixin, BaseEstimator):
    """Extrai contexto temporal sem aprender estatísticas da população."""

    def fit(self, X, y=None):
        self._extrair(X)
        self.feature_names_in_ = np.array(ENTRADAS, dtype=object)
        self.n_features_in_ = len(ENTRADAS)
        return self

    def transform(self, X):
        check_is_fitted(self, "feature_names_in_")
        return self._extrair(X)

    def get_feature_names_out(self, input_features=None):
        return np.array(NUMERICAS + CATEGORICAS, dtype=object)

    @staticmethod
    def _extrair(X):
        if not isinstance(X, pd.DataFrame):
            raise ValueError("As entradas devem ser um DataFrame com nomes de colunas.")
        if PROIBIDAS & set(X.columns):
            raise ValueError("As entradas contêm colunas que revelam o alvo.")
        df = selecionar_entradas(X)
        if not set(df["Activity_Type"].dropna()).issubset(ATIVIDADES) or df["Activity_Type"].isna().any():
            raise ValueError("Tipo de atividade desconhecido; não é possível interpretar as ausências.")
        tempo = pd.to_datetime(df.pop("Timestamp"), errors="raise")
        if tempo.isna().any():
            raise ValueError("Timestamp ausente.")
        for coluna, atividades in {
            "Login_Attempts": {"Login", "Remote_Login"},
            "File_Size": {"File_Access", "File_Deletion", "File_Modification"},
        }.items():
            valores = pd.to_numeric(df[coluna].replace("", np.nan), errors="raise")
            aplicavel = df["Activity_Type"].isin(atividades)
            if valores[aplicavel].isna().any():
                raise ValueError(f"{coluna} desconhecido numa atividade aplicável; completar o registo.")
            if valores[~aplicavel].notna().any():
                raise ValueError(f"{coluna} preenchido numa atividade não aplicável.")
            if (valores.dropna() < 0).any() or not np.isfinite(valores.dropna().to_numpy(dtype=float)).all():
                raise ValueError(f"Valor numérico inválido em {coluna}.")
            df[coluna] = valores.fillna(0.0)
        for prefixo, valores, periodo in [("Hora", tempo.dt.hour, 24), ("Semana", tempo.dt.day_of_week, 7)]:
            df[prefixo + "_sin"] = np.sin(2 * np.pi * valores / periodo)
            df[prefixo + "_cos"] = np.cos(2 * np.pi * valores / periodo)
        for coluna in CATEGORICAS:
            df[coluna] = df[coluna].astype(object).replace("", np.nan)
            df[coluna] = df[coluna].where(pd.notna(df[coluna]), np.nan)
        return df.loc[:, list(NUMERICAS + CATEGORICAS)]


def criar_preparacao():
    """As estatísticas de escala e as categorias são aprendidas em fit."""
    numericas = Pipeline([
        ("imputar", SimpleImputer(strategy="constant", fill_value=0.0)),
        ("escalar", StandardScaler()),
    ])
    categoricas = Pipeline([
        ("imputar", SimpleImputer(strategy="constant", fill_value="Unknown")),
        ("codificar", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
    ])
    return Pipeline([
        ("caracteristicas", PrepararCaracteristicas()),
        ("colunas", ColumnTransformer([
            ("numericas", numericas, list(NUMERICAS)),
            ("categoricas", categoricas, list(CATEGORICAS)),
        ], remainder="drop")),
    ])


def criar_pipeline(modelo):
    return Pipeline([("preparacao", criar_preparacao()), ("modelo", modelo)])
