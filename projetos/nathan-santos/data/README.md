# Dados do projeto

Fonte: [Phishing website Detector — Eswar Chand T — Kaggle](https://www.kaggle.com/datasets/eswarchandt/phishing-website-detector).

O CSV original não está incluído neste pacote. O notebook descarrega-o automaticamente. Para download manual, descarrega o ZIP do Kaggle, extrai `phishing.csv` e coloca-o na pasta de trabalho do notebook; no Colab, carrega-o no painel Ficheiros.

Foi usada a versão 3, consultada em 13/10/2026. O CSV tem 11 054 linhas, 30 características, a coluna `Index` e a resposta `class`. A convenção usada é `class = -1` para phishing e `class = 1` para legítimo. No modelo, a resposta é convertida para `1 = phishing` e `0 = legítimo`.

SHA256 do CSV verificado:

```text
96d48b5c9e957e2dc06f880b2161476da192f814f74332cfd2e3d61a35309dc3
```

As características e respostas correspondem às do [UCI Phishing Websites](https://archive.ics.uci.edu/dataset/327/phishing+websites), depois de excluir a primeira linha do UCI e o índice do CSV. Referência: Mohammad, R. e McCluskey, L., Phishing Websites, DOI 10.24432/C51W2X. Consulta as condições na fonte antes de redistribuir o dataset.
