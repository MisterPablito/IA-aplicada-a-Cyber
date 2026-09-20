> Autor da componente: Guilherme Jesus · Turma: 2.º Ciber. Este CSV pertence à componente individual de ciberataques; os resultados referem-se apenas a este dataset. A integração com as restantes áreas do grupo será feita depois.

# Dados do projeto

Usei o ficheiro `cyber_attack_dataset_100000.csv` nesta análise. Tem 100.000 registos originais e 7 colunas: `duration`, `src_bytes`, `dst_bytes`, `packet_count`, `protocol`, `failed_logins` e `attack_type`.

Usei `attack_type` como alvo de classificação. Obtive no Kaggle o dataset Cyber Security Attack Using Network Traffic. Mantive o ficheiro original sem alterações; o script remove uma linha duplicada apenas da cópia carregada em memória para a análise e o treino.




