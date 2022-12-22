az account set --subscription eec443ab-c101-4d83-a612-ec3f87c7fb59
az aks get-credentials --resource-group AirflowK8s --name AirflowK8sTest

ACR_NAME=airflowk8stest.azurecr.io

# assumes ACR Admin Account is enabled
ACR_UNAME=''
ACR_PASSWD=''

kubectl create namespace pumpwood
kubectl config set-context --current --namespace=pumpwood
kubectl create secret docker-registry dockercfg \
  --docker-server=$ACR_NAME \
  --docker-username=$ACR_UNAME \
  --docker-password=$ACR_PASSWD \
  --docker-email=ignorethis@email.com
