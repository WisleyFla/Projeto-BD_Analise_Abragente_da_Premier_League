# Projeto_BD - database

import psycopg2
import os
from dotenv import load_dotenv
from psycopg2 import Error

load_dotenv()

password = "admin"


def conecta_bd():
    try:
        conn = psycopg2.connect(
            user="postgres",
            password=password,
            host="localhost",
            port="5432",
            database="Premier")

        print("Banco conectado com sucesso!!")

        return conn

    except Error as e:
        print(f"Ocorreu um erro ao conectar ao banco {e}")


def encerra_conn(conn):
    if conn:
        conn.close()
    print("Conexão encerrada!!")

conecta_bd()

