# Backlog — componente de ciberataques

Este backlog cobre apenas a minha componente individual do dataset de ciberataques. Os resultados de outras áreas do grupo ficam fora deste documento.

| ID | User story | Critério de aceitação | Estado |
|---|---|---|---|
| US01 | Como autor, quero compreender o problema e os dados antes de treinar modelos. | Classes, qualidade dos dados e EDA caracterizadas. | Concluída |
| US02 | Como autor, quero preparar os dados sem ajustar transformações ao teste. | Split estratificado e pré-processamento dentro de pipeline. | Concluída |
| US03 | Como autor, quero comparar classificadores com uma métrica adequada às quatro classes. | Baseline e modelos comparados por macro-F1 em validação cruzada. | Concluída |
| US04 | Como autor, quero avaliar o candidato final e registar limitações. | Seleção feita no treino; teste retido e limitações documentados. | Concluída |

## Sprints propostos

| Sprint | Foco | Evidência |
|---|---|---|
| 1 | Business e Data Understanding | EDA e gráficos em `resultados/graficos/`. |
| 2 | Data Preparation | Script e split 80/20 estratificado. |
| 3 | Supervised Learning e Evaluation | Validação cruzada, modelo final e relatório em `docs/RESULTADOS.md`. |

A organização por sprints é uma forma de apresentar o trabalho. Não realizámos cerimónias Scrum formais e não registo atas retroativas.
