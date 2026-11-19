# Âmbito do projeto e critérios de sucesso

## 1. Contexto e referências

Este projeto integra a unidade curricular de IA Aplicada à Cibersegurança do CTeSP de Cibersegurança do ISTEC Porto. Aproveita o dataset e a análise exploratória já existentes; este documento estabelece o enquadramento da continuação do trabalho.

As referências académicas são o **Machine Learning Canvas**, de 30/09/2026, iteração 1, e o **IAAC - Roadmap**, fornecidos para o projeto. Os PDF encontram-se fora do repositório. No Roadmap, `M` significa *Minimum to Apply*: os conteúdos assinalados têm prioridade, distinguindo o seu enquadramento teórico da implementação que se adequa ao problema.

Este documento define objetivos e critérios. Não constitui evidência de que a preparação, os modelos ou a avaliação final já estejam implementados.

## 2. Problema e tarefa de aprendizagem

Os analistas de cibersegurança e as equipas de resposta a incidentes precisam de identificar atividades que mereçam investigação. Pretende-se estudar se as características de um registo permitem distinguir atividades normais de atividades potencialmente suspeitas.

A tarefa é de **classificação binária supervisionada**, com `Label` como variável alvo:

| Rótulo | Representação numérica do alvo | Papel na avaliação |
| --- | --- | --- |
| `Normal` | `0` | Classe negativa |
| `Suspicious` | `1` | Classe positiva |

A unidade de previsão é um registo de atividade do dataset. Uma previsão `Suspicious` é um sinal para análise humana: **não confirma um ataque, um incidente ou a sua gravidade**. Vários registos podem pertencer ao mesmo utilizador ou acontecimento; não se assume que cada linha represente um incidente independente.

O objetivo experimental é determinar se os classificadores identificam padrões que generalizam para registos não utilizados no treino, sem receber informação que revele antecipadamente o alvo. A utilidade será avaliada relativamente a referências simples, admitindo explicitamente a possibilidade de não existir melhoria demonstrável.

## 3. Utilização prevista e limites do âmbito

De acordo com o Canvas, as previsões serão produzidas **localmente e em batch**, com Python e bibliotecas de aprendizagem automática. O trabalho será explicado através de notebooks, gráficos, métricas e conclusões reproduzíveis.

Num cenário de utilização, um analista de cibersegurança ou uma equipa de resposta a incidentes analisaria os registos sinalizados e decidiria se é necessária investigação. Não estão definidos um responsável nominal, a capacidade diária de análise, a frequência das previsões, a latência admissível ou os custos financeiros dos erros. Estes valores não serão inventados.

O âmbito compreende a consolidação da EDA existente, a preparação dos dados, referências simples, classificadores adequados, comparação, otimização, avaliação final e demonstração de previsões batch, acompanhadas das respetivas limitações.

Não se prevê desenvolver uma aplicação web, API, base de dados externa ou infraestrutura de produção. O CSV é estático e o Canvas não define atualização contínua dos dados ou dos modelos. Também não se prevê bloquear automaticamente utilizadores ou atividades com base nas previsões.

## 4. Dados disponíveis e limitações conhecidas

O ficheiro original é [`data/raw/cybercrime_forensic_dataset.csv`](../data/raw/cybercrime_forensic_dataset.csv). A análise existente está em [`notebooks/01_data_understanding.ipynb`](../notebooks/01_data_understanding.ipynb).

| Característica | Situação observada no CSV |
| --- | --- |
| Dimensão | 7 400 registos e 11 colunas |
| Intervalo temporal | 12/09/2024 a 12/10/2024 |
| Classe `Normal` | 6 167 registos, aproximadamente 83,3% |
| Classe `Suspicious` | 1 233 registos, aproximadamente 16,7% |
| Duplicados completos | Nenhum identificado |
| Valores ausentes | Concentrados em `Login_Attempts`, `File_Size` e `File_Name`; a ausência observada depende do tipo de atividade |

Os rótulos estão disponíveis no CSV histórico, mas o processo de anotação, a sua validação e o intervalo entre atividade e confirmação do resultado não estão confirmados. Não se assume que um rótulo do dataset corresponda a um incidente confirmado em ambiente real.

A descrição oficial do autor no Kaggle, consultada posteriormente ao diagnóstico inicial, identifica observações simuladas; a fonte e as dúvidas remanescentes estão em [Proveniência e dicionário dos dados](dados.md). Os padrões e os rótulos podem refletir o mecanismo de geração e não o comportamento de uma rede real. A origem simulada não demonstra, por si só, que as variáveis tenham sido geradas de forma independente.

As análises realizadas ainda não demonstram uma separação clara das classes pelas características admissíveis. Correlação linear ou monótona reduzida não exclui relações não lineares ou interações. A capacidade preditiva terá de ser medida por experiências comparáveis, sem prometer antecipadamente desempenho elevado.

## 5. Prevenção de fuga de informação

No CSV analisado, `Anomaly_Type = "None"` corresponde sempre a `Normal` e os restantes valores correspondem sempre a `Suspicious`. Por esse motivo, **`Anomaly_Type` será excluída das entradas do classificador principal**. A correspondência observada não demonstra que esta informação estaria disponível de forma independente no momento da previsão.

`Label` será utilizado apenas como alvo. A coluna `Label_bin`, criada na EDA, é uma representação direta desse alvo e também não poderá integrar as entradas.

Na implementação seguinte, as características serão selecionadas explicitamente e será verificada programaticamente a exclusão de `Label`, `Label_bin` e `Anomaly_Type`. O CSV original será preservado.

A disponibilidade das restantes características no momento da previsão terá de ser justificada. Identificadores como `User_ID` e `IP_Address` exigem análise do risco de memorização; a sua exclusão ou transformação será documentada. Serão também avaliadas a redundância de `Resource_Accessed` e `File_Name` e a relação entre registos do mesmo utilizador ou período.

Qualquer transformação que aprenda parâmetros será ajustada apenas ao treino. Durante a validação cruzada, esse ajuste ocorrerá dentro de cada divisão. Eventual reamostragem será limitada ao treino, mantendo a distribuição natural do teste.

## 6. Protocolo de comparação previsto

Antes do treino, será escolhida e documentada a estratégia de divisão. A seleção entre divisão estratificada, temporal ou por utilizador dependerá da generalização pretendida e das relações entre registos. Esta decisão pertence à fase de preparação e não fica antecipadamente fixada neste documento.

Será reservado um conjunto de teste final. A comparação de algoritmos, o ajuste de hiperparâmetros e eventual escolha do limiar de decisão utilizarão exclusivamente os dados de desenvolvimento, através de validação ou validação cruzada adequadas à divisão escolhida.

O dataset completo já foi explorado na EDA. Esta utilização limita a independência absoluta de um teste reservado posteriormente e será declarada nos resultados. Depois de definido, o teste ficará fora das decisões de desenvolvimento; os seus resultados não serão usados para voltar a escolher ou otimizar o modelo.

Todos os candidatos serão comparados com as mesmas divisões, classe positiva, métricas e regras de avaliação. Serão utilizadas sementes fixas quando aplicável e serão registados os parâmetros relevantes.

As referências previstas são prever sempre a classe maioritária e prever sempre `Suspicious`. A primeira pode obter aproximadamente 83,3% de accuracy neste CSV sem detetar qualquer atividade suspeita. A segunda deteta todos os registos suspeitos, mas sinaliza também todos os registos normais. Estas observações descrevem regras simples sobre a distribuição conhecida; não são resultados de modelos já treinados ou do futuro teste final.

## 7. Métricas e critérios de seleção

| Medida | Interpretação e utilização |
| --- | --- |
| F1 de `Suspicious` | Critério principal de comparação na validação, combinando Precision e Recall. Não representa custos financeiros nem resolve, por si só, as prioridades operacionais. |
| Precision de `Suspicious` | Proporção de previsões suspeitas que corresponde a rótulos suspeitos; ajuda a avaliar a qualidade dos alertas. |
| Recall de `Suspicious` | Proporção dos registos suspeitos identificados; permite analisar atividades suspeitas não detetadas. |
| Matriz de confusão | Apresenta as contagens de acertos, falsos positivos e falsos negativos, com identificação explícita das classes. |
| Accuracy | Métrica secundária, apresentada juntamente com as anteriores devido ao desequilíbrio das classes. |
| ROC-AUC | Avalia a ordenação entre classes através de diferentes limiares, quando existem pontuações adequadas e ambas as classes no conjunto avaliado. |
| Curva Precision–Recall e Average Precision | Complementam a avaliação da classe minoritária; Average Precision será o critério secundário de comparação. |

Os **falsos positivos** podem aumentar o trabalho de investigação e a fadiga de alertas. Os **falsos negativos** representam atividades suspeitas que deixam de ser sinalizadas. Nenhum destes efeitos será convertido em custos monetários sem dados que o sustentem.

A seleção principal será baseada no F1 de `Suspicious` em validação, acompanhada da Precision, Recall, Average Precision e contagens de erros. Se a comparação recorrer a validação cruzada, serão apresentadas a média e a variabilidade dos resultados. Não será declarada superioridade robusta a partir de uma diferença isolada ou mínima.

Entre candidatos sem vantagem consistente demonstrável, será preferida a solução mais simples e reproduzível, justificando a decisão. Qualquer ajuste do limiar será realizado nos dados de desenvolvimento e fixado antes da avaliação final. Não serão definidas metas arbitrárias de desempenho ou garantias de eficácia.

## 8. Critérios de sucesso do trabalho académico

O trabalho será considerado metodologicamente concluído quando apresentar evidência verificável dos seguintes pontos:

1. **Compreensão dos dados:** EDA preservada e consolidada, com validações explícitas, visualizações e conclusões proporcionais à evidência.
2. **Preparação correta:** tratamento justificado de ausências e características, preservação do CSV original e exclusão programaticamente verificada das variáveis que revelam o alvo.
3. **Avaliação comparável:** referências simples e classificadores adequados avaliados pelo mesmo protocolo, sem ajustar transformações com o teste.
4. **Generalização analisada:** comparação entre treino e validação, discussão de sobreajustamento ou desempenho insuficiente, e otimização limitada ao desenvolvimento.
5. **Teste final separado:** avaliação do candidato previamente selecionado, incluindo as métricas aplicáveis, falsos positivos e falsos negativos e comparação com as referências.
6. **Resultados honestos:** declarar se existe ou não evidência de melhoria sobre as referências; a ausência de melhoria não será ocultada nem corrigida através de fuga de informação.
7. **Reprodutibilidade:** dependências verificadas, caminhos portáveis, notebooks executáveis pela ordem documentada e demonstração de previsões batch, caso seja selecionado um modelo experimental.
8. **Comunicação académica:** explicações em português de Portugal, relação com os conteúdos aplicáveis do Roadmap e histórico Git que permita acompanhar as alterações validadas.

Concluir corretamente estas etapas não significa obter um sistema adequado a produção. Uma melhoria experimental terá de ser interpretada segundo a variabilidade observada, as limitações do teste e a representatividade dos dados.

## 9. Condições para utilização fora do contexto académico

Uma eventual aplicação real exigiria dados representativos e autorizados, validação da origem e qualidade dos rótulos, confirmação da disponibilidade das entradas, avaliação temporal e em utilizadores ou ambientes não observados e análise de eventos independentes.

Seria ainda necessário definir um responsável pelas decisões, capacidade de análise dos alertas, prioridades entre erros, limiar operacional, requisitos de privacidade e segurança e acompanhamento periódico do desempenho. Caso as ações desencadeadas pelos alertas alterassem os resultados observados, seria necessário avaliar esse efeito na recolha de novos rótulos.

Os resultados deste projeto, sobretudo se obtidos em dados sintéticos, não constituirão garantia de deteção de ameaças numa rede real.
