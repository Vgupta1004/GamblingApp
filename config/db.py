import mysql.connector
from config.settings import *

def get_connection():
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        return connection
    except mysql.connector.Error as e:
        print(f"Connection failed: {e}")
        raise

def get_cursor(connection):
    return connection.cursor(dictionary=True)

def close_all(cursor=None, connection=None):
    if cursor:
        cursor.close()
    if connection:
        connection.close()