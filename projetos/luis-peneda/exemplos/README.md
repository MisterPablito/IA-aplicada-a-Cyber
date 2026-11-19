# Exemplo de previsão batch

`atividades.csv` contém três registos efetivamente extraídos do conjunto de treino, reduzidos às seis entradas permitidas. Não inclui rótulos, anomalias ou identificadores de utilizador. Serve para demonstrar o formato e a execução, não para medir generalização.

Na raiz do projeto, depois de instalar as dependências:

```powershell
.\.venv\Scripts\python.exe -m src.previsoes treinar
.\.venv\Scripts\python.exe -m src.previsoes prever exemplos/atividades.csv --saida artefactos/previsoes.csv
```

O primeiro comando reconstitui a preparação e o modelo selecionado a partir do desenvolvimento. O segundo carrega o artefacto local e preserva a ordem das linhas. Carregar apenas o ficheiro joblib local produzido por este projeto.

Campos: `Timestamp`, `Activity_Type`, `Resource_Accessed`, `Action`, `Login_Attempts` e `File_Size`. Campos vazios são lidos como ausências; `N/A` continua a ser uma categoria. Uma ausência numérica numa atividade aplicável é recusada; a ausência estrutural torna-se zero. Categorias de ação ou recurso não observadas são aceites sem reaprender o codificador.

As previsões são `Normal` ou `Suspicious`. `PontuacaoSuspicious` é a pontuação do modelo, não uma garantia de incidente nem de calibração. A referência selecionada devolve pontuação 1 e sinaliza todas as linhas por definição: isso não representa certeza de ameaça. Os binários e as saídas locais ficam na pasta ignorada `artefactos/`.
