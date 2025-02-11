# Projeto_BD - CRUD

from database import conecta_bd, encerra_conn


def main():
    connection = conecta_bd()
    cursor = connection.cursor()

    # CREATE
    def inserir(matricula, nome_funcionario, idade,profissao,sigla_dep):
        cmd_insert = "INSERT INTO funcionarios (matricula, nome_funcionario, idade,profissao,sigla_dep) VALUES (%s,%s,%s,%s,%s)"
        valores = (matricula, nome_funcionario, idade,profissao,sigla_dep)
        cursor.execute(cmd_insert, valores)
        connection.commit()
        print("Dados inseridos com sucesso!!")

    # READ

    def seleciona(matricula, nome_funcionario):

        cria = "SELECT * FROM funcionarios;"
        values = matricula, nome_funcionario
        cursor.execute(cria, values)
        acoes = cursor.fetchall()
        for acao in acoes:
            print(acao)
        return acao

    # UPDATE
    def atualiza(matricula, nome_funcionario, idade,profissao,sigla_dep_antiga):
        cmd_update = f'UPDATE funcionarios SET matricula = %s, nome_funcionario = %s, idade = %s, profissao = %s WHERE sigla_dep= %s'
        valores = (matricula, nome_funcionario, idade,profissao,sigla_dep_antiga)
        cursor.execute(cmd_update, valores)
        connection.commit()


    # DELETE

    def deleta(nome_funcionario):
        cmd_delete = f"DELETE FROM time WHERE nome_clube= %s"
        cursor.execute(cmd_delete, (nome_funcionario,))
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
