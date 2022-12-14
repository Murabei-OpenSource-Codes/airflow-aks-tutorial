# Airflow K8s with virtual nodes Tutorial
Tutorial to deploy Airflow on Azure AKS with KubernetsPodOperator. It
describes the steps needed to correctly configure the AKS cluster to run
Airflow and permit scheduling tasks on virtual node.

Using virtual node permit scaling resource intensive task on demand,
allocating the necessary resource and realizing them at the end of the task.
Using Airflow with CeleryExecutor along with KubernetsPodOperator permit
mixing simple Python functions with Pod execution.

This tutorial was developed as results of studies and application on different
clients by Murabei Data Science. Murabei is a consulting company from Brazil
dedicated to development of AI and statistical models along with development
of AI oriented systems, for further information check out
[website](https://www.murabei.com).

![alt text](__doc/murabei.png)

# Directory overview
The files of this tutorial are divided in some folders:

## Images
There are two simple docker at test_images subfolders there are two images
that were used on clusters tests. There is also a `login-repository.bash` script
responsible for logging at the docker image repository at Azure and a
pumpwood_images folder with scripts used to transfer some private images
from one repository to another.

The private images are not actually necessary, made the tests possible since
it was build an integration of the Airflow with Pumpood. It is not necessary
to deploy them, but some changes on yml must be necessary.

- **test-task-image:** A test image with a simple loop sleep.
- **test-task-image--error:** A test image with a simple loop sleep, but that
raises an error to test the ability of airflow to deal with error on Pod
execution.

## Deploy
To help creating the yml files with it was used a package to deploy Pumpwood
based systems. It is not necessary to run the those codes, the final yml files
are avaiable at deploy_yml_files.

On this files there are some scripts that helps creating disks, ip and logging
to the cluster on Azure.

- **01__create_public_ip.bash:** Creates an static IP to be used on Load
    Balancer.
- **02__create_disks.bash:** Creates an disks used to persists Postgres data.
- **03__create_fernet_cripto.py:** A simple Python script that can be used
- **04__login_cluster.bash:** Script to login to the cluster and create
    a separeted namespace to deploy the containers.
- **05__clear_cluster.bash:** Clear Kubernets cluster removing all deployments
    and volumes.
- **template__create_docker_secret.bash** A bash script to create the secrets
    necessary for K8s to login on private repository and retrieve images.

## Deploy yml files
Files generated by Pumpwood Deploy to deploy Pods necessary for Airflow.

#### 000__nginx-gateway__endpoint.yml
Create a NGINX gateway for HTTPS termination.

#### 000__rabbitmq__secrets.yml
Create a secrets for RabbitMQ.

#### 001__rabbitmq__deployment.yml
Deploy RabbitMQ.

#### 002__hash_salt__secrets.yml
Create a Secret to be used as salt for hash (not necessary for Airflow).

#### 003__storage-config.yml
Configure the type of storage to be used on Pumpwood (not necessary for Airflow).

#### 004__azure__storage_key.yml
If used, configure Azure credentials for storages (not necessary for Airflow).

#### 005__gcp--storage-key.yml
If used, configure GCP credentials for storages (not necessary for Airflow).

#### 006__aws__storage_key.yml
Configure the type of storage to be used on Pumpwood (not necessary for Airflow).

#### 007__microsservice_model__secrets.yml
Configure secrets for Microservices on Pumpwood (not necessary for Airflow).

#### 008__load_balancer__volume.yml
Create a volume to be used by Kong (not necessary for Airflow).

#### 009__load_balancer__postgres.yml
Deploy a Postgres to be used by Kong (not necessary for Airflow).

#### 010__load_balancer__app.yml
Deploy a Kong service mesh (not necessary for Airflow).

#### 011__nginx-gateway__deploy.yml
Create a NGINX gateway for HTTPS termination.

#### 012__pumpwood_auth__secrets.yml
Secrets for Pumpwood Auth (not necessary for Airflow).

#### 013__pumpwood_auth__volume.yml
Volume for postgres for Pumpwood Auth (not necessary for Airflow).

#### 014__pumpwood_auth__postgres.yml
Deploy for postgres for Pumpwood Auth (not necessary for Airflow).

#### 015__pumpwood_auth_app__deploy.yml
Deploy for api for Pumpwood Auth (not necessary for Airflow).

#### 016__pumpwood_auth_admin_static__deploy.yml
Static files for Pumpwood Auth Django Admin (not necessary for Airflow).

#### 017__airflow__secrets.yml
Secrets used on Airflow.

#### 019__airflow__serviceaccount.yml
Create a service account for Airflow to create Pods on K8s.

#### 020__airflow__volume.yml
Create a volume for Airfow Postgres.

#### 021__airflow__postgres.yml
Create a deploy for Airflow Postgres.

#### 022__airflow_app__deploy.yml
Create an Deploy for Airflow front-end.

#### 023__airflow_scheduler__deploy.yml
Create an Deploy for Airflow scheduler.

#### 024__airflow_worker__deploy.yml
Create an Deploy for Airflow worker.

# General configuration commands
To create the first user on airflow at K8s, it is possible to enter de container using kubectrl exec command.

Exemple of commands:
```
$kubectl get pods
NAME                                         READY   STATUS      RESTARTS      AGE
apigateway-kong-66b886448d-c6rkr             1/1     Running     0             29h
apigateway-kong-66b886448d-f88l6             1/1     Running     0             29h
apigateway-nginx-b5b75c485-gdtz5             1/1     Running     0             28h
kube-op-3-e28221cb2c574d58a4d164f91114dddd   0/1     Completed   0             26h
postgres-kong-database-5d45bf895f-rnx2g      1/1     Running     0             29h
postgres-pumpwood-auth-588fd54488-9qlxn      1/1     Running     0             29h
postgres-simple-airflow-5f7c49f9b5-658vb     1/1     Running     0             29h
pumpwood-auth-app-8596465cf9-kf7mm           1/1     Running     0             29h
pumpwood-auth-static-6b9dfcf96b-27sv7        1/1     Running     0             29h
rabbitmq-main-8684fc8f99-mb4c7               1/1     Running     0             29h
simple-airflow--scheduler-5ff8bb7c5b-kqt5g   1/1     Running     1 (29h ago)   29h
simple-airflow--webserver-6ff994945c-prhsv   1/1     Running     0             29h
simple-airflow--worker-6b7dcf774d-g6tqz      1/1     Running     1 (29h ago)   29h
simple-airflow--worker-6b7dcf774d-jd8bb      1/1     Running     1 (29h ago)   29h
simple-airflow--worker-6b7dcf774d-mk8fb      1/1     Running     2 (29h ago)   29h

# Use exec command with -it to run bash in the container with interactive mode
kubectl exec -it simple-airflow--webserver-6ff994945c-prhsv -- bash
root@simple-airflow--webserver-6ff994945c-prhsv:/airflow#

# At the Simple Airflow image the enviroment variables
# are create by an start script, and to create an Airflow
# user it is necessary to set them
export AIRFLOW__DATABASE__SQL_ALCHEMY_CONN="postgresql://${DB_USERNAME}:${DB_PASSWORD}@${DB_HOST}:${DB_PORT}/${DB_DATABASE}"
export AIRFLOW__CELERY__BROKER_URL="amqp://${RABBITMQ_USERNAME}:${RABBITMQ_PASSWORD}@${RABBITMQ_HOST}:${RABBITMQ_PORT}/airflow"
export AIRFLOW__CELERY__RESULT_BACKEND="db+postgresql://${DB_USERNAME}:${DB_PASSWORD}@${DB_HOST}:${DB_PORT}/${DB_DATABASE}"

# Create the first user on Airflow
airflow users create \
  --username admin \
  --firstname FIRST_NAME \
  --lastname LAST_NAME \
  --role Admin \
  --email admin@example.org
```
