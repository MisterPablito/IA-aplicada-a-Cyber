# Registo de desenvolvimento e validações

Registo em 27/10/2026 da parte de Luís Peneda. Todos os commits abaixo foram enviados com sucesso para origin/Forensic-Dataset-Luis-Peneda. O estado remoto era confirmado antes de cada alteração publicada; não foram usados merges ou force push.

| Commit | Alteração | Validação executada | GitHub |
| --- | --- | --- | --- |
| [5e4c5a5](https://github.com/MisterPablito/IA-aplicada-a-Cyber/commit/5e4c5a5) | docs: define project scope and success criteria | Documento, ligações, contagens do CSV e diferenças Git. | Push concluído |
| [ba85af5](https://github.com/MisterPablito/IA-aplicada-a-Cyber/commit/ba85af5) | docs: add product backlog and proposed sprints | Leitura de Issues/milestones; limitação de Projects documentada; revisão documental. | Push concluído |
| [0735270](https://github.com/MisterPablito/IA-aplicada-a-Cyber/commit/0735270) | docs: verify dataset provenance and document schema | API oficial do Kaggle, esquema, redundância e SHA-256 do CSV. | Push concluído |
| [662e8aa](https://github.com/MisterPablito/IA-aplicada-a-Cyber/commit/662e8aa) | chore: verify and document reproducible Python environment | 54 versões locais verificadas, pip check e execução integral da EDA. | Push concluído |
| [aa3d312](https://github.com/MisterPablito/IA-aplicada-a-Cyber/commit/aa3d312) | analysis: validate and refine exploratory conclusions | EDA integral com nove células; IQR e duplicados; gráficos preservados. | Push concluído |
| [10e26b1](https://github.com/MisterPablito/IA-aplicada-a-Cyber/commit/10e26b1) | feat: split development and test data by user | Quatro testes e notebook 02 integral; grupos e linhas disjuntos. | Push concluído |
| [f9412f0](https://github.com/MisterPablito/IA-aplicada-a-Cyber/commit/f9412f0) | feat: add leakage-safe preprocessing pipeline | Oito testes e notebook 02 integral; entradas proibidas e aprendizagem das transformações. | Push concluído |
| [d36c92f](https://github.com/MisterPablito/IA-aplicada-a-Cyber/commit/d36c92f) | feat: add baseline classifiers and grouped evaluation | Doze testes e notebook 03 integral; referências e métricas. | Push concluído |
| [d033395](https://github.com/MisterPablito/IA-aplicada-a-Cyber/commit/d033395) | model: add logistic regression experiment | Notebook 03 integral: cinco folds por utilizador, previsões, pontuações, contagens e métricas finitas; apenas desenvolvimento. | Push concluído |
| [35a9857](https://github.com/MisterPablito/IA-aplicada-a-Cyber/commit/35a9857) | model: add decision tree experiment | Notebook 03 integral: cinco folds por utilizador, previsões, pontuações, contagens e métricas finitas; apenas desenvolvimento. | Push concluído |
| [0316900](https://github.com/MisterPablito/IA-aplicada-a-Cyber/commit/0316900) | model: add random forest experiment | Notebook 03 integral: cinco folds por utilizador, previsões, pontuações, contagens e métricas finitas; apenas desenvolvimento. | Push concluído |
| [0bd0305](https://github.com/MisterPablito/IA-aplicada-a-Cyber/commit/0bd0305) | model: add nearest neighbors experiment | Notebook 03 integral: cinco folds por utilizador, previsões, pontuações, contagens e métricas finitas; apenas desenvolvimento. | Push concluído |
| [688fafe](https://github.com/MisterPablito/IA-aplicada-a-Cyber/commit/688fafe) | model: add naive Bayes experiment | Notebook 03 integral: cinco folds por utilizador, previsões, pontuações, contagens e métricas finitas; apenas desenvolvimento. | Push concluído |
| [c83d831](https://github.com/MisterPablito/IA-aplicada-a-Cyber/commit/c83d831) | model: add support vector classifier experiment | Notebook 03 integral: cinco folds por utilizador, previsões, pontuações, contagens e métricas finitas; apenas desenvolvimento. | Push concluído |
| [f80a3ff](https://github.com/MisterPablito/IA-aplicada-a-Cyber/commit/f80a3ff) | model: add gradient boosting experiment | Notebook 03 integral: cinco folds por utilizador, previsões, pontuações, contagens e métricas finitas; apenas desenvolvimento. | Push concluído |
| [4bbf6d2](https://github.com/MisterPablito/IA-aplicada-a-Cyber/commit/4bbf6d2) | model: add XGBoost experiment | Notebook 03 integral: cinco folds por utilizador, previsões, pontuações, contagens e métricas finitas; apenas desenvolvimento. | Push concluído |
| [2e19108](https://github.com/MisterPablito/IA-aplicada-a-Cyber/commit/2e19108) | analysis: compare models and define optimization protocol | Doze testes, notebook 04 e gráfico revisto visualmente; protocolo antes da pesquisa. | Push concluído |
| [eaf338a](https://github.com/MisterPablito/IA-aplicada-a-Cyber/commit/eaf338a) | fix: preserve Portuguese text and verify notebook sources | Catorze testes, reexecução dos notebooks 01–03, gráficos e métricas preservados. | Push concluído |
| [c6f6558](https://github.com/MisterPablito/IA-aplicada-a-Cyber/commit/c6f6558) | perf: tune classifiers and freeze decision before final test | Dezasseis testes, notebook 04 e 42 configurações/210 ajustes; decisão sem teste. | Push concluído |
| [96c5406](https://github.com/MisterPablito/IA-aplicada-a-Cyber/commit/96c5406) | analysis: evaluate frozen models on held-out users | Dezassete testes, notebook 04, assinatura e gráficos finais. | Push concluído |
| [595c89d](https://github.com/MisterPablito/IA-aplicada-a-Cyber/commit/595c89d) | feat: add reproducible local batch predictions | Vinte testes, comandos de treino/previsão, notebook 04 e artefactos ignorados. | Push concluído |

O commit que adiciona este relatório e o README final é posterior a este retrato do histórico; o seu identificador encontra-se no git log e no relatório entregue na conversa. Esta indicação evita inventar um identificador ou criar um commit vazio para referenciar o próprio commit.

Validação integrada de entrega concluída antes do commit documental: notebooks 01–04 em kernels novos e pela ordem correta; vinte testes aprovados; pip check sem incompatibilidades; vinte ligações locais e sintaxe Python verificadas; dataset e decisão íntegros; métricas reproduzidas sem alterações. Os registos de reuniões SCRUM permanecem dependentes de acontecimentos reais.
