"""
Deploy Pods using Pumpwood Deploy.

It creates the YML files using Jinja templates wirh Python.
"""
import simplejson as json
from pumpwood_deploy.deploy import DeployPumpWood
from pumpwood_deploy.microservices.api_gateway.deploy import ApiGateway
from pumpwood_deploy.microservices.pumpwood_auth.deploy import (
    PumpWoodAuthMicroservice)

# Airflow
from pumpwood_deploy.airflow.deploy import AirflowMicroservice


################
# Read secrets #
with open("secrets/secrets.secrets", "r") as file:
    secrets = json.loads(file.read())


#########################
# Create deploy objects #
deploy = DeployPumpWood(
    model_user_password="microservice--model",
    rabbitmq_secret=secrets["rabbitmq_secret"],
    hash_salt=secrets["hash_salt"],

    kong_db_disk_name="pumpwood--postgres--kong",
    kong_db_disk_size="10Gi",

    k8_provider="azure",
    k8_deploy_args={
        "subscription": "eec443ab-c101-4d83-a612-ec3f87c7fb59",
        "resource_group": "AirflowK8s",
        "k8s_resource_group": (
            "MC_AirflowK8s_AirflowK8sTest_brazilsouth"),
        "aks_resource": "AirflowK8sTest",
    },
    k8_namespace="airflow-test",
    storage_type="azure_storage",
    storage_deploy_args={
        "azure_storage": {
            "azure_storage_connection_string": secrets[
                "azure_storage_connection_string"]
        }
    })

deploy.add_microservice(
    ApiGateway(
        gateway_public_ip="4.228.102.59",
        email_contact="a.baceti@murabei.com",
        version="0.32",
        health_check_url="health-check/pumpwood-auth-app/",
        server_name="aks-airflow-test.brazilsouth.cloudapp.azure.com",
        repository="airflowk8stest.azurecr.io/pumpwood",
        souce_ranges=[
            # Murabei
            secrets["souce_ranges"],
        ]))

deploy.add_microservice(
    PumpWoodAuthMicroservice(
        replicas=1,
        secret_key=secrets["secret_key"],
        db_password=secrets["auth_db_password"],
        microservice_password=secrets["auth_password"],
        email_host_user="teste1",
        email_host_password="teste2",
        bucket_name="test-pumpwood",
        version_app="0.66",
        version_static="0.3",
        debug="FALSE",
        disk_size="20Gi",
        disk_name="pumpwood--postgres--auth",
        repository="airflowk8stest.azurecr.io/pumpwood",
        postgres_limits_memory="4Gi",
        postgres_limits_cpu="2000m",
        postgres_requests_memory="10Mi",
        postgres_requests_cpu="1m"))

deploy.add_microservice(
    AirflowMicroservice(
        db_password=secrets["airflow_db_password"],
        microservice_password=secrets["airflow_microservice"],
        secret_key=secrets["airflow_secret_key"],
        fernet_key=secrets["airflow_fernet_key"],
        k8s_pods_namespace="airflow-test",
        bucket_name="airflow-test",
        version="0.18",
        disk_size="20Gi",
        disk_name="pumpwood--postgres--airflow",
        firewall_ips=[],
        app_replicas=1, worker_replicas=3,
        git_ssh_private_key_path="secrets/airflow/id_rsa",
        git_ssh_public_key_path="secrets/airflow/id_rsa.pub",
        git_server="github.com",
        git_repository=(
            "git@github.com:Murabei-OpenSource-Codes/airflow-aks-tutorial--dags.git"),
        git_branch="main"))

# results = deploy.create_deploy_files()
deploy.deploy_cluster()
# self.deploy_cluster()
