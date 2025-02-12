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
        except Exception as err:
            return f"Erro ao inserir dados: {err}"
    def deletar(self, id_jogador):
        try:
            cmd_delete = "DELETE FROM elenco WHERE id_jogador = %s"
            self.cursor.execute(cmd_delete, (id_jogador,))
            self.connection.commit()
            return "Jogador deletado com sucesso!"
        except Exception as err:
            return f"Erro ao deletar jogador: {err}"

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
            return "Jogador atualizado com sucesso!"
        except Exception as err:
            return f"Erro ao atualizar jogador: {err}"

    def selecionar(self, id_jogador=None):
        try:
            cmd_select = "SELECT * FROM elenco"
            if id_jogador:
                cmd_select += " WHERE id_jogador = %s"
                self.cursor.execute(cmd_select, (id_jogador,))
            else:
                self.cursor.execute(cmd_select)
            return self.cursor.fetchall()
        except Exception as err:
            return f"Erro ao selecionar jogador: {err}"
    def __del__(self):
        encerra_conn(self.connection)
