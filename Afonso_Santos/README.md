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

Como correr
cd .\Afonso_Santos\
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python data_preparation.py (gera prepared/)
python model_comparison.py (lê prepared/, gera
prepared/model_comparison_val.csv)