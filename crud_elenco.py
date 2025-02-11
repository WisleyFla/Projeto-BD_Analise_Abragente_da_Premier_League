# Projeto_BD - CRUD

from database import conecta_bd, encerra_conn


def main():
    connection = conecta_bd()
    cursor = connection.cursor()

    # CREATE
    def inserir(id_jogador, nome_jogador, idade,valor_mercado,sigla,sigla_posicao):
        cmd_insert = "INSERT INTO elenco (id_jogador, nome_jogador, idade,valor_mercado,sigla,sigla_posicao) VALUES (%s,%s,%s,%s,%s,%s)"
        valores = (id_jogador, nome_jogador, idade,valor_mercado,sigla,sigla_posicao)
        cursor.execute(cmd_insert, valores)
        connection.commit()
        print("Dados inseridos com sucesso!!")

    # READ

    def seleciona(nome_jogador,sigla_posicao):

        cria = "SELECT * FROM elenco;"
        values = nome_jogador,sigla_posicao
        cursor.execute(cria, values)
        acoes = cursor.fetchall()
        for acao in acoes:
            print(acao)
        return acao

    # UPDATE
    def atualiza(id_jogador, nome_jogador, idade,valor_mercado,sigla,sigla_posicao):
        cmd_update = f'UPDATE elenco SET id_jogador = %s, nome_jogador = %s, idade = %s, valor_mercado = %s WHERE nome_jogador= %s'
        valores = (id_jogador, nome_jogador, idade,valor_mercado,sigla,sigla_posicao)
        cursor.execute(cmd_update, valores)
        connection.commit()


    # DELETE

    def deleta(nome_jogador):
        cmd_delete = f"DELETE FROM elenco WHERE nome_clube= %s"
        cursor.execute(cmd_delete, (nome_jogador,))
        connection.commit()
        cursor.execute("SELECT * FROM elenco")
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
