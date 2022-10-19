# Login at K8s on Azure
az account set --subscription eec443ab-c101-4d83-a612-ec3f87c7fb59
az aks get-credentials --resource-group AirflowK8s --name AirflowK8sTest

# Create and set a default namespace to organize the deploy
kubectl create namespace airflow-test
kubectl config set-context --current --namespace=airflow-test
