# Sprints — componente de ciberataques

**Responsável:** Guilherme Jesus  
**Âmbito:** componente individual do dataset de ciberataques.

Este plano organiza o trabalho concluído segundo as fases do roadmap. Não é uma ata de Sprint Planning, Daily Scrum, Review ou Retrospective; não realizámos formalmente essas cerimónias.

## Sprint 1 — Business e Data Understanding

**Objetivo:** compreender o problema, as classes e a estrutura do dataset.

| Tarefa | Estado | Evidência |
|---|---|---|
| Identificar alvo e classes | Concluída | `docs/MACHINE_LEARNING_CANVAS.md` |
| Verificar dimensão, tipos, nulos e duplicados | Concluída | `iaac_minimum_apply.py`, `docs/resultado_treino.txt` |
| Explorar distribuições e correlações | Concluída | `resultados/graficos/eda_*.png` |

## Sprint 2 — Data Preparation

**Objetivo:** preparar treino e teste sem ajustar transformações ao teste.

| Tarefa | Estado | Evidência |
|---|---|---|
| Remover duplicados na cópia em memória | Concluída | `iaac_minimum_apply.py` |
| Dividir dados de forma estratificada | Concluída | `iaac_minimum_apply.py`, `resultados/resumo_resultados.json` |
| Aplicar encoding e scaling em pipeline | Concluída | `iaac_minimum_apply.py` |

## Sprint 3 — Supervised Learning e Evaluation

**Objetivo:** comparar classificadores, escolher um candidato e avaliar no teste retido.

| Tarefa | Estado | Evidência |
|---|---|---|
| Comparar classificadores por validação cruzada | Concluída | `docs/COMPARACAO_MODELOS.md`, `docs/RESULTADOS.md` |
| Ajustar uma árvore apenas com dados de treino | Concluída | `iaac_minimum_apply.py` |
| Avaliar o modelo final e documentar limitações | Concluída | `docs/RESULTADOS.md`, `resultados/` |

## Templates para registos futuros

Preencher estes modelos apenas quando as reuniões ocorrerem; não criar atas retroativas.

### Daily Scrum

**Data:** ____  **Participantes:** ____

| Elemento | Desde a última reunião | Próxima tarefa | Bloqueio |
|---|---|---|---|
| ____ | ____ | ____ | ____ |

### Review e Retrospective

**Data / sprint:** ____

- Trabalho demonstrado e feedback real:
- O que correu bem ou foi difícil:
- Próxima ação, responsável e prazo:
