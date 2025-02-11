# Projeto_BD - CRUD

from database import conecta_bd, encerra_conn


def main():
    connection = conecta_bd()
    cursor = connection.cursor()

    # CREATE
    def inserir(sigla, nome_clube, fundacao, mascote, n_titulos):
        cmd_insert = "INSERT INTO time (sigla, nome_clube,fundacao,mascote,n_titulos) VALUES (%s,%s,%s,%s,%s)"
        valores = (sigla, nome_clube, fundacao, mascote, n_titulos)
        cursor.execute(cmd_insert, valores)
        connection.commit()
        print("Dados inseridos com sucesso!!")

    # READ

    def seleciona(sigla, nome_clube):

        cria = "SELECT * FROM time;"
        values = sigla, nome_clube
        cursor.execute(cria, values)
        acoes = cursor.fetchall()
        for acao in acoes:
            print(acao)
        return acao

    # UPDATE
    def atualiza(sigla, nome_clube, mascote, n_titulos, nome_original):
        cmd_update = f'UPDATE time SET sigla = %s, nome_clube = %s, mascote = %s, n_titulos = %s WHERE nome_clube= %s'
        valores = (sigla, nome_clube, mascote, n_titulos, nome_original)
        cursor.execute(cmd_update, valores)
        connection.commit()


    # DELETE

    def deleta(nome_clube):
        cmd_delete = f"DELETE FROM time WHERE nome_clube= %s"
        cursor.execute(cmd_delete, (nome_clube,))
        connection.commit()
        cursor.execute("SELECT * FROM time")
        registros = cursor.fetchall()
        print("\nRegistros restantes na tabela:")
        for registro in registros:
            print(registro)
        return registros

    # inserir("FLA","Flamengo","1895-11-05","Urubu",50)
    #seleciona(sigla="FLA", nome_clube="Flamengo")
    #atualiza("FLA", "Flamenga", "Macaco", 10, "Flamengo")
    # deleta(nome_clube="Flamengo")


if __name__ == "__main__":
    main()
