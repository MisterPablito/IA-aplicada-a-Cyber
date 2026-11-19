# Deteção de Tráfego de Rede Malicioso 🛡️

Projeto de IA aplicada à cibersegurança: deteção de tráfego de rede malicioso com modelos de Machine Learning, desenvolvido no âmbito do CTeSP em Cibersegurança do ISTEC Porto.

## Projeto

O objetivo é treinar e comparar modelos que distinguem ligações de rede normais de ligações maliciosas, usando o dataset [Cybersecurity Network Logs: Anomaly Detection](https://www.kaggle.com/datasets/aatmaca/cybersecurity-network-logs-anomaly-detection), de aatmaca. O CSV contém 25 000 ligações, com classes desequilibradas (cerca de 95% normais e 5% maliciosas).

O processo inclui preparação dos dados, codificação de `Protocol`, normalização das variáveis numéricas e divisão estratificada em treino, validação e teste. Depois são comparados Regressão Logística, Random Forest e HistGradientBoosting. O conjunto de teste fica reservado para avaliação final.

## Estrutura

```text
.
├── data/
│   ├── cybersecurity_network_logs.csv
│   └── README.md
├── docs/
│   └── Relatorio_IAAC_Afonso_Santos_final.docx
├── scripts/
│   ├── data_preparation.py
│   └── model_comparison.py
├── prepared/                 # gerada pelos scripts; ignorada pelo Git
├── requirements.txt
└── README.md
```

## Como executar

Na raiz do repositório, cria e ativa um ambiente virtual e instala as dependências:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Executa os scripts pela ordem indicada:

```powershell
python scripts/data_preparation.py
python scripts/model_comparison.py
```

O primeiro script lê o CSV em `data/` e cria os conjuntos de treino, validação e teste em `prepared/`. O segundo compara os modelos usando treino e validação e guarda as métricas em `prepared/model_comparison_val.csv`.

## Decisões principais

- Os outliers são mantidos porque muitos correspondem a ligações maliciosas e contêm informação útil para a deteção.
- Não é aplicado SMOTE nem undersampling; os modelos usam pesos de classe equilibrados.
- São usadas métricas PR-AUC, ROC-AUC e recall para vários níveis de precisão, porque a accuracy isolada não descreve bem o desempenho num dataset desequilibrado.
- A divisão é estratificada e reproduzível (`random_state=42`).

Mais detalhes sobre os dados, as decisões e os resultados estão no [relatório](docs/Relatorio_IAAC_Afonso_Santos_final.docx).
