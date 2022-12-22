"""Create a fernet key to be used in Airflow to encript credentials."""
from cryptography.fernet import Fernet

fernet_key = Fernet.generate_key()
print(fernet_key.decode())
