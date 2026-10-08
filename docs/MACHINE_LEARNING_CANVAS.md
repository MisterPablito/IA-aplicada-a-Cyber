# Machine Learning Canvas — componente individual

**Responsável:** Guilherme Jesus  
**Data de referência do roadmap:** 18/09/2026  
**Problema:** classificar registos de tráfego como Normal, DDoS, PortScan ou BruteForce.

## Tarefa de previsão

A unidade de previsão é um registo do dataset. O alvo é `attack_type`; os atributos disponíveis são `duration`, `src_bytes`, `dst_bytes`, `packet_count`, `protocol` e `failed_logins`.

## Utilizador e decisão

A classificação pode apoiar a análise académica de registos de tráfego. Uma equipa de segurança poderia investigar previsões suspeitas, mas este projeto não define limiar de alerta, custos de erro nem capacidade de resposta operacional.

## Dados

Usei o dataset *Cyber Security Attack Using Network Traffic*, obtido no Kaggle. A cópia local tem 100.000 linhas, sete colunas e quatro classes. Não confirmei a metodologia de geração nem a representatividade dos registos para tráfego real.

## Âmbito implementado

Implementei EDA, preparação tabular, comparação de classificadores e avaliação num conjunto de teste retido. O modelo é executado localmente sobre um CSV.

## Hipóteses para trabalho futuro

Deteção em tempo real, integração com um sistema de monitorização, alertas contínuos e atualização com dados novos são possibilidades descritas neste Canvas, não funcionalidades implementadas. Antes de as considerar, seria necessário validar o modelo com uma fonte independente e definir requisitos operacionais.
