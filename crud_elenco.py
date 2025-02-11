from database import conecta_bd, encerra_conn

class CRUDElenco:
    def __init__(self):
        self.connection = conecta_bd()
        self.cursor = self.connection.cursor()

    def inserir(self, id_jogador, nome_jogador, idade, valor_mercado, sigla, sigla_posicao):
        try:
            cmd_insert = """
                INSERT INTO elenco (id_jogador, nome_jogador, idade, valor_mercado, sigla, sigla_posicao)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            valores = (id_jogador, nome_jogador, idade, valor_mercado, sigla, sigla_posicao)
            self.cursor.execute(cmd_insert, valores)
            self.connection.commit()
            return "Dados inseridos com sucesso!"
        except psycopg2.Error as err:
            return f"Erro ao inserir dados: {err}"

    def selecionar(self, nome_jogador=None, sigla_posicao=None):
        try:
            cmd_select = "SELECT * FROM elenco"
            if nome_jogador or sigla_posicao:
                cmd_select += " WHERE "
                conditions = []
                if nome_jogador:
                    conditions.append(f"nome_jogador = %s")
                if sigla_posicao:
                    conditions.append(f"sigla_posicao = %s")
                cmd_select += " AND ".join(conditions)
            valores = tuple(filter(None, [nome_jogador, sigla_posicao]))
            self.cursor.execute(cmd_select, valores)
            return self.cursor.fetchall()
        except psycopg2.Error as err:
            return f"Erro ao selecionar dados: {err}"

    def atualizar(self, id_jogador, nome_jogador, idade, valor_mercado, sigla, sigla_posicao):
        try:
            cmd_update = """
                UPDATE elenco
                SET nome_jogador = %s, idade = %s, valor_mercado = %s, sigla = %s, sigla_posicao = %s
                WHERE id_jogador = %s
            """
            valores = (nome_jogador, idade, valor_mercado, sigla, sigla_posicao, id_jogador)
            self.cursor.execute(cmd_update, valores)
            self.connection.commit()
            return "Dados atualizados com sucesso!"
        except psycopg2.Error as err:
            return f"Erro ao atualizar dados: {err}"

    def deletar(self, nome_jogador):
        try:
            cmd_delete = "DELETE FROM elenco WHERE nome_jogador = %s"
            self.cursor.execute(cmd_delete, (nome_jogador,))
            self.connection.commit()
            return "Dados deletados com sucesso!"
        except psycopg2.Error as err:
            return f"Erro ao deletar dados: {err}"

    def __del__(self):
        encerra_conn(self.connection)
