az disk create \
  --resource-group MC_AirflowK8s_AirflowK8sTest_brazilsouth \
  --name pumpwood--postgres--kong \
  --size-gb 10 \
  --location brazilsouth \
  --zone 1 \
  --query id --output tsv

az disk create \
    --resource-group MC_AirflowK8s_AirflowK8sTest_brazilsouth \
    --name pumpwood--postgres--airflow \
    --size-gb 20 \
    --location brazilsouth \
    --zone 1 \
    --query id --output tsv

az disk create \
    --resource-group MC_AirflowK8s_AirflowK8sTest_brazilsouth \
    --name pumpwood--postgres--auth \
    --size-gb 20 \
    --location brazilsouth \
    --zone 1 \
    --query id --output tsv
