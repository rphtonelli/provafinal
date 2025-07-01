import psycopg2
from psycopg2 import OperationalError
import yaml
import os

def create_connection():
    """
    Create a connection to the PostgreSQL database.
    :return: Connection object or None
    """
    try:
        # Tentar usar variáveis de ambiente primeiro (Docker)
        if os.getenv('DB_HOST'):
            connection = psycopg2.connect(
                user=os.getenv('DB_USER', 'faat'),
                password=os.getenv('DB_PASSWORD', 'faat'),
                host=os.getenv('DB_HOST', 'db'),
                port=os.getenv('DB_PORT', '5432'),
                database=os.getenv('DB_NAME', 'escola')
            )
        else:
            # Usar arquivo de configuração (desenvolvimento local)
            with open('Util/paramsBD.yml', 'r') as config_file:
                config = yaml.safe_load(config_file)
            connection = psycopg2.connect(
                user=config['user'],
                password=config['password'],
                host=config['host'],
                port=config['port'],
                database=config['database']
            )
        print("Connection to PostgreSQL DB successful")
        return connection
    except OperationalError as e:
        print(f"Error connecting to PostgreSQL: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None