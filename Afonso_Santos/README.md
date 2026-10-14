O que foi feito

data_preparation.py: limpeza (verificação de nulos/duplicados), encoding
one-hot de Protocol, standardização das 4 variáveis numéricas, e split
70/15/15 estratificado em treino/validação/teste.
model_comparison.py: compara Regressão Logística, Random Forest e
HistGradientBoosting (todos com class_weight="balanced") no conjunto
de validação.
Decisões principais

Outliers não removidos: em Packet_Size_Bytes, Failed_Logins e
Geo_Distance_km, a maioria dos "outliers" (critério IQR) são as
próprias ligações maliciosas — é sinal, não ruído.
Sem SMOTE/undersampling para já; a separação entre classes já é forte
e o desequilíbrio é tratado com class_weight="balanced".
Conjunto de teste não foi tocado nesta fase — fica reservado para a
avaliação final.
Resultados (conjunto de validação, 3750 linhas, 187 maliciosos)

Modelo	PR-AUC	ROC-AUC
Regressão logística	0.920	0.960
Random Forest	0.923	0.966
HistGradientBoosting	0.919	0.957
Os três ficam muito próximos. Random Forest ligeiramente à frente,
mas a diferença é pequena.

Como correr:
1- cd .\Afonso_Santos\ (para entrar dentro da pasta da database)
2- .\venv\Scripts\Activate.ps1 (para ativar a venv para que se possa usar o Python e as bibliotecas isoladas desse projeto específico.)
3- pip install -r requirements.txt (para instalar as bibliotecas necessarias para o projeto funcionar)
4- python data_preparation.py (gera prepared/)
5- python model_comparison.py (lê prepared/, gera prepared/model_comparison_val.csv)