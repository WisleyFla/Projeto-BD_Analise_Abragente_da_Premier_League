from database import conecta_bd, encerra_conn

class CRUDTime:
    def __init__(self):
        self.connection = conecta_bd()
        self.cursor = self.connection.cursor()

    def inserir(self, sigla, nome_clube, fundacao, mascote, n_titulos, escudo):
        try:
            cmd_insert = """
                INSERT INTO time (sigla, nome_clube, fundacao, mascote, n_titulos, escudo)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            valores = (sigla, nome_clube, fundacao, mascote, n_titulos, escudo)
            self.cursor.execute(cmd_insert, valores)
            self.connection.commit()
            return "Time inserido com sucesso!"
        except Exception as err:
            return f"Erro ao inserir time: {err}"

    def deletar(self, sigla):
        try:
            # Comando para deletar o time
            cmd_delete_time = "DELETE FROM Time WHERE Sigla = %s"
            self.cursor.execute(cmd_delete_time, (sigla,))
            
            # Commit da transação
            self.connection.commit()
            return "Time e dados relacionados deletados com sucesso!"
        except Exception as err:
            # Rollback em caso de erro
            self.connection.rollback()
            return f"Erro ao deletar time: {err}"

    def atualizar(self, sigla, nome_clube, fundacao, mascote, n_titulos):
        try:
            # Comando para atualizar os dados do time
            cmd_update_time = """
                UPDATE Time
                SET Nome_clube = %s, Fundacao = %s, Mascote = %s, N_Titulos = %s
                WHERE Sigla = %s
            """
            valores_time = (nome_clube, fundacao, mascote, n_titulos, sigla)
            self.cursor.execute(cmd_update_time, valores_time)
            
            # Commit da transação
            self.connection.commit()
            return "Time atualizado com sucesso!"
        except Exception as err:
            # Rollback em caso de erro
            self.connection.rollback()
            return f"Erro ao atualizar time: {err}"

    def selecionar(self, sigla=None):
        try:
            cmd_select = "SELECT * FROM time"
            if sigla:
                cmd_select += " WHERE sigla = %s"
                self.cursor.execute(cmd_select, (sigla,))
            else:
                self.cursor.execute(cmd_select)
            return self.cursor.fetchall()
        except Exception as err:
            return f"Erro ao selecionar time: {err}"

    def __del__(self):
        encerra_conn(self.connection)
