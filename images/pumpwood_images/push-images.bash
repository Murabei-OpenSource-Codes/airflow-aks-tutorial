# API Gateway
docker pull gcr.io/repositorio-geral-170012/pumpwood-nginx-ssl-gateway:0.32
docker tag gcr.io/repositorio-geral-170012/pumpwood-nginx-ssl-gateway:0.32 airflowk8stest.azurecr.io/pumpwood/pumpwood-nginx-ssl-gateway:0.32
docker push airflowk8stest.azurecr.io/pumpwood/pumpwood-nginx-ssl-gateway:0.32

# Auth
docker pull gcr.io/repositorio-geral-170012/pumpwood-auth-app:0.66
docker tag gcr.io/repositorio-geral-170012/pumpwood-auth-app:0.66 airflowk8stest.azurecr.io/pumpwood/pumpwood-auth-app:0.66
docker push airflowk8stest.azurecr.io/pumpwood/pumpwood-auth-app:0.66

docker pull gcr.io/repositorio-geral-170012/pumpwood-auth-static:0.3
docker tag gcr.io/repositorio-geral-170012/pumpwood-auth-static:0.3 airflowk8stest.azurecr.io/pumpwood/pumpwood-auth-static:0.3
docker push airflowk8stest.azurecr.io/pumpwood/pumpwood-auth-static:0.3
