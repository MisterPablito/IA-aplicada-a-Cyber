# Enquadramento dos conteúdos da disciplina

## Classificação, regressão linear e regressão logística

A classificação prevê uma categoria, aqui Normal ou Suspicious. A regressão linear aproxima uma resposta numérica contínua por uma combinação das entradas, ajustando coeficientes, habitualmente através do erro quadrático. A introdução à regressão linear está assinalada com M no Roadmap e é aqui enquadrada; não é usada como classificador principal porque não modela diretamente uma categoria e pode produzir valores fora do intervalo de probabilidades.

A regressão logística aplica a função sigmoide à combinação linear para obter uma pontuação entre zero e um. O ajuste utiliza uma perda logística, não o erro quadrático de uma regressão linear. A regularização penaliza coeficientes extremos; no parâmetro C de scikit-learn, valores menores correspondem a regularização mais forte. O limiar converte pontuações em classes e é um parâmetro de decisão distinto dos coeficientes.

O projeto não inclui um alvo contínuo que justifique experiências de regressão ou métricas como MAE e RMSE. Esse código não é acrescentado apenas para preencher uma lista.

## Árvores, vizinhança e Bayes

Uma árvore de decisão aprende separações sucessivas das entradas. ID3, C4.5 e CART representam famílias de métodos; a implementação usada é CART para classificação com critério Gini. Profundidade e número mínimo de registos por folha limitam a complexidade. Uma árvore não limitada pode memorizar pequenas particularidades do treino.

KNN classifica pela vizinhança nas entradas transformadas. A escala influencia as distâncias e a representação de muitas categorias pode reduzir o seu significado. Naïve Bayes combina probabilidades com uma hipótese de independência condicional que simplifica o cálculo. GaussianNB admite entradas contínuas, mas as categorias codificadas e os pares temporais podem violar as suas hipóteses; essa limitação faz parte da comparação.

## SVM e ensembles

SVM procura uma fronteira de margem ampla; o kernel RBF permite relações não lineares. As suas pontuações de decisão não são probabilidades calibradas. Random Forest representa bagging, combinando árvores com bootstrap e subconjuntos de entradas. Gradient Boosting e XGBoost representam boosting, adicionando árvores sequencialmente para melhorar uma função de perda, com opções de regularização.

Estas abordagens são comparadas na mesma divisão e com preparação dentro dos folds. Os pesos balanced, priors iguais e o peso positivo do XGBoost são opções para estudar o desequilíbrio; não criam informação discriminativa ausente nos dados.

## Avaliação, complexidade e generalização

Accuracy elevada pode resultar da classe maioritária. Precision descreve a qualidade dos alertas, Recall a proporção de casos suspeitos identificados e F1 a sua média harmónica. A matriz de confusão expõe a carga de falsos positivos e os casos não sinalizados. ROC-AUC e Average Precision avaliam a ordenação por pontuações, separadamente do limiar utilizado.

Desempenho elevado no treino e fraco fora dele é compatível com sobreajustamento. Desempenho insuficiente nos dois conjuntos pode resultar de subajustamento, pouco sinal nas entradas, desequilíbrio ou limiar inadequado; não identifica isoladamente a causa. A regularização e a limitação de complexidade procuram controlar a generalização, sem garantias de melhoria.

A validação cruzada estima a variabilidade dentro do desenvolvimento; os seus folds não são amostras de incidentes independentes. O teste reservado descreve o resultado da configuração fixada, não serve para a otimizar. A heurística de um erro padrão favorece simplicidade e não demonstra equivalência estatística.
