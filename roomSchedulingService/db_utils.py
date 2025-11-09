import os
import time
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

def get_connection(retries=3, delay=1):

    required_vars = ['DB_HOST', 'DB_USER', 'DB_PASSWORD', 'DB_NAME', 'DB_PORT']
    for var in required_vars:
        if not os.getenv(var):
            raise ValueError(f"Missing required environment variable: {var}")


    
    host = os.getenv('DB_HOST')
    user = os.getenv('DB_USER')
    password = os.getenv('DB_PASSWORD')
    database = os.getenv('DB_NAME')
    port = int(os.getenv('DB_PORT'))
    last_exc = None

    print(host,user.password,database)

    for _ in range(retries):
        try:
            conn = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database,
                port=port
            )
            return conn
        except Exception as e:
            last_exc = e
            time.sleep(delay)
    raise last_exc
