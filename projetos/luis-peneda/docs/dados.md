# Proveniência e dicionário dos dados

## Fonte e integridade

- Dataset: [Cybercrime Forensic Dataset, publicado por jimohyusuf no Kaggle](https://www.kaggle.com/datasets/jimohyusuf/cybercrime-forensic-dataset/data).
- Metadados oficiais consultados em 27/10/2026 através da [API pública do Kaggle](https://www.kaggle.com/api/v1/datasets/view/jimohyusuf/cybercrime-forensic-dataset).
- A descrição do autor identifica **7 400 observações simuladas**. Está confirmada a natureza simulada declarada pela fonte; não está disponível o código de geração que permitiria verificar a independência das variáveis ou a construção dos rótulos.
- Os metadados declaram a licença **MIT** e última atualização em `2024-10-12T14:47:33.877Z`. Esta declaração refere-se ao dataset, não atribui automaticamente uma licença ao código deste repositório.
- Cópia analisada: `data/raw/cybercrime_forensic_dataset.csv`, 853 702 bytes, 7 400 linhas de dados e 11 colunas. A igualdade de tamanho com os metadados não demonstra, por si só, identidade de conteúdo com uma versão remota.
- SHA-256 local: `6f7355d0a563822cd1c8995a2b9a0bb1f9a249b7ee388a4db25c787e5c5c0264`.

O CSV original permanece inalterado. As divisões serão reproduzidas a partir deste ficheiro; não é necessário guardar cópias processadas completas no Git.

## Dicionário observado

| Coluna | Tipo lógico | Conteúdo e decisão prevista |
| --- | --- | --- |
| `Timestamp` | Data/hora | Instante da atividade; derivar hora e dia da semana. Fuso horário não confirmado. |
| `User_ID` | Identificador | 5 031 utilizadores distintos; analisar repetição e risco de memorização antes de decidir a divisão. |
| `IP_Address` | Identificador textual | 7 353 valores distintos; elevada cardinalidade, sem contexto de rede confirmado. |
| `Activity_Type` | Categoria | Sete tipos de atividade; candidato a entrada. |
| `Resource_Accessed` | Categoria textual | 36 caminhos; candidato a entrada, incluindo a informação do recurso. |
| `File_Name` | Categoria textual | Seis nomes não vazios; quando preenchido coincide com o último componente de `Resource_Accessed`. A redundância deve justificar eventual exclusão. |
| `Action` | Categoria | Sete valores, incluindo `N/A`; descreve a ação ou o resultado registado. Só é admissível se conhecido antes da classificação, após o registo da atividade. |
| `Login_Attempts` | Contagem | Valores de 1 a 10; preenchido em `Login` e `Remote_Login`. |
| `File_Size` | Número real | Valores de 0,13 a 49,98; a unidade não é indicada na descrição consultada e não será inventada. |
| `Anomaly_Type` | Categoria de anotação | Correspondência perfeita com `Label`; excluída dos modelos. |
| `Label` | Alvo | `Normal` ou `Suspicious`; classe positiva `Suspicious`. |

O intervalo observado é de `2024-09-12 15:03:38.257277` a `2024-10-12 15:13:36.096647`. Não existem linhas integralmente duplicadas. Contagens: 6 167 `Normal` e 1 233 `Suspicious`.

## Leitura e ausências

A leitura utiliza `keep_default_na=False, na_values=[""]`. Assim, apenas campos vazios são considerados ausentes; `None` em `Anomaly_Type` e `N/A` em `Action` permanecem categorias textuais.

| Campo | Ausentes | Interpretação observada |
| --- | ---: | --- |
| `Login_Attempts` | 5 295 | Não preenchido fora das atividades de login. |
| `File_Size` | 4 204 | Preenchido apenas em acesso, eliminação e modificação de ficheiros. |
| `File_Name` | 4 204 | Mesmo padrão estrutural de `File_Size`. |

Campos não aplicáveis não devem levar à eliminação de linhas. Na preparação, o preenchimento numérico com zero pode representar ausência estrutural, pois zero não ocorre nos valores numéricos observados. Uma categoria como `Not_Applicable` é adequada para um campo categórico estruturalmente ausente, se for utilizado. Um valor inesperadamente ausente numa atividade aplicável deve ser distinguido desse caso.

## Limites da interpretação

O projeto classifica registos de atividades concluídas usando os campos do registo disponíveis antes da classificação; não prevê antecipadamente o resultado de uma ação ainda não realizada. A disponibilização de `Action` e dos restantes campos num sistema real teria de ser validada.

A origem simulada não prova independência estatística entre entradas e alvo. Os rótulos não constituem evidência de incidentes reais confirmados. Permanecem desconhecidos o código de geração, a metodologia de anotação, o identificador de incidente, o fuso horário e a unidade de `File_Size`.
