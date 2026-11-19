# Relatório pessoal — classificação de ataques

**Aluno:** Guilherme Jesus  
**Turma:** 2.º Ciber  
**Âmbito:** componente individual do dataset de ciberataques.

## Objetivo

Apliquei o fluxo de aprendizagem supervisionada do roadmap ao dataset *Cyber Security Attack Using Network Traffic*, obtido no Kaggle. O alvo é `attack_type`, com as classes Normal, DDoS, PortScan e BruteForce.

## Dados e método

A cópia local contém 100.000 registos e sete colunas. Não encontrei valores nulos e removi uma duplicação exata da cópia carregada para análise. Usei uma divisão estratificada de 79.999 registos para treino e 20.000 para teste. O encoding de `protocol` e o scaling das variáveis numéricas são ajustados dentro dos pipelines.

Comparei baseline, regressão logística, árvore, k-NN, Gaussian Naive Bayes, SVM linear, Random Forest e XGBoost com três folds estratificados no treino. Ajustei também uma árvore com procura aleatória. Escolhi o Random Forest pela validação cruzada e só depois avaliei o modelo no teste retido.

## Resultados

O Random Forest obteve macro-F1 CV de 1,0000 e, no teste, accuracy, macro-F1 e ROC-AUC macro OvR de 1,0000. As métricas por classe também foram 1,0000. Os gráficos, o modelo e as métricas estruturadas estão em `../resultados/`; a análise detalhada está em `RESULTADOS.md`.

## Limitações e conclusão

Os resultados perfeitos não demonstram generalização. No CSV, `protocol` e `failed_logins` têm relações quase determinísticas com os rótulos. A avaliação usa uma divisão aleatória da mesma fonte; não há timestamp nem ID de sessão e não testei uma fonte independente. Assim, o modelo serve como exercício académico, não como ferramenta operacional de defesa.

Não implementei deteção em tempo real, alertas ou integração com sistemas de monitorização. Essas ideias permanecem hipóteses para trabalho futuro, condicionadas a validação independente e requisitos operacionais.
