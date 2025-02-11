from database import conecta_bd, encerra_conn

class CRUDTime:
    def __init__(self):
        self.connection = conecta_bd()
        self.cursor = self.connection.cursor()

    def inserir(self, sigla, nome_clube, fundacao, mascote, n_titulos):
        try:
            cmd_insert = """
                INSERT INTO time (sigla, nome_clube, fundacao, mascote, n_titulos)
                VALUES (%s, %s, %s, %s, %s)
            """
            valores = (sigla, nome_clube, fundacao, mascote, n_titulos)
            self.cursor.execute(cmd_insert, valores)
            self.connection.commit()
            return "Dados inseridos com sucesso!"
        except psycopg2.Error as err:
            return f"Erro ao inserir dados: {err}"

    def selecionar(self, sigla=None, nome_clube=None):
        try:
            cmd_select = "SELECT * FROM time"
            if sigla or nome_clube:
                cmd_select += " WHERE "
                conditions = []
                if sigla:
                    conditions.append(f"sigla = %s")
                if nome_clube:
                    conditions.append(f"nome_clube = %s")
                cmd_select += " AND ".join(conditions)
            valores = tuple(filter(None, [sigla, nome_clube]))
            self.cursor.execute(cmd_select, valores)
            return self.cursor.fetchall()
        except psycopg2.Error as err:
            return f"Erro ao selecionar dados: {err}"

    def atualizar(self, sigla, nome_clube, mascote, n_titulos, nome_original):
        try:
            cmd_update = """
                UPDATE time
                SET sigla = %s, nome_clube = %s, mascote = %s, n_titulos = %s
                WHERE nome_clube = %s
            """
            valores = (sigla, nome_clube, mascote, n_titulos, nome_original)
            self.cursor.execute(cmd_update, valores)
            self.connection.commit()
            return "Dados atualizados com sucesso!"
        except psycopg2.Error as err:
            return f"Erro ao atualizar dados: {err}"

    def deletar(self, nome_clube):
        try:
            cmd_delete = "DELETE FROM time WHERE nome_clube = %s"
            self.cursor.execute(cmd_delete, (nome_clube,))
            self.connection.commit()
            return "Dados deletados com sucesso!"
        except psycopg2.Error as err:
            return f"Erro ao deletar dados: {err}"

    def __del__(self):
        encerra_conn(self.connection)
