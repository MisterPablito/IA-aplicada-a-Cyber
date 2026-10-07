# Guia simples

## Objetivo

O projeto classifica registos do dataset de tráfego como Normal, DDoS, PortScan ou BruteForce. É uma experiência académica com um CSV local, não um sistema de defesa pronto para produção.

## Preparar os dados

O script verifica os dados, remove duplicados da cópia carregada em memória, separa treino e teste de forma estratificada e define encoding e scaling num pipeline.

## Executar

Na pasta raiz do projeto, no Windows:

```powershell
.\.venv\Scripts\python.exe iaac_minimum_apply.py
```

O script usa `data/cyber_attack_dataset_100000.csv` por omissão. Também aceita o caminho para outro CSV como primeiro argumento. Os resultados e gráficos são escritos em `resultados/`.

## Modelos e métricas

Comparei um baseline, regressão logística, árvore de decisão, k-NN, Gaussian Naive Bayes, SVM linear, Random Forest e XGBoost. Usei macro-F1 para dar o mesmo peso às quatro classes e accuracy como métrica complementar. A validação cruzada e o ajuste da árvore usam apenas os dados de treino; o conjunto de teste fica reservado para a avaliação final.

O Random Forest foi selecionado por validação cruzada. Os resultados perfeitos no teste devem ser interpretados com cautela: no dataset, `protocol` e `failed_logins` têm relações muito fortes com algumas classes. Isto não demonstra que o modelo generalize para tráfego real; os detalhes estão em `docs/RESULTADOS.md`.
