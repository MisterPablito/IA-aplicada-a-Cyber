# IA-aplicada-a-Cyber
IA aplicada a Cyber

Projeto académico do CTeSP de Cibersegurança do ISTEC Porto, dedicado à classificação de atividades informáticas como `Normal` ou `Suspicious` com o Cybercrime Forensic Dataset.

O [âmbito do projeto e os critérios de sucesso](docs/ambito_e_criterios.md) documentam o problema, a utilização prevista, o protocolo de comparação e as limitações conhecidas. Este enquadramento orienta a continuação do trabalho existente.

## Resultado principal

Foram implementados oito classificadores, duas referências simples, preparação sem informação do alvo, validação cruzada por utilizador e otimização. **Não foi demonstrada uma melhoria útil sobre a regra que sinaliza todas as atividades.** A seleção e os parâmetros foram enviados no commit `c6f6558` antes da avaliação final.

| Modelo no teste reservado | Accuracy | Precision de Suspicious | Recall | F1 | ROC-AUC | Average Precision |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Sempre Normal | 0,8287 | 0 por convenção, sem alertas | 0 | 0 | 0,5000 | 0,1713 |
| Sempre Suspicious — referência selecionada | 0,1713 | 0,1713 | 1,0000 | 0,2925 | 0,5000 | 0,1713 |
| Logística otimizada, limiar 0,2 | 0,1713 | 0,1713 | 1,0000 | 0,2925 | 0,5178 | 0,1792 |

A referência selecionada e a logística sinalizam os 1 506 registos de teste: 258 verdadeiros positivos e 1 248 falsos positivos. Recall total não demonstra discriminação útil. **Não se recomenda utilização operacional.** Os resultados completos e a interpretação estão no [relatório final](docs/relatorio_final.md).

## Dados e objetivo

O [Cybercrime Forensic Dataset](https://www.kaggle.com/datasets/jimohyusuf/cybercrime-forensic-dataset/data), publicado por jimohyusuf, contém 7 400 atividades **simuladas**, 11 colunas e duas classes: 6 167 `Normal` e 1 233 `Suspicious`. O intervalo observado é de 12/09/2024 a 12/10/2024. A classe positiva é `Suspicious`, codificada como 1.

O projeto estuda a classificação de uma atividade já registada, usando informação disponível antes da sua classificação. Um rótulo suspeito não confirma um incidente real. A fonte declara licença MIT para o dataset; não se atribui automaticamente essa licença ao código do repositório. Proveniência, integridade, significado dos campos e dúvidas estão em [dados.md](docs/dados.md). A unidade de `File_Size`, o fuso horário e o código de geração não estão confirmados.

## Estrutura

```text
data/raw/       CSV original preservado
notebooks/      EDA, preparação, comparação e avaliação
src/            Leitura, preparação, avaliação, experiências, otimização e previsões
tests/          Testes de integridade, protocolo, métricas e reprodução
scripts/        Execução integral dos notebooks em kernels novos
resultados/     Métricas pequenas, decisão congelada e gráficos
exemplos/       Formato de entrada e demonstração batch
docs/           Enquadramento, dados, ambiente, backlog e relatório
artefactos/     Modelos e previsões locais; pasta ignorada pelo Git
```

## Instalação

Ambiente verificado: Windows 11, Python 3.14.8, NumPy 2.5.3, pandas 3.1.0, scikit-learn 1.9.1 e XGBoost 3.4.1. As restantes versões verificadas estão em [requirements.txt](requirements.txt); o [ficheiro completo de versões](requirements-lock.txt) fixa 54 dependências diretas e transitivas para este ambiente.

Na raiz do projeto, em PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-lock.txt
.\.venv\Scripts\python.exe -m pip check
```

Não é necessário alterar o Python global. Selecionar `.venv\Scripts\python.exe` como interpretador e kernel no VS Code, com as extensões Python e Jupyter. Consultar [ambiente.md](docs/ambiente.md) para a validação realizada e justificação das bibliotecas.

## Ordem de execução

1. [01_data_understanding.ipynb](notebooks/01_data_understanding.ipynb): EDA existente consolidada, duplicados, ausências, IQR, correlações e fuga de informação.
2. [02_data_preparation.ipynb](notebooks/02_data_preparation.ipynb): divisão por utilizador e demonstração da preparação.
3. [03_model_comparison.ipynb](notebooks/03_model_comparison.ipynb): referências e oito classificadores, produzindo `resultados/desenvolvimento.json`.
4. [04_model_evaluation.ipynb](notebooks/04_model_evaluation.ipynb): comparação, resultados da otimização já executada, decisão congelada, avaliação final e exemplo batch.

Para validar a sequência num kernel novo para cada notebook, sem regravar as saídas dos notebooks:

```powershell
.\.venv\Scripts\python.exe scripts/executar_notebooks.py notebooks/01_data_understanding.ipynb notebooks/02_data_preparation.ipynb notebooks/03_model_comparison.ipynb notebooks/04_model_evaluation.ipynb
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Os notebooks 03 e 04 atualizam os seus pequenos ficheiros de resultados; o executador só grava saídas nos ficheiros `.ipynb` com `--gravar`. Não depende de ficheiros temporários: os notebooks localizam a raiz e utilizam o CSV versionado. A versão e a integridade da decisão final são verificadas, e uma reprodução diferente da avaliação registada é recusada.

## Metodologia

- Divisão por `User_ID`, com semente 42: treino com 4 416 registos/3 018 utilizadores, validação com 1 478/1 006 e teste com 1 506/1 007. Não há utilizadores nem linhas comuns. As proporções são aproximadamente 60%/20%/20% dos utilizadores, não uma estratificação por linhas.
- Entradas permitidas: `Timestamp`, `Activity_Type`, `Resource_Accessed`, `Action`, `Login_Attempts` e `File_Size`. `Label`, `Label_bin` e `Anomaly_Type` nunca entram nos modelos.
- `User_ID` serve apenas para agrupar; `IP_Address` é excluído por elevada cardinalidade e falta de contexto transferível. `File_Name` é redundante com o recurso acedido. Os motivos estão no notebook 02.
- Ausências numéricas estruturais tornam-se zero; ausências inesperadas em atividades aplicáveis são recusadas. `None` e `N/A` continuam categorias. Não são eliminadas linhas por ausência estrutural.
- Seno/cosseno da hora e do dia da semana, OneHotEncoder e StandardScaler integram uma Pipeline. Categorias e escala são aprendidas no treino de cada fold. Não há reamostragem global ou ajuste ao teste.
- Cinco folds de StratifiedGroupKFold no treino. Modelos: regressão logística, árvore, Random Forest, KNN, Naïve Bayes gaussiano, SVM RBF, Gradient Boosting e XGBoost.
- Otimização de logística, árvore e Naïve Bayes: 42 configurações, 210 ajustes; hiperparâmetros e limiar pesquisados conjuntamente nos folds. A regra de um erro padrão favorece simplicidade em soluções próximas, sem representar um teste de significância.
- A configuração congelada é reajustada no desenvolvimento completo antes do teste. A avaliação final abrange as referências e a melhor alternativa aprendida previamente escolhida. Não se escolhem algoritmos ou parâmetros pelo teste.

## Previsões locais

```powershell
.\.venv\Scripts\python.exe -m src.previsoes treinar
.\.venv\Scripts\python.exe -m src.previsoes prever exemplos/atividades.csv --saida artefactos/previsoes.csv
```

O ficheiro de entrada requer apenas as seis características permitidas. O exemplo contém três linhas do treino, sem rótulos nem anomalias. A saída mantém a ordem das linhas e contém previsão e pontuação. **A regra selecionada devolve sempre Suspicious; a pontuação 1 não representa certeza de ameaça.** Instruções em [exemplos/README.md](exemplos/README.md). Os binários locais não são publicados no Git.

## Limitações e evolução

A EDA original explorou o dataset completo antes da reserva do teste. Os rótulos são de dados simulados; faltam incidentes independentes e validação operacional. A divisão por utilizador não comprova generalização temporal. A pesquisa limitada e a comparação de várias configurações podem introduzir otimismo. Não foi demonstrada capacidade útil para reduzir a investigação de atividades normais.

Melhorias futuras exigem novos dados representativos, rótulos validados, separação temporal e por incidente e critérios operacionais definidos por analistas. A seleção atual não deve ser reajustada com base no teste já observado; uma nova experiência requer validação independente.

O [mapa de requisitos](docs/requisitos_roadmap.md) distingue conteúdos cumpridos, parciais e não aplicáveis. O [backlog](docs/backlog_e_sprints.md) é uma proposta da parte de Luís Peneda: não inventa reuniões ou decisões do grupo. A consulta dos Projects V2 permaneceu limitada pela permissão `read:project`.

O [registo de desenvolvimento](docs/registo_desenvolvimento.md) relaciona commits, validações e pushes. O histórico anterior e as branches dos colegas foram preservados.
