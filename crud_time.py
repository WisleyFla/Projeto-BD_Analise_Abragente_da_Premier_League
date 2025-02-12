from database import conecta_bd, encerra_conn

class CRUDTime:
    def __init__(self):
        self.connection = conecta_bd()
        self.cursor = self.connection.cursor()

    def inserir(self, sigla, nome_clube, fundacao, mascote, n_titulos, caminho_imagem):
        try:
            cmd_insert = """
                INSERT INTO time (sigla, nome_clube, fundacao, mascote, n_titulos, caminho_imagem)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            valores = (sigla, nome_clube, fundacao, mascote, n_titulos, caminho_imagem)
            self.cursor.execute(cmd_insert, valores)
            self.connection.commit()
            return "Time inserido com sucesso!"
        except Exception as err:
            return f"Erro ao inserir time: {err}"

    def deletar(self, sigla):
        try:
            cmd_delete = "DELETE FROM time WHERE sigla = %s"
            self.cursor.execute(cmd_delete, (sigla,))
            self.connection.commit()
            return "Time deletado com sucesso!"
        except Exception as err:
            return f"Erro ao deletar time: {err}"

    def atualizar(self, sigla, nome_clube, fundacao, mascote, n_titulos):
        try:
            cmd_update = """
                UPDATE time
                SET nome_clube = %s, fundacao = %s, mascote = %s, n_titulos = %s
                WHERE sigla = %s
            """
            valores = (nome_clube, fundacao, mascote, n_titulos, sigla)
            self.cursor.execute(cmd_update, valores)
            self.connection.commit()
            return "Time atualizado com sucesso!"
        except Exception as err:
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
