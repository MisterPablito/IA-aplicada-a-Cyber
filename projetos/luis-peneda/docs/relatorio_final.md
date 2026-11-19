# Relatório final — IA Aplicada à Cibersegurança

## 1. Estado inicial e âmbito preservado

O trabalho foi continuado na branch Forensic-Dataset-Luis-Peneda, a partir do enquadramento aprovado no commit 5e4c5a5. Existiam o CSV original, .gitignore, README breve e uma EDA substancial. Não existiam nesta branch preparação consolidada, modelos ou avaliação final.

O dataset e o histórico anterior foram preservados. Não foram feitos merges, force push ou alterações nas branches dos colegas. O trabalho do Afonso usa outro dataset e permaneceu separado.

## 2. Trabalho realizado

- Consulta de Issues, milestones e tentativa de leitura de Projects no GitHub; proposta local de backlog e sprints sem reuniões inventadas.
- Confirmação dos metadados oficiais do Kaggle: observações simuladas e licença MIT declarada para o dataset.
- Ambiente independente com Python 3.14.8, 54 versões fixadas, verificação de compatibilidade e executador de notebooks.
- EDA consolidada com duplicados, IQR, conclusão prudente e explicação da informação que revela o alvo.
- Divisão reproduzível por utilizador: 4 416 registos de treino, 1 478 de validação e 1 506 de teste, sem utilizadores ou linhas comuns.
- Lista explícita de entradas, ausências estruturais, variáveis temporais cíclicas, codificação e escala dentro de cada fold.
- Duas referências e oito classificadores, com explicações e cinco folds por utilizador.
- Otimização conjunta de hiperparâmetros e limiar, com 42 configurações e 210 ajustes, apenas nos folds de treino.
- Decisão congelada e enviada antes do teste; avaliação das referências e da melhor alternativa aprendida.
- Demonstração batch com validação de entradas e artefacto binário local ignorado pelo Git.

A revisão visual identificou substituição de acentos pela consola Windows na geração de texto. A codificação foi corrigida, os notebooks afetados foram reexecutados e foram acrescentados testes para prevenir essa regressão. Os gráficos originais da EDA e as métricas foram preservados.

## 3. Ficheiros e finalidade

| Ficheiros | Finalidade |
| --- | --- |
| notebooks/01_data_understanding.ipynb | Consolidação da EDA existente, preservando os gráficos. |
| notebooks/02_data_preparation.ipynb | Validação, divisão e demonstração da preparação. |
| notebooks/03_model_comparison.ipynb | Referências e experiências individuais dos classificadores. |
| notebooks/04_model_evaluation.ipynb | Comparação, otimização registada, teste e batch. |
| src/dados.py e src/preparacao.py | Integridade, grupos, lista permitida e Pipeline. |
| src/avaliacao.py e src/experiencias.py | Métricas e protocolo comparável. |
| src/otimizacao.py e src/avaliacao_final.py | Pesquisa e proteção da decisão anterior ao teste. |
| src/previsoes.py e exemplos/ | Treino local, carregamento e previsão de CSV compatível. |
| tests/ | Vinte testes de dados, protocolo, métricas, decisão, codificação e serialização. |
| scripts/executar_notebooks.py | Kernel novo, falha em erros e gravação opcional de saídas reais. |
| resultados/ | Métricas pequenas, decisão assinada e gráficos de apresentação. |
| requirements.txt, requirements-lock.txt e docs/ambiente.md | Ambiente e instruções de reprodução. |
| README.md e docs/ | Enquadramento, dicionário, organização, fundamentos, requisitos e relatório. |
| .gitignore | Preserva exclusões existentes e ignora artefactos locais. |

Não foram versionados modelos binários, ambientes virtuais, credenciais ou cópias processadas completas do dataset.

## 4. Validação executada

- Vinte testes unittest passaram: integridade do CSV, categorias None/N/A, divisão e folds sem utilizadores comuns, reprodução, recusa de rótulos inesperados, exclusão e recusa das entradas proibidas, escala e categorias sem aprender na validação, ausências estruturais, contagens de erros, pontuações finitas, regra de simplicidade, limiar, assinatura da decisão, codificação, esquema dos notebooks, serialização e contrato de previsão.
- Os quatro notebooks foram executados integralmente em kernels novos. A EDA tem nove células de código executadas; os gráficos anteriores foram preservados.
- As 54 distribuições fixadas foram verificadas dentro da .venv, com acesso a pacotes globais desativado. pip check não encontrou requisitos incompatíveis.
- A interface de comandos de treino e previsão produziu três previsões reais para o exemplo do treino; o artefacto carregado reproduz o objeto em memória.
- Os gráficos foram revistos visualmente. Diferenças, ficheiros preparados, padrões de credenciais e preservação do SHA-256 original foram verificados antes dos commits.
- Validação integrada final concluída: os quatro notebooks executaram na ordem 01–04 em kernels novos, os vinte testes passaram novamente, pip check passou e foram verificadas vinte ligações locais, a sintaxe Python e a integridade do dataset e da decisão. A reprodução não alterou as métricas registadas.

A execução de testes não é uma Sprint Review nem comprova eficácia operacional. Não foi realizada validação em tráfego real ou em incidentes independentes.

## 5. Resultados de desenvolvimento

A tabela usa métricas da validação separada e a média/desvio do F1 nos cinco folds de treino. Não contém métricas de teste dos oito classificadores iniciais.

| Modelo | F1 CV | Desvio F1 CV | F1 validação | Precision | Recall | Accuracy | ROC-AUC | Average Precision |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| maioritaria | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.8369 | 0.5000 | 0.1631 |
| sempre_suspeita | 0.2850 | 0.0007 | 0.2804 | 0.1631 | 1.0000 | 0.1631 | 0.5000 | 0.1631 |
| logistica | 0.2368 | 0.0104 | 0.2448 | 0.1636 | 0.4855 | 0.5115 | 0.5142 | 0.1671 |
| arvore | 0.2478 | 0.0424 | 0.2819 | 0.1696 | 0.8340 | 0.3072 | 0.5321 | 0.1743 |
| random_forest | 0.2283 | 0.0304 | 0.2169 | 0.1522 | 0.3776 | 0.5555 | 0.4950 | 0.1560 |
| knn | 0.0027 | 0.0060 | 0.0000 | 0.0000 | 0.0000 | 0.8363 | 0.4984 | 0.1685 |
| naive_bayes | 0.2463 | 0.0100 | 0.2522 | 0.1646 | 0.5394 | 0.4783 | 0.5060 | 0.1766 |
| svm | 0.2402 | 0.0350 | 0.2101 | 0.1496 | 0.3527 | 0.5677 | 0.4868 | 0.1574 |
| gradient_boosting | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.8363 | 0.5056 | 0.1581 |
| xgboost | 0.2394 | 0.0240 | 0.2581 | 0.1693 | 0.5436 | 0.4905 | 0.4972 | 0.1553 |

A maioritária obtém accuracy elevada sem detetar casos suspeitos. Random Forest e SVM mostram diferenças importantes entre treino e avaliação. KNN e Gradient Boosting têm baixa deteção de positivos com as opções iniciais. As hipóteses de pouco sinal, desequilíbrio, limiar e complexidade devem ser distinguidas; as métricas não provam sozinhas a causa.

## 6. Otimização e seleção

Foram pesquisadas logística, árvore e Naïve Bayes. O limiar integra o classificador pesquisado, com valores 0, 0,2 e 0,5, dentro da validação cruzada por utilizador. A validação separada não escolheu limiares.

A logística otimizada usa C=1, pesos balanced e limiar 0,2. F1 CV: 0.285104. A referência sempre suspeita tem F1 CV de 0.285048. A diferença é pequena e a regra de um erro padrão selecionou a referência mais simples.

As configurações e a decisão estão em decisao_modelo.json, enviadas no commit c6f6558 antes da avaliação final. Uma assinatura canónica impede que a avaliação aceite uma decisão diferente silenciosamente. A heurística de simplicidade não é um teste estatístico de equivalência.

## 7. Teste final

O desenvolvimento completo tem 5 894 registos. O teste tem 1 506 registos de 1 007 utilizadores ausentes do desenvolvimento: 1 248 Normal e 258 Suspicious. Os modelos são reajustados no desenvolvimento após fixar a configuração, sem aprender transformações ou parâmetros no teste.

| Modelo | Accuracy | Precision | Recall | F1 | ROC-AUC | Average Precision | FP | FN |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| maioritaria | 0.8287 | 0.0000 | 0.0000 | 0.0000 | 0.5000 | 0.1713 | 0 | 258 |
| sempre_suspeita | 0.1713 | 0.1713 | 1.0000 | 0.2925 | 0.5000 | 0.1713 | 1248 | 0 |
| logistica_otimizada | 0.1713 | 0.1713 | 1.0000 | 0.2925 | 0.5178 | 0.1792 | 1248 | 0 |

Precision zero na maioritária é uma convenção computacional: não existem previsões positivas. A referência selecionada e a logística sinalizam tudo, com 1 248 falsos positivos e zero falsos negativos. A logística fornece pontuações com ROC-AUC 0,5178 e Average Precision 0,1792, próximas das referências neste conjunto, sem demonstração de utilidade suficiente.

O F1 de 0,2925 da regra constante é superior ao seu F1 de validação devido à prevalência positiva diferente, não a uma nova capacidade aprendida. O resultado final não foi utilizado para reescolher modelo ou limiar. As reexecuções posteriores são verificações determinísticas de reprodução da mesma decisão e resultados.

## 8. Utilidade e limitações

Não se recomenda utilização operacional. Sinalizar todas as atividades não reduz o esforço de análise; omitir todas as suspeitas também não resolve o problema. A entrega demonstra o ciclo experimental e a ausência de vantagem útil observada, sem elevar artificialmente os resultados com Anomaly_Type ou Label_bin.

A EDA utilizou o dataset completo antes de reservar o teste. A origem é simulada, o código de geração e a construção dos rótulos não estão confirmados, faltam identificadores de incidente, fuso horário e unidade de File_Size. Separar utilizadores não garante independência de acontecimentos ou generalização para períodos futuros.

A pesquisa limitada não esgota todos os modelos ou parâmetros possíveis, e a comparação de configurações pode introduzir otimismo. Folds e linhas não devem ser confundidos com incidentes independentes. Não foram inventados custos monetários, capacidade de análise, metas de eficácia ou resultados de reuniões.

## 9. Git, requisitos e organização

O registo cronológico de commits e validações está em [registo_desenvolvimento.md](registo_desenvolvimento.md). Cada alteração lógica foi validada, comprometida e enviada para a mesma branch antes da seguinte. O commit de entrega documental completa a lista no próprio histórico Git.

O [mapa do Roadmap e Canvas](requisitos_roadmap.md) distingue conteúdos cumpridos, parciais, não aplicáveis e pendentes. Os [fundamentos](fundamentos.md) enquadram, entre outros, a introdução à regressão linear sem a aplicar indevidamente ao alvo binário.

O backlog e os sprints são propostas locais. As reuniões SCRUM reais e a validação do plano pelo grupo não foram inventadas. Projects V2 não pôde ser consultado com a permissão atual; não se conclui que esteja vazio.

## 10. Próximo passo

A parte técnica está preparada para revisão académica, com uma conclusão de desempenho limitada e explícita. Falta ao grupo confirmar os registos SCRUM reais, eventuais tarefas nos Projects e os critérios de avaliação específicos do docente.

Uma evolução científica exige novos dados representativos e rótulos validados, definição de incidentes e disponibilidade das entradas, teste temporal e validação independente. Não se deve continuar a ajustar esta seleção usando o teste já observado.
