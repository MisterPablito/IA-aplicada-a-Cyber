# Guia simples do trabalho individual de Nathan

**Turma:** 2ºCIB

O ficheiro **IAAC_Phishing_Simples.ipynb** contém o trabalho, o código e os resultados. Este guia explica como o executar e apresentar. O notebook foi adaptado para trabalho individual e executado sem erros com o CSV real.

## Primeiro perceber dataset e modelos

**Um dataset é uma tabela de exemplos. Um modelo é uma forma de aprender com esses exemplos.** Neste caso, tens um dataset de phishing e treinas vários modelos com os mesmos dados.

Os três modelos a destacar são:

- **Árvore de decisão / Decision Tree:** faz perguntas sobre as características para decidir a classe.
- **Random Forest:** combina várias árvores para produzir uma previsão.
- **XGBoost:** acrescenta árvores sucessivamente para melhorar as previsões.

Sim, é preciso treinar os modelos, e **o código do notebook já faz isso**. Não tens de criar uma IA de raiz. Ao executar `fit`, a biblioteca aprende com os exemplos de treino. Ao executar `predict`, prevê a classe de outros exemplos. Depois as métricas comparam essas previsões com as respostas certas.

Pela conversa que partilhaste, o foco atual é treinar, validar e testar pelo menos três modelos e mostrar as cinco métricas em tabelas, além dos gráficos. Essa conversa é uma orientação de um colega; não confirma que os outros mínimos do roadmap foram dispensados. Por isso, mantive-os no notebook. Criar um agente é uma possível etapa futura e não faz parte desta entrega.

## 1 Como abrir e executar

1. Guarda o ficheiro `IAAC_Phishing_Simples.ipynb` no computador.
2. Abre o [Google Colab](https://colab.research.google.com/).
3. Escolhe **Ficheiro / File → Carregar notebook / Upload notebook** e seleciona o ficheiro.
4. Usa um ambiente Python com CPU; não precisas de GPU.
5. Escolhe **Ambiente de execução / Runtime → Executar tudo / Run all** e espera que termine.
6. Confirma o nome Nathan e a turma 2ºCIB e guarda uma cópia com os resultados.

O CSV é descarregado automaticamente. Se falhar, descarrega o ZIP do [Kaggle](https://www.kaggle.com/datasets/eswarchandt/phishing-website-detector), extrai **phishing.csv** e carrega-o no painel **Ficheiros** do Colab. Volta a executar tudo. Não uses o TXT.

Também podes executar cada bloco com ▶. Lê o texto antes do código. Se aparecer `NameError`, falta executar um bloco anterior. Os nomes dos menus podem variar com o idioma.

## 2 O que mostrar nesta fase

| O que mostrar | Onde encontrar |
|---|---|
| Explicação do problema e dataset | Secções 1 e 3 do notebook |
| Preparação e gráficos dos dados | Secções 4 a 6 |
| Treino e tabela de validação dos modelos | Secção 8 |
| Ajuste de parâmetros e treino versus validação | Secção 9 |
| Tabelas de teste com as cinco métricas | Secção 10 |
| Gráfico de comparação, curvas ROC e matriz de confusão | Secção 10 |
| Conclusão com os resultados reais | Secção 11 |

**Treino ensina; validação ajuda a escolher; teste mede o resultado final.** O notebook usa cerca de 80% para treino e 20% para teste. Dentro do treino, faz validação cruzada com três divisões.

Todos os modelos usam a mesma separação dos dados. O modelo final é escolhido pelo F1 de validação. As tabelas de teste são apresentadas depois dessa escolha, sem voltar a ajustar os modelos por causa desses resultados.

## 3 Resultados numéricos dos três modelos

Estes valores foram calculados pelo código com o CSV real, semente 42, na execução de 13 de outubro de 2026. Precision, recall e F1 referem-se à classe **phishing**.

### Validação

Média das três divisões feitas dentro do treino.

| Modelo | Accuracy | Precision | Recall | F1 | ROC-AUC |
|---|---:|---:|---:|---:|---:|
| Árvore de decisão | 90,77% | 93,27% | 88,68% | 90,84% | 0,9694 |
| Random Forest | 94,96% | 95,39% | 94,83% | 95,11% | 0,9909 |
| XGBoost | 93,87% | 94,62% | 93,47% | 94,03% | 0,9870 |


### Teste

Resultados nos mesmos **1 167 exemplos reservados** para todos os modelos.

| Modelo | Accuracy | Precision | Recall | F1 | ROC-AUC |
|---|---:|---:|---:|---:|---:|
| Árvore de decisão | 92,37% | 92,79% | 92,32% | 92,55% | 0,9792 |
| Random Forest | 96,23% | 96,80% | 95,83% | 96,31% | 0,9946 |
| XGBoost | 95,54% | 96,12% | 95,16% | 95,64% | 0,9919 |


O **Random Forest** foi escolhido pelo F1 de validação e também teve o melhor F1 neste teste. Detetou **574 dos 599 casos de phishing**, deixou passar **25** e gerou **19 falsos alarmes**. O ajuste de parâmetros não melhorou a configuração inicial nas combinações testadas.

As tabelas completas no notebook incluem ainda os restantes modelos do roadmap e a referência Dummy. No notebook, as métricas aparecem entre 0 e 1: `0.9623` corresponde a aproximadamente `96,23%`. Neste guia, as primeiras quatro métricas estão em percentagem e ROC-AUC permanece entre 0 e 1.

### O que significa cada métrica

- **Accuracy:** de todos os exemplos, quantos classifiquei corretamente.
- **Precision:** dos exemplos que sinalizei como phishing, quantos eram mesmo phishing.
- **Recall:** de todo o phishing existente, quanto consegui detetar.
- **F1:** uma medida que combina precision e recall.
- **ROC-AUC:** capacidade de separar as classes ao variar o limiar; quanto mais perto de 1, melhor a separação.

Os dados tinham **11 054 linhas**, **30 características** e nenhum valor em falta. Depois de retirar o índice e **5 205 cópias**, ficaram **5 849 linhas**: 4 682 para treino e 1 167 para teste. Há 64 padrões com respostas contraditórias; os padrões iguais ficam juntos na divisão para evitar repetição entre treino e teste. Aqui, “grupos” significa grupos de linhas de dados, não uma equipa de alunos.

São dados históricos com características já calculadas. Estes resultados não garantem deteção em sites atuais, nem permitem analisar um link diretamente sem extrair as características. As bibliotecas da execução verificada incluem pandas 3.0.1, scikit-learn 1.9.1 e XGBoost 3.4.1; outra versão dos dados ou das bibliotecas pode alterar os valores. Usa os resultados da tua execução.

## 4 Onde está cada mínimo do roadmap

| Tema marcado com M | Onde está no notebook |
|---|---|
| Business e Data Understanding | Secções 1 e 3: problema, utilizador, entradas, saída e dados |
| EDA univariada, bivariada e multivariada | Secção 5: frequências, tabelas e cruzamento de variáveis |
| Visualização e análise de correlação | Secção 5: gráficos, Pearson e Spearman |
| Introdução à preparação e limpeza | Secção 4: retirar índice e cópias |
| Missing values e outliers | Secções 4 e 6: verificar códigos e usar preenchimento na pipeline |
| Splitting data | Secção 4: treino e teste separados por grupos |
| Feature scaling e imbalanced data | Secção 6: StandardScaler, proporções e pesos das classes no ajuste |
| Supervised learning e classification | Secções 1 e 7 |
| Introdução à regressão linear | Secção 7: explicação e exemplo fictício separado |
| Regressão logística, árvores e tipos de árvores | Secções 7 e 8 |
| KNN, Naive Bayes e SVM | Secções 7 e 8 |
| Ensemble, Gradient Boosting, XGBoost e Random Forest | Secções 7 e 8 |
| Hyperparameter tuning | Secção 9: GridSearchCV com oito configurações |
| Overfitting e underfitting | Secção 9: comparação de treino e validação |
| Confusion matrix, precision, recall, F1 e ROC-AUC | Secção 10 |
| User stories, sprints, branches e Scrum | Secção 5 deste guia: adaptação individual |

A regressão linear aparece como introdução, porque prever phishing é um problema de classificação. As variantes de regressão e outros temas sem M ficaram fora. Para os algoritmos marcados com M, incluí implementações simples, mesmo quando o roadmap só indica uma introdução.


## 5 Organização individual sem complicar

**Responsável por todas as tarefas: Nathan.** O backlog é a tua lista de tarefas; o sprint é um pequeno período em que escolhes algumas para concluir. Não há divisão entre pessoas.

| Tarefa | Critério de conclusão | Sprint proposto |
|---|---|---|
| US01 — Como autor, quero explicar o problema para definir o objetivo. | Problema, entrada, saída e dados explicados. | 1 |
| US02 — Como analista, quero explorar os dados para compreender padrões. | Gráficos e correlações acompanhados de observações. | 1 |
| US03 — Como analista, quero preparar os dados para avaliar de forma fiável. | Limpeza, divisão, scaling e classes verificados. | 2 |
| US04 — Como analista, quero comparar modelos para escolher uma solução. | Modelos treinados e tabela de validação completa. | 3 |
| US05 — Como analista, quero avaliar os erros para conhecer os limites. | Tuning, cinco métricas de teste, ROC e matriz completos. | 4 |
| US06 — Como autor, quero explicar o trabalho para o apresentar. | Conclusão compreendida e notebook guardado. | 4 |

Se a organização em GitHub fizer parte da entrega, cria uma issue por tarefa, atribui-a a ti e usa os estados **Por fazer**, **Em curso** e **Concluído**. Podes criar uma branch por tarefa, como `nathan-eda` ou `nathan-modelos`, e registar commits do trabalho efetivamente realizado. Não precisas de inventar revisores nem membros de equipa.

Para adaptar os registos de Scrum ao trabalho individual, usa o template da aula se tiver sido fornecido. Os modelos abaixo são registos pessoais; não representam reuniões de equipa já realizadas.

**Registo de progresso por aula — adaptação do Daily**

```text
Data:
Autor: Nathan
O que concluí:
O que vou fazer a seguir:
Dificuldades:
```

**Revisão — a cada duas aulas, conforme o roadmap**

```text
Data e sprint:
Tarefas concluídas:
Resultados ou evidências:
O que ficou pendente:
Feedback recebido, se existir:
```

**Retrospetiva individual — a cada duas aulas**

```text
O que correu bem:
O que me dificultou o trabalho:
Uma melhoria para o próximo sprint:
```

Preenche apenas acontecimentos reais. As tarefas estão preparadas em `docs/BACKLOG.md` e os modelos de registo em `docs/REGISTO_INDIVIDUAL.md`. As issues, branches e registos pessoais no GitHub devem corresponder ao trabalho que efetivamente realizares.

## 6 Como explicar ao professor

Podes seguir esta sequência, depois de compreenderes o código:

> Usei um dataset de phishing e treinei vários modelos com os mesmos dados. Para a comparação principal, destaquei Árvore de Decisão, Random Forest e XGBoost. Comparei accuracy, precision, recall, F1 e ROC-AUC em tabelas e gráficos. Escolhi o Random Forest pelo F1 de validação. No teste, detetou 574 de 599 casos de phishing e obteve cerca de 96,2% de accuracy. Ainda existem erros e o modelo não foi validado em sites atuais.

Se te perguntarem onde treinaste os modelos, mostra `cross_validate` na secção 8 e `fit` nas secções 9 e 10. Se te perguntarem pelos números, mostra as tabelas das secções 8 e 10.

## 7 Antes de entregar

- [ ] Confirmar o nome Nathan e a turma 2ºCIB.
- [ ] Executar o notebook inteiro e guardar os resultados.
- [ ] Confirmar que as tabelas mostram os três modelos e as cinco métricas.
- [ ] Conseguir explicar os gráficos e a diferença entre dataset e modelo.
- [ ] Ler a conclusão e adaptá-la às tuas palavras e à tua execução.
- [ ] Acrescentar os registos individuais de organização pedidos pelo professor.
- [ ] Confirmar o formato e o local de entrega da aula.

As referências técnicas estão no final do notebook, incluindo o [dataset do Kaggle](https://www.kaggle.com/datasets/eswarchandt/phishing-website-detector), a [documentação das métricas](https://scikit-learn.org/stable/modules/model_evaluation.html) e o [MLU Explain](https://mlu-explain.github.io/) indicado no roadmap. O código foi verificado localmente; a execução na tua conta do Colab é feita seguindo este guia.
