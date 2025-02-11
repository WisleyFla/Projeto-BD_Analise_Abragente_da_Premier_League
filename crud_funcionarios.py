from database import conecta_bd, encerra_conn

class CRUDFuncionario:
    def __init__(self):
        self.connection = conecta_bd()
        self.cursor = self.connection.cursor()

    def inserir(self, matricula, nome_funcionario, idade, profissao, sigla_dep):
        try:
            cmd_insert = """
                INSERT INTO funcionarios (matricula, nome_funcionario, idade, profissao, sigla_dep)
                VALUES (%s, %s, %s, %s, %s)
            """
            valores = (matricula, nome_funcionario, idade, profissao, sigla_dep)
            self.cursor.execute(cmd_insert, valores)
            self.connection.commit()
            return "Dados inseridos com sucesso!"
        except psycopg2.Error as err:
            return f"Erro ao inserir dados: {err}"

    def selecionar(self, matricula=None, nome_funcionario=None):
        try:
            cmd_select = "SELECT * FROM funcionarios"
            if matricula or nome_funcionario:
                cmd_select += " WHERE "
                conditions = []
                if matricula:
                    conditions.append(f"matricula = %s")
                if nome_funcionario:
                    conditions.append(f"nome_funcionario = %s")
                cmd_select += " AND ".join(conditions)
            valores = tuple(filter(None, [matricula, nome_funcionario]))
            self.cursor.execute(cmd_select, valores)
            return self.cursor.fetchall()
        except psycopg2.Error as err:
            return f"Erro ao selecionar dados: {err}"

    def atualizar(self, matricula, nome_funcionario, idade, profissao, sigla_dep_antiga):
        try:
            cmd_update = """
                UPDATE funcionarios
                SET matricula = %s, nome_funcionario = %s, idade = %s, profissao = %s
                WHERE sigla_dep = %s
            """
            valores = (matricula, nome_funcionario, idade, profissao, sigla_dep_antiga)
            self.cursor.execute(cmd_update, valores)
            self.connection.commit()
            return "Dados atualizados com sucesso!"
        except psycopg2.Error as err:
            return f"Erro ao atualizar dados: {err}"

    def deletar(self, nome_funcionario):
        try:
            cmd_delete = "DELETE FROM funcionarios WHERE nome_funcionario = %s"
            self.cursor.execute(cmd_delete, (nome_funcionario,))
            self.connection.commit()
            return "Dados deletados com sucesso!"
        except psycopg2.Error as err:
            return f"Erro ao deletar dados: {err}"

    def __del__(self):
        encerra_conn(self.connection)
