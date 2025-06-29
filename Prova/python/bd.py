"""
Módulo de conexão com banco de dados PostgreSQL
Este módulo gerencia a conexão com o banco de dados da escola infantil
"""
import psycopg2
from psycopg2 import Error
import logging

# Configurações de conexão com o banco de dados
DB_CONFIG = {
    'host': 'localhost',  # Host do banco (localhost para desenvolvimento)
    'database': 'escola_db',  # Nome do banco de dados
    'user': 'postgres',  # Usuário do PostgreSQL
    'password': 'secret',  # Senha do PostgreSQL
    'port': '5432'  # Porta padrão do PostgreSQL
}

def create_connection():
    """
    Cria e retorna uma conexão com o banco de dados PostgreSQL
    
    Returns:
        connection: Objeto de conexão psycopg2 ou None em caso de erro
    """
    try:
        # Tenta estabelecer conexão com o banco usando as configurações
        connection = psycopg2.connect(
            host=DB_CONFIG['host'],
            database=DB_CONFIG['database'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            port=DB_CONFIG['port']
        )
        
        # Log de sucesso na conexão
        logging.info("Conexão com PostgreSQL estabelecida com sucesso")
        return connection
        
    except Error as e:
        # Log de erro caso a conexão falhe
        logging.error(f"Erro ao conectar com PostgreSQL: {e}")
        return None

def test_connection():
    """
    Testa a conexão com o banco de dados
    
    Returns:
        bool: True se conexão bem-sucedida, False caso contrário
    """
    conn = create_connection()
    if conn:
        try:
            # Testa a conexão executando uma query simples
            cursor = conn.cursor()
            cursor.execute("SELECT version();")
            version = cursor.fetchone()
            logging.info(f"Versão do PostgreSQL: {version[0]}")
            cursor.close()
            conn.close()
            return True
        except Error as e:
            logging.error(f"Erro ao testar conexão: {e}")
            return False
    return False