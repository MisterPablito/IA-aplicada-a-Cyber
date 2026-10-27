"""Pesquisa limitada e seleção antes da abertura do teste final."""

import json
from math import sqrt

import numpy as np
from sklearn.base import BaseEstimator, ClassifierMixin, clone
from sklearn.model_selection import GridSearchCV, ParameterGrid
from sklearn.utils.validation import check_is_fitted

from src.avaliacao import calcular_metricas, pontuacoes
from src.dados import RAIZ, SHA256, SEMENTE, carregar_dados, dividir_dados
from src.experiencias import MODELOS, criar_cv
from src.preparacao import criar_pipeline, obter_alvo, selecionar_entradas


class ClassificadorComLimiar(ClassifierMixin, BaseEstimator):
    """Inclui o limiar na pesquisa sem ajustar fora dos folds de treino."""

    def __init__(self, estimador, limiar=0.5):
        self.estimador = estimador
        self.limiar = limiar

    def fit(self, X, y):
        if not 0 <= self.limiar <= 1:
            raise ValueError("O limiar de probabilidade deve estar entre zero e um.")
        self.estimador_ = clone(self.estimador).fit(X, y)
        self.classes_ = self.estimador_.classes_
        self.n_features_in_ = X.shape[1]
        return self

    def predict_proba(self, X):
        check_is_fitted(self, "estimador_")
        return self.estimador_.predict_proba(X)

    def predict(self, X):
        posicao = list(self.classes_).index(1)
        return (self.predict_proba(X)[:, posicao] >= self.limiar).astype(int)


GRELHAS = {
    "logistica": {"estimador__modelo__C": [0.1, 1.0],
                  "estimador__modelo__class_weight": [None, "balanced"]},
    "arvore": {"estimador__modelo__max_depth": [1, 3, 5],
               "estimador__modelo__min_samples_leaf": [20, 100]},
    "naive_bayes": {"estimador__modelo__priors": [None, [0.5, 0.5]],
                    "estimador__modelo__var_smoothing": [1e-9, 1e-6]},
}
ORDEM_SIMPLICIDADE = {"maioritaria": 0, "sempre_suspeita": 0, "logistica": 1, "arvore": 2, "naive_bayes": 3}


def selecionar_simples(candidatos):
    """Heurística de um erro padrão, sem interpretação de significância."""
    melhor = max(candidatos, key=lambda c: (c["f1_cv"], c["ap_cv"]))
    limite = melhor["f1_cv"] - melhor["desvio_f1_cv"] / sqrt(5)
    elegiveis = [c for c in candidatos if c["f1_cv"] >= limite - 1e-12]
    escolhido = min(elegiveis, key=lambda c: (ORDEM_SIMPLICIDADE[c["familia"]], -c["f1_cv"], -c["ap_cv"]))
    return escolhido, limite


def construir_modelo(configuracao):
    familia = configuracao["familia"]
    pipeline = criar_pipeline(MODELOS[familia]())
    if configuracao.get("tipo") == "referencia":
        return pipeline
    return ClassificadorComLimiar(pipeline).set_params(**configuracao["parametros"])


def otimizar():
    """Só lê treino e validação; a decisão é persistida antes do teste."""
    conjuntos = dividir_dados(carregar_dados())
    treino, validacao = conjuntos["treino"], conjuntos["validacao"]
    X, y = selecionar_entradas(treino), obter_alvo(treino)
    Xv, yv = selecionar_entradas(validacao), obter_alvo(validacao)
    iniciais = json.loads((RAIZ / "resultados/desenvolvimento.json").read_text(encoding="utf-8"))
    if len(iniciais) != len(MODELOS) or any(r["sha256_dados"] != SHA256 for r in iniciais):
        raise ValueError("Executar a comparação completa antes da otimização.")
    candidatos = []
    for r in iniciais:
        if r["modelo"] in ["maioritaria", "sempre_suspeita"]:
            candidatos.append({
                "familia": r["modelo"], "tipo": "referencia", "parametros": {},
                "f1_cv": r["cv"]["f1_media"], "desvio_f1_cv": r["cv"]["f1_desvio"],
                "ap_cv": r["cv"]["average_precision_media"], "validacao": r["validacao"],
            })
    pesquisas = []
    for familia, parametros in GRELHAS.items():
        grelha = {**parametros, "limiar": [0.0, 0.2, 0.5]}
        base = ClassificadorComLimiar(criar_pipeline(MODELOS[familia]()))
        pesquisa = GridSearchCV(
            base, grelha, scoring={"f1": "f1", "ap": "average_precision"},
            refit=False, cv=criar_cv(), n_jobs=1, error_score="raise",
        )
        pesquisa.fit(X, y, groups=treino["User_ID"])
        cv = pesquisa.cv_results_
        melhor = max(range(len(cv["params"])), key=lambda i: (cv["mean_test_f1"][i], cv["mean_test_ap"][i], -i))
        config = {
            "familia": familia, "tipo": "aprendizagem", "parametros": cv["params"][melhor],
            "f1_cv": float(cv["mean_test_f1"][melhor]),
            "desvio_f1_cv": float(np.std([cv[f"split{k}_test_f1"][melhor] for k in range(5)], ddof=1)),
            "ap_cv": float(cv["mean_test_ap"][melhor]),
        }
        modelo = construir_modelo(config).fit(X, y)
        config["validacao"] = calcular_metricas(yv, modelo.predict(Xv), pontuacoes(modelo, Xv))
        candidatos.append(config)
        for i, params in enumerate(cv["params"]):
            pesquisas.append({"familia": familia, "parametros": params,
                              "f1_cv": float(cv["mean_test_f1"][i]), "ap_cv": float(cv["mean_test_ap"][i])})
        print(f"Pesquisa {familia}: {len(list(ParameterGrid(grelha)))} configurações × 5 folds.", flush=True)
    escolhido, limite = selecionar_simples(candidatos)
    aprendido = max((c for c in candidatos if c["tipo"] == "aprendizagem"), key=lambda c: (c["f1_cv"], c["ap_cv"]))
    decisao = {
        "versao_protocolo": 1, "sha256_dados": SHA256, "semente": SEMENTE,
        "regra": "F1 CV e heurística de um erro padrão; Average Precision secundária; simplicidade em soluções elegíveis",
        "limite_um_erro_padrao": limite, "selecionado": escolhido,
        "melhor_aprendizagem": aprendido, "candidatos": candidatos,
        "configuracoes_pesquisadas": len(pesquisas), "ajustes_cv": 5 * len(pesquisas),
        "teste_utilizado": False,
    }
    for nome, conteudo in [("otimizacao.json", pesquisas), ("decisao_modelo.json", decisao)]:
        (RAIZ / "resultados" / nome).write_text(
            json.dumps(conteudo, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8"
        )
    return decisao
