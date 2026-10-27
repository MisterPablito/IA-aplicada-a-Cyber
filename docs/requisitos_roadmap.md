# Evidências do Roadmap e do Canvas

As páginas referem-se ao IAAC - Roadmap de cinco páginas e ao Canvas de três páginas fornecidos. M corresponde à marcação explícita no Roadmap. Conteúdos listados sem M podem ter sido implementados por serem úteis ou pedidos pelo utilizador; isso não os transforma retroativamente em mínimos do professor.

| Conteúdo | M no Roadmap | Estado | Evidência |
| --- | --- | --- | --- |
| Business e Data Understanding | Aula de 21/09 identificada com M, pp. 1–2 | Cumprido | Âmbito, dados e notebook 01. |
| EDA: introdução, univariada, bivariada e multivariada | Sim, p. 1 | Cumprido | Notebook 01, conservando o trabalho original e acrescentando validações. |
| Visualização e análise de correlação | Sim, p. 1 | Cumprido | Gráficos e tabelas no notebook 01. |
| Pearson e Spearman | Sim, p. 1 | Cumprido | Matrizes e interpretação no notebook 01. |
| Data Cleaning e Missing Values | Sim, p. 2 | Cumprido | Notebook 02; src/dados.py e src/preparacao.py; testes de dados e ausências. |
| Outliers | Sim, p. 2 | Cumprido | Critério quantitativo de 1,5 × IQR no notebook 01; ausência de remoção automática justificada. |
| Splitting Data | Sim, p. 2 | Cumprido | Divisão por utilizador, conjuntos disjuntos, semente e testes. |
| Feature Scaling | Sim, p. 2 | Cumprido | StandardScaler dentro da Pipeline e dentro dos folds. |
| Imbalanced Data | Sim, p. 2 | Cumprido | Referências, métricas da classe positiva e experiências com pesos/priors; distribuição do teste preservada. |
| Feature Selection, Engineering e Extraction | Sem M, p. 2 | Cumprido | Lista permitida, exclusões justificadas e contexto temporal cíclico. |
| Supervised Learning / Classification | Sim, p. 2 | Cumprido | Oito classificadores e duas referências no notebook 03. |
| Introdução à regressão linear | Sim, p. 3 | Cumprido como enquadramento | docs/fundamentos.md; implementação de regressão não aplicável ao alvo binário. |
| Regressão logística | Introdução marcada M, p. 3 | Cumprido | Experiência, parâmetros, regularização e otimização. |
| Árvores e tipos de algoritmos | Introdução e tipos marcados M, p. 3 | Cumprido | CART implementado; ID3/C4.5/CART enquadrados no notebook 03 e fundamentos. |
| KNN, Naïve Bayes e SVM | Introduções marcadas M, p. 4 | Cumprido | Experiências individuais, hipóteses e limitações no notebook 03. |
| Ensemble Learning, Gradient Boosting e XGBoost | Sim, p. 4 | Cumprido | Bagging e boosting explicados; Random Forest, Gradient Boosting e XGBoost executados. |
| Random Forest Classifier | Sim, p. 4 | Cumprido | Experiência e comparação treino/validação. |
| Matriz de confusão; Precision, Recall e F1 | Sim, p. 5 | Cumprido | src/avaliacao.py, notebook 04, gráficos e testes com contagens conhecidas. |
| AUC-ROC | Sim, p. 5 | Cumprido | Pontuações adequadas, métricas e curvas no teste. |
| Overfitting e Underfitting | Sim, p. 5 | Cumprido | Comparação treino/CV/validação e interpretação sem atribuir causas não demonstradas. |
| Hyperparameter Tuning | Sim, p. 5 | Cumprido | 42 configurações, 210 ajustes, limiar dentro dos folds e decisão congelada antes do teste. |
| Cross-validation, regularização e Model Selection | Sem M, p. 5 | Cumprido | Cinco folds por utilizador, controlo de complexidade e seleção por F1/simplicidade. |
| Métricas e modelos de regressão | Sem M, pp. 2–5 | Não aplicável | Não existe alvo contínuo; não se aplica MAE/RMSE à classificação binária. |
| Probabilidade e estatística de base | Consulta opcional, p. 1 | Não aplicável como entrega separada | Conceitos necessários explicados; não foi inventado um módulo obrigatório adicional. |
| User stories, product/sprint backlog e responsabilidades | Instruções da aula de 21/09, p. 1 | Parcialmente cumprido | Proposta local da parte de Luís em backlog_e_sprints.md; falta validar o plano do grupo e consultar Projects com permissão adequada. |
| Daily, Sprint Review e Retrospective | Instruções das pp. 1–2 | Pendente de evidência real | Modelos de registo definidos; não se inventaram reuniões, participantes ou decisões. |
| Trabalho individual por branches | Instrução da p. 1 | Cumprido nesta parte | Alterações apenas em Forensic-Dataset-Luis-Peneda, sem merge ou alteração das branches dos colegas. |
| Canvas: previsão local em batch | Compromisso do Canvas, p. 1 | Cumprido como demonstração | src/previsoes.py, exemplo e testes; limitação prática explícita. |
| Canvas: impacto, métricas e decisões | Compromissos das pp. 1–2 | Cumprido no âmbito académico | Erros e limitações discutidos; sem custos financeiros inventados. Responsável nominal, capacidade e limiares operacionais continuam por definir para eventual produção. |
| Produção, atualização contínua e eficácia real | Não exigidas para esta entrega | Não aplicável | Fora do âmbito atual; dados e decisões operacionais adicionais seriam necessários. |

«Cumprido» significa que há evidência técnica ou conceptual correspondente neste projeto, não uma classificação atribuída pelo docente. A organização efetiva do grupo e os registos SCRUM exigem confirmação humana. Não se afirma que conteúdos opcionais como AdaBoost, todas as variantes de Naïve Bayes ou todas as técnicas de EDA avançada tenham sido implementados.
