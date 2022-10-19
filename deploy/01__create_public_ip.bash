# Using the same resource group of the K8s cluster
az network public-ip create \
    --resource-group MC_AirflowK8s_AirflowK8sTest_brazilsouth \
    --name api_gateway \
    --sku Standard \
    --allocation-method static
# Ip Created
# 20.197.198.250
