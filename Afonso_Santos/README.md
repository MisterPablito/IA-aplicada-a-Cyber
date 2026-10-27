# Deteção de Tráfego de Rede Malicioso 🛡️

A minha parte do projeto de grupo **IAAC** (IA Aplicada a Cibersegurança) — CTeSP em Cibersegurança, ISTEC Porto.

## Do que é que isto trata?

Imagina que tens uma lista enorme de ligações à internet, e no meio delas há umas quantas que são de "assaltantes" a tentar invadir a rede, disfarçados de ligações normais. O objetivo deste projeto é construir um modelo de Machine Learning que aprenda a distinguir as ligações normais das maliciosas, só olhando para umas quantas pistas (tamanho do pacote, duração, erros de login, etc.).

## O dataset

- **Fonte:** [Kaggle — Cybersecurity Network Logs: Anomaly Detection](https://www.kaggle.com/datasets/aatmaca/cybersecurity-network-logs-anomaly-detection) (autor: aatmaca)
- **Tamanho:** 25 000 ligações de rede
- **Classes:** 95% normais, 5% maliciosas (dataset bastante desequilibrado)
- **Colunas:**

| Coluna | O que é |
|---|---|
| `Protocol` | TCP, UDP ou ICMP |
| `Packet_Size_Bytes` | tamanho do pacote de rede, em bytes |
| `Connection_Duration_ms` | duração da ligação, em milissegundos |
| `Failed_Logins` | quantas vezes houve um login falhado nessa ligação |
| `Geo_Distance_km` | distância geográfica estimada, em km |
| `Is_Malicious` | **o alvo**: 0 = normal, 1 = malicioso |

## O que já foi feito

1. **Machine Learning Canvas** — um "mapa" do projeto: quem usa o modelo (um analista de segurança), o que ele faz com a resposta, e o que ainda falta decidir.
2. **EDA (análise exploratória dos dados)** — espreitar os dados antes de treinar qualquer coisa: histogramas, comparação entre classes, correlações. Descoberta principal: `Failed_Logins`, `Packet_Size_Bytes` e `Geo_Distance_km` são as variáveis que mais ajudam a distinguir malicioso de normal; `Connection_Duration_ms` e `Protocol` quase não ajudam.
3. **Data Preparation** (`data_preparation.py`) — limpar, transformar o `Protocol` em números, pôr tudo na mesma escala, e dividir os dados em treino/validação/teste.
4. **Modeling** (`model_comparison.py`) — comparar 3 modelos diferentes (Regressão Logística, Random Forest, HistGradientBoosting) para ver qual se sai melhor.

## O que ainda falta

- Definir quanto custa cada tipo de erro (deixar passar um ataque vs. dar um alarme falso)
- Afinar os parâmetros do modelo escolhido
- Testar o modelo final no conjunto de teste (ainda intocado, de propósito)
- Decidir como monitorizar o modelo depois de estar a funcionar

## Como correr o projeto

**1. Criar e ativar um ambiente virtual** (para não misturar bibliotecas com outros projetos):

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1      # Windows (PowerShell)
# source venv/bin/activate       # Mac/Linux
```

> ⚠️ **O erro mais comum:** esquecer de ativar o venv antes de correr os scripts. Sabes que está ativo quando aparece `(venv)` no início da linha do terminal.

**2. Instalar as dependências:**

```powershell
pip install -r requirements.txt
```

**3. Correr os scripts, por esta ordem** (o segundo depende do primeiro):

```powershell
python data_preparation.py
```
→ Isto cria uma pasta `prepared/` com `train.csv`, `val.csv`, `test.csv` e `scaler_mean_std.json`.

```powershell
python model_comparison.py
```
→ Lê a pasta `prepared/` e mostra no terminal (e guarda em CSV) a comparação dos 3 modelos.

## Estrutura dos ficheiros

```
.
├── cybersecurity_network_logs.csv   # dataset original (não se mexe neste ficheiro)
├── data_preparation.py              # limpeza, encoding, escala e split dos dados
├── model_comparison.py              # treina e compara os 3 modelos
├── requirements.txt                 # bibliotecas necessárias
├── prepared/                        # gerado pelos scripts (não é enviado para o Git)
│   ├── train.csv / val.csv / test.csv
│   └── scaler_mean_std.json
└── README.md                        # este ficheiro
```

## Principais decisões (e porquê)

- **Os outliers não foram removidos.** Verifiquei e a maior parte dos valores "fora do normal" são precisamente as ligações maliciosas — não é ruído, é o sinal que o modelo precisa de aprender.
- **Sem SMOTE/undersampling.** A separação entre classes já é forte; inventar dados numa fronteira já limpa só traria ruído artificial. Em vez disso, uso `class_weight="balanced"` nos modelos.
- **Três modelos comparados**, não só um — para não ficar preso à primeira ideia que funcionou.

*(Mais detalhes e os gráficos da EDA estão no relatório do grupo.)*
