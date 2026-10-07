# Comparacao inicial de modelos

**Data:** 30/09/2026  
**Ambito:** componente individual do dataset de ciberataques.

Comparei classificadores com validacao cruzada estratificada de tres folds, usando apenas os dados de treino. O pre-processamento foi mantido dentro de cada pipeline.

| Modelo | Macro-F1 CV | Accuracy CV |
|---|---:|---:|
| Random Forest | 1,0000 | 1,0000 |
| XGBoost | 1,0000 | 1,0000 |
| Arvore de decisao | 1,0000 | 1,0000 |
| k-NN | 0,9997 | 0,9997 |
| SVM linear | 0,9997 | 0,9997 |
| Regressao logistica | 0,9994 | 0,9994 |
| Gaussian Naive Bayes | 0,8062 | 0,8239 |
| Baseline (classe mais frequente) | 0,1002 | 0,2508 |

Random Forest, XGBoost e arvore de decisao empataram no macro-F1 medio apresentado. Depois do ajuste da arvore, mantive o Random Forest como candidato final pela regra de selecao implementada. A avaliacao no teste retido e as limitacoes estao em [Resultados](RESULTADOS.md).
