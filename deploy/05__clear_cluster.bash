az account set --subscription eec443ab-c101-4d83-a612-ec3f87c7fb59
az aks get-credentials --resource-group AirflowK8s --name AirflowK8sTest
kubectl create namespace airflow-test
kubectl config set-context --current --namespace=airflow-test

kubectl delete --all --namespace airflow-test deployments
kubectl delete --all --namespace airflow-test persistentvolumeclaims
kubectl delete --all --namespace airflow-test persistentvolumes
kubectl delete --all --namespace airflow-test services
