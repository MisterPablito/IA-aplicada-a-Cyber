# IAAC — Deteção de phishing

**Autor:** Nathan · **Turma:** 2ºCIB

Este projeto usa Machine Learning para classificar exemplos como **phishing** ou **legítimos**, a partir de 30 características já calculadas. O dataset é o [Phishing website Detector do Kaggle](https://www.kaggle.com/datasets/eswarchandt/phishing-website-detector).

O trabalho inclui preparação dos dados, análise exploratória, treino, validação, ajuste de parâmetros e avaliação. A comparação principal destaca **Árvore de Decisão, Random Forest e XGBoost**. Os restantes classificadores mantêm a cobertura dos tópicos M do roadmap IAAC.

## Como ver o trabalho

1. Abre o [notebook com código e resultados](notebooks/IAAC_Phishing_Simples.ipynb).
2. Vê a **secção 8** para a validação e a **secção 10** para as tabelas de teste, os gráficos e as curvas ROC.
3. Lê a **secção 11** para a conclusão ou o [relatório de resultados](docs/RESULTADOS.md).

Para perceber o código e preparar a apresentação, segue o [guia simples](docs/GUIA_SIMPLES.md).

## Executar no Google Colab

1. Descarrega o notebook deste repositório.
2. Abre o [Google Colab](https://colab.research.google.com/) e carrega o notebook.
3. Escolhe Python com CPU e executa todas as células por ordem.

O notebook descarrega automaticamente `phishing.csv`. Se o download falhar, descarrega o ZIP do Kaggle, extrai o CSV e carrega-o no painel Ficheiros do Colab. Os resultados da execução verificada já estão guardados no notebook.

## Resultados principais

Avaliação nos mesmos **1 167 exemplos de teste**, com phishing como classe positiva. As primeiras quatro métricas estão em percentagem; ROC-AUC está entre 0 e 1.

| Modelo | Accuracy | Precision | Recall | F1 | ROC-AUC |
|---|---:|---:|---:|---:|---:|
| Árvore de decisão | 92,37% | 92,79% | 92,32% | 92,55% | 0,9792 |
| Random Forest | 96,23% | 96,80% | 95,83% | 96,31% | 0,9946 |
| XGBoost | 95,54% | 96,12% | 95,16% | 95,64% | 0,9919 |


O modelo escolhido pelo F1 de validação foi **Random Forest**. No teste, detetou **574 de 599 casos de phishing**, deixou passar **25** e gerou **19 falsos alarmes**. A escolha foi feita antes da comparação final no teste.

![Comparação das métricas e curvas ROC](resultados/graficos/comparacao_e_roc.png)

## Método

- Remoção de `Index` e 5 205 cópias de linhas, ficando 5 849 exemplos.
- Aproximadamente 80% para treino e 20% para teste, sem padrões idênticos nos dois conjuntos.
- Validação cruzada com três divisões agrupadas apenas no treino.
- Preparação dentro de pipelines e scaling nos modelos que dele beneficiam.
- Escolha por F1 de validação; ajuste de oito configurações de Random Forest.
- Avaliação com accuracy, precision, recall, F1, ROC-AUC e matriz de confusão.

## Estrutura

```text
IAAC_Nathan_2CIB/
├── README.md
├── requirements.txt
├── .gitignore
├── notebooks/
│   └── IAAC_Phishing_Simples.ipynb
├── data/
│   └── README.md
├── docs/
│   ├── GUIA_SIMPLES.md
│   ├── RESULTADOS.md
│   ├── BACKLOG.md
│   └── REGISTO_TRABALHO.md
└── resultados/
    ├── resumo_resultados.json
    └── graficos/
        ├── comparacao_e_roc.png
        └── matriz_confusao.png
```

## Executar localmente no Windows

Na pasta principal do projeto:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Abre o notebook no VS Code com as extensões Python e Jupyter, seleciona o Python de `.venv` e executa as células. O CSV e o resumo JSON gerados durante a execução ficam na pasta de trabalho do notebook. Não é necessário instalar Docker.


## Limitações e fontes

É um protótipo académico com dados históricos. A entrada é uma linha com características já calculadas; não é um URL. O desempenho não garante deteção de ataques atuais. Existem padrões com rótulos contraditórios, e a remoção de cópias muda a frequência original dos padrões.

Dados: [Eswar Chand T — Kaggle](https://www.kaggle.com/datasets/eswarchandt/phishing-website-detector), versão 3 consultada em 13/10/2026; correspondência verificada com [UCI Phishing Websites — Mohammad e McCluskey](https://archive.ics.uci.edu/dataset/327/phishing+websites), excluindo a primeira linha do UCI e o índice do CSV. Mais referências no notebook.
