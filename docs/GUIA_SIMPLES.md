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
