from database import conecta_bd, encerra_conn

class CRUDFuncionario:
    def __init__(self):
        self.connection = conecta_bd()
        self.cursor = self.connection.cursor()

    def inserir(self, matricula, nome_funcionario, idade, profissao, sigla_departamento, sigla_time):
        try:
            cmd_insert = """
                INSERT INTO funcionarios (matricula, nome_funcionario, idade, profissao, sigla_departamento, sigla_time)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            valores = (matricula, nome_funcionario, idade, profissao, sigla_departamento, sigla_time)
            self.cursor.execute(cmd_insert, valores)
            self.connection.commit()
            return "Funcionário inserido com sucesso!"
        except Exception as err:
            return f"Erro ao inserir funcionário: {err}"

    def deletar(self, matricula):
        try:
            cmd_delete = "DELETE FROM funcionarios WHERE matricula = %s"
            self.cursor.execute(cmd_delete, (matricula,))
            self.connection.commit()
            return "Funcionário deletado com sucesso!"
        except Exception as err:
            return f"Erro ao deletar funcionário: {err}"

    def atualizar(self, matricula, nome_funcionario, idade, profissao, sigla_departamento, sigla_time):
        try:
            cmd_update = """
                UPDATE funcionarios
                SET nome_funcionario = %s, idade = %s, profissao = %s, sigla_departamento = %s, sigla_time = %s
                WHERE matricula = %s
            """
            valores = (nome_funcionario, idade, profissao, sigla_departamento, sigla_time, matricula)
            self.cursor.execute(cmd_update, valores)
            self.connection.commit()
            return "Funcionário atualizado com sucesso!"
        except Exception as err:
            return f"Erro ao atualizar funcionário: {err}"

    def selecionar(self, matricula=None):
        try:
            cmd_select = "SELECT * FROM funcionarios"
            if matricula:
                cmd_select += " WHERE matricula = %s"
                self.cursor.execute(cmd_select, (matricula,))
            else:
                self.cursor.execute(cmd_select)
            return self.cursor.fetchall()
        except Exception as err:
            return f"Erro ao selecionar funcionário: {err}"

    def __del__(self):
        encerra_conn(self.connection)