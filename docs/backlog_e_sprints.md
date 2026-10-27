# Backlog e proposta de sprints — Cybercrime Forensic Dataset

## Consulta do GitHub

Consulta de leitura efetuada em 27/10/2026 ao repositório `MisterPablito/IA-aplicada-a-Cyber`:

- A API de Issues devolveu apenas o [pull request #1, «Data preparation e comparação de modelos - Afonso Santos»](https://github.com/MisterPablito/IA-aplicada-a-Cyber/pull/1), aberto e sem responsáveis atribuídos. Um pull request não constitui, por si só, um backlog de user stories.
- Não foram devolvidas Issues independentes nem milestones.
- A consulta dos Projects V2 foi recusada por falta do âmbito de leitura `read:project`. Não é possível concluir se existem quadros ou tarefas nessa área. Não foram alteradas permissões da conta.
- Não foram criadas ou alteradas Issues, Projects, pull requests ou tarefas de colegas.

Este documento é uma proposta local para a parte de Luís Peneda, na branch `Forensic-Dataset-Luis-Peneda`. Não representa aprovação de um plano pelo grupo nem substitui eventuais registos externos que não foi possível consultar.

## Product backlog

| ID | User story | Critérios de aceitação | Dependência |
| --- | --- | --- | --- |
| LP-01 | Como aluno, quero explicitar o problema e a avaliação para defender o objetivo do projeto. | Âmbito, classe positiva, métricas e limitações documentados. Concluída no commit `5e4c5a5`. | — |
| LP-02 | Como aluno, quero organizar o trabalho para acompanhar requisitos e progresso. | Backlog local, dependências, proposta de sprints e limitações da consulta ao GitHub documentados. | LP-01 |
| LP-03 | Como revisor, quero reproduzir o ambiente e compreender os dados. | Dependências instaláveis e verificadas, instruções e dicionário com dúvidas explícitas. | LP-01 |
| LP-04 | Como analista, quero uma EDA verificável para justificar a preparação. | Duplicados e outliers demonstrados, conclusões revistas e notebook executado sem erros. | LP-03 |
| LP-05 | Como investigador, quero separar desenvolvimento e teste sem revelar o alvo. | Divisão justificada e reproduzível, sem sobreposição; características permitidas explícitas; transformações ajustadas apenas no treino. | LP-04 |
| LP-06 | Como investigador, quero referências simples para reconhecer melhorias reais. | Referências maioritária e sempre suspeita; métricas corretas para a classe positiva. | LP-05 |
| LP-07 | Como aluno, quero comparar classificadores relevantes para cobrir as abordagens da disciplina. | Experiências separadas, explicações, mesmo protocolo de validação e comparação treino/validação. | LP-06 |
| LP-08 | Como investigador, quero otimizar candidatos sem utilizar o teste. | Pesquisa limitada, validação cruzada adequada, limiar escolhido no desenvolvimento e decisão registada antes do teste. | LP-07 |
| LP-09 | Como revisor, quero conhecer o desempenho final e os erros. | Teste reservado, matriz de confusão, métricas e interpretação de falsos positivos e negativos. | LP-08 |
| LP-10 | Como utilizador académico, quero produzir previsões batch reproduzíveis. | Exemplo compatível, validação das entradas, sem campos que revelem o alvo e limitações explícitas. | LP-09 |
| LP-11 | Como professor, quero localizar evidências dos requisitos e reproduzir o trabalho. | README, resultados, mapa do Roadmap e registo de validações e commits. | LP-10 |

Responsabilidade proposta: Luís Peneda, exclusivamente para a sua parte. Não são atribuídas tarefas aos restantes elementos. O estado efetivo de cada implementação deve ser confirmado no histórico Git e no relatório final, não inferido da simples existência desta lista.

## Proposta de sprint backlog

| Sprint proposto | Histórias | Resultado esperado |
| --- | --- | --- |
| A — Consolidação | LP-02, LP-03, LP-04 | Organização, ambiente reproduzível e EDA consolidada. |
| B — Preparação e referências | LP-05, LP-06 | Divisão congelada, preparação sem fuga de informação e métricas comuns. |
| C — Modelação | LP-07 | Experiências comparáveis, com commits por alteração lógica. |
| D — Avaliação e entrega | LP-08, LP-09, LP-10, LP-11 | Otimização, teste final, previsões e documentação. |

Esta sequência exprime dependências técnicas. Não atribui datas letivas, duração ou reuniões realizadas. O Roadmap prevê Review e Retrospective a cada duas aulas; a sua calendarização real cabe ao grupo e ao docente.

## Registos SCRUM a preencher com acontecimentos reais

**Daily Scrum:** data, participantes reais, trabalho concluído desde a reunião anterior, próximo trabalho e impedimentos. Não existem reuniões registadas neste documento.

**Sprint Review:** data, participantes, histórias demonstradas, evidências de aceitação e feedback efetivamente recebido. A execução automática de testes não equivale a uma Review do grupo.

**Sprint Retrospective:** data, participantes, aspetos que funcionaram, dificuldades observadas e ações acordadas. Não foram inventadas decisões ou conclusões de reuniões.

O histórico de commits documenta progresso técnico. Os eventos SCRUM permanecem pendentes de realização ou de disponibilização dos seus registos reais.
