import psycopg2
import os
from dotenv import load_dotenv
from psycopg2 import Error

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

def conecta_bd():
    try:
        conn = psycopg2.connect(
            user=os.getenv("DB_USER"),  # Usuário do banco de dados
            password=os.getenv("DB_PASSWORD"),  # Senha do banco de dados
            host=os.getenv("DB_HOST"),  # Host do banco de dados
            port=os.getenv("DB_PORT"),  # Porta do banco de dados
            database=os.getenv("DB_NAME")  # Nome do banco de dados
        )
        print("Banco conectado com sucesso!!")
        return conn
    except Error as e:
        print(f"Ocorreu um erro ao conectar ao banco: {e}")
        return None

def encerra_conn(conn):
    if conn:
        conn.close()
        print("Conexão encerrada!!")

# Teste da conexão (opcional)
if __name__ == "__main__":
    conn = conecta_bd()
    if conn:
        encerra_conn(conn)

"""def salvar_imagem(nome_arquivo, conn):
    cursor = conn.cursor()
    with open(nome_arquivo, 'rb') as file:
        imagem_binaria = file.read()

    cursor.execute("INSERT INTO imagens (nome, imagem) VALUES (%s, %s)", 
                   ("Imagem Exemplo", imagem_binaria))
    conn.commit()
    print("Imagem salva com sucesso!")

# Chamada do código
conn = conecta_bd()
if conn:
    salvar_imagem("imagem_exemplo.jpg", conn)
    conn.close()"""
