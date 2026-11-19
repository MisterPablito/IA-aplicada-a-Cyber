"""Avalia a decisão congelada; não pesquisa nem seleciona no teste."""

import hashlib
import json

import pandas as pd

from src.avaliacao import calcular_metricas, pontuacoes
from src.dados import RAIZ, SHA256, carregar_dados, dividir_dados
from src.otimizacao import construir_modelo
from src.preparacao import obter_alvo, selecionar_entradas

COMMIT_DECISAO = "c6f6558ec207a15b0c7288666aeb89a937f69b2b"
ASSINATURA_DECISAO = "b2efea375b6887918f044fbfccb69e01f2e5bf098d0264913ccae148fd90cb36"


def assinatura_decisao(decisao):
    canonico = json.dumps(decisao, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False)
    return hashlib.sha256(canonico.encode("ascii")).hexdigest()


def carregar_decisao():
    decisao = json.loads((RAIZ / "resultados/decisao_modelo.json").read_text(encoding="utf-8"))
    if assinatura_decisao(decisao) != ASSINATURA_DECISAO:
        raise ValueError("A decisão congelada foi alterada. Não reutilizar o teste para selecionar outro modelo.")
    if decisao["sha256_dados"] != SHA256 or decisao["teste_utilizado"]:
        raise ValueError("A decisão não corresponde ao protocolo anterior ao teste.")
    return decisao


def avaliar_final():
    """Reajusta configurações fixadas no desenvolvimento completo e abre o teste."""
    decisao = carregar_decisao()
    partes = dividir_dados(carregar_dados())
    desenvolvimento = pd.concat([partes["treino"], partes["validacao"]])
    teste = partes["teste"]
    if set(desenvolvimento.User_ID) & set(teste.User_ID):
        raise AssertionError("Existe sobreposição de utilizadores com o teste.")
    X, y = selecionar_entradas(desenvolvimento), obter_alvo(desenvolvimento)
    Xt, yt = selecionar_entradas(teste), obter_alvo(teste)
    configuracoes = {
        "maioritaria": {"familia": "maioritaria", "tipo": "referencia"},
        "sempre_suspeita": {"familia": "sempre_suspeita", "tipo": "referencia"},
        decisao["melhor_aprendizagem"]["familia"] + "_otimizada": decisao["melhor_aprendizagem"],
    }
    metricas, detalhes = {}, {}
    for nome, config in configuracoes.items():
        modelo = construir_modelo(config).fit(X, y)
        previsoes, scores = modelo.predict(Xt), pontuacoes(modelo, Xt)
        metricas[nome] = calcular_metricas(yt, previsoes, scores)
        detalhes[nome] = {"alvo": yt.to_numpy(), "previsoes": previsoes, "pontuacoes": scores}
    resultado = {
        "commit_decisao": COMMIT_DECISAO, "assinatura_decisao": ASSINATURA_DECISAO,
        "sha256_dados": SHA256, "modelo_selecionado": decisao["selecionado"]["familia"],
        "registos_desenvolvimento": len(desenvolvimento), "registos_teste": len(teste),
        "utilizadores_teste": int(teste.User_ID.nunique()), "metricas": metricas,
        "uso_operacional_recomendado": False,
    }
    destino = RAIZ / "resultados/avaliacao_final.json"
    if destino.exists():
        anterior = json.loads(destino.read_text(encoding="utf-8"))
        if resultado != anterior:
            raise ValueError("A reprodução não coincide com a avaliação final registada; investigar sem reajustar pelo teste.")
    destino.write_text(json.dumps(resultado, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    return resultado, detalhes
