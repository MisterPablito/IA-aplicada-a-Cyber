# Ambiente de execução

O ambiente de referência é Windows 11 com Python 3.14. As versões efetivamente verificadas estão em `requirements.txt`; `requirements-lock.txt` fixa também as dependências transitivas observadas neste ambiente. Estes ficheiros não incluem o ambiente virtual.

Na raiz do projeto, em PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-lock.txt
.\.venv\Scripts\python.exe -m pip check
```

No VS Code, selecionar `.venv\Scripts\python.exe` como interpretador e kernel dos notebooks. Não é necessário instalar um kernel global. As extensões Python e Jupyter pertencem ao VS Code e não são instaladas pelo `requirements.txt`.

Para validar um notebook num kernel novo, a partir da raiz:

```powershell
.\.venv\Scripts\python.exe scripts/executar_notebooks.py notebooks/01_data_understanding.ipynb
```

Por omissão, a execução não altera o ficheiro. Acrescentar `--gravar` apenas quando se pretende atualizar as saídas reais. Uma célula com erro interrompe a execução. As configurações temporárias ficam dentro da pasta ignorada `.venv/runtime/`.

Bibliotecas: pandas e NumPy para dados; matplotlib e seaborn para visualização; scikit-learn para preparação, modelos e avaliação; XGBoost para a abordagem de boosting referida no Roadmap; nbformat, nbclient e ipykernel para validação dos notebooks. Os testes utilizarão `unittest`, da biblioteca padrão.

Na sessão de desenvolvimento, uma falha de rede interrompeu a primeira instalação. Uma etapa intermédia reutilizou pacotes do sistema, sem os alterar. Depois foram instaladas localmente as 54 dependências fixadas e desativado o acesso aos pacotes globais. Foi confirmado que todas as distribuições do ficheiro de versões estão dentro da `.venv`, que as versões coincidem e que `pip check` não identifica incompatibilidades. A EDA original foi executada num kernel novo neste ambiente independente.
