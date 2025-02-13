from database import conecta_bd, encerra_conn

class CRUDElenco:
    def __init__(self):
        self.connection = conecta_bd()
        self.cursor = self.connection.cursor()

    def inserir(self, nome_jogador, idade, valor_mercado, sigla, sigla_posicao):
        try:
            # Validações básicas
            if not all([nome_jogador, idade, valor_mercado, sigla, sigla_posicao]):
                raise ValueError("Todos os campos são obrigatórios!")

            # Verifica se o time existe
            self.cursor.execute("SELECT sigla FROM time WHERE sigla = %s", (sigla,))
            if not self.cursor.fetchone():
                raise ValueError(f"Time com sigla {sigla} não encontrado!")

            # Verifica se a posição existe
            self.cursor.execute("SELECT sigla_posicao FROM posicao WHERE sigla_posicao = %s", (sigla_posicao,))
            if not self.cursor.fetchone():
                raise ValueError(f"Posição com sigla {sigla_posicao} não encontrada!")

            cmd_insert = """
                INSERT INTO elenco (nome_jogador, idade, valor_mercado, sigla, sigla_posicao)
                VALUES (%s, %s, %s, %s, %s)
            """
            valores = (nome_jogador, idade, valor_mercado, sigla, sigla_posicao)
            self.cursor.execute(cmd_insert, valores)
            self.connection.commit()
            return "Jogador inserido com sucesso!"
        except ValueError as ve:
            return f"Erro de validação: {str(ve)}"
        except Exception as err:
            self.connection.rollback()
            return f"Erro ao inserir jogador: {err}"

    def atualizar(self, nome_jogador_antigo, nome_jogador, idade, valor_mercado, sigla, sigla_posicao):
        try:
            # Validações básicas
            if not all([nome_jogador_antigo, nome_jogador, idade, valor_mercado, sigla, sigla_posicao]):
                raise ValueError("Todos os campos são obrigatórios!")

            # Verificar se o jogador existe no time
            self.cursor.execute("""
                SELECT id_jogador FROM elenco 
                WHERE nome_jogador = %s AND sigla = %s
            """, (nome_jogador_antigo, sigla))
            
            if not self.cursor.fetchone():
                raise ValueError(f"Jogador {nome_jogador_antigo} não encontrado no time {sigla}!")

            # Verifica se o time existe
            self.cursor.execute("SELECT sigla FROM time WHERE sigla = %s", (sigla,))
            if not self.cursor.fetchone():
                raise ValueError(f"Time com sigla {sigla} não encontrado!")

            # Verifica se a posição existe
            self.cursor.execute("SELECT sigla_posicao FROM posicao WHERE sigla_posicao = %s", (sigla_posicao,))
            if not self.cursor.fetchone():
                raise ValueError(f"Posição com sigla {sigla_posicao} não encontrada!")

            # Verificar se já existe outro jogador com o novo nome no mesmo time
            if nome_jogador != nome_jogador_antigo:
                self.cursor.execute("""
                    SELECT id_jogador FROM elenco 
                    WHERE nome_jogador = %s AND sigla = %s
                """, (nome_jogador, sigla))
                
                if self.cursor.fetchone():
                    raise ValueError(f"Já existe um jogador com o nome {nome_jogador} neste time!")

            # Comando de atualização
            cmd_update = """
                UPDATE elenco 
                SET nome_jogador = %s, 
                    idade = %s, 
                    valor_mercado = %s, 
                    sigla_posicao = %s
                WHERE nome_jogador = %s AND sigla = %s
            """
            valores = (nome_jogador, idade, valor_mercado, sigla_posicao, 
                       nome_jogador_antigo, sigla)
            
            self.cursor.execute(cmd_update, valores)
            self.connection.commit()
            return "Jogador atualizado com sucesso!"
        except ValueError as ve:
            return f"Erro de validação: {str(ve)}"
        except Exception as err:
            self.connection.rollback()
            return f"Erro ao atualizar jogador: {err}"

    def deletar(self, nome_jogador, sigla):
        try:
            if not nome_jogador or not sigla:
                raise ValueError("Nome do jogador e sigla do time são obrigatórios!")

            # Verifica se o jogador existe no time especificado
            cmd_check = """
                SELECT id_jogador FROM elenco 
                WHERE nome_jogador = %s AND sigla = %s
            """
            self.cursor.execute(cmd_check, (nome_jogador, sigla))
            if not self.cursor.fetchone():
                raise ValueError(f"Jogador {nome_jogador} não encontrado no time {sigla}!")

            cmd_delete = "DELETE FROM elenco WHERE nome_jogador = %s AND sigla = %s"
            self.cursor.execute(cmd_delete, (nome_jogador, sigla))
            self.connection.commit()
            return "Jogador deletado com sucesso!"
        except ValueError as ve:
            return f"Erro de validação: {str(ve)}"
        except Exception as err:
            self.connection.rollback()
            return f"Erro ao deletar jogador: {err}"

    def selecionar(self, nome_jogador=None, sigla=None):
        try:
            # Base query com JOINS para obter informações completas
            cmd_select = """
                SELECT 
                    e.id_jogador, 
                    e.nome_jogador, 
                    e.idade, 
                    e.valor_mercado, 
                    e.sigla, 
                    t.nome_clube, 
                    e.sigla_posicao, 
                    p.nome_posicao
                FROM 
                    elenco e
                JOIN 
                    time t ON e.sigla = t.sigla
                JOIN 
                    posicao p ON e.sigla_posicao = p.sigla_posicao
            """
            params = []
            conditions = []

            # Adiciona condições de busca
            if nome_jogador:
                conditions.append("e.nome_jogador = %s")
                params.append(nome_jogador)
            if sigla:
                conditions.append("e.sigla = %s")
                params.append(sigla)

            # Adiciona WHERE se houver condições
            if conditions:
                cmd_select = cmd_select.rstrip() + " WHERE " + " AND ".join(conditions)

            # Ordena os resultados
            cmd_select = cmd_select.rstrip() + " ORDER BY e.sigla, e.nome_jogador"

            self.cursor.execute(cmd_select, tuple(params))
            result = self.cursor.fetchall()
            
            if not result:
                return "Nenhum jogador encontrado."
            return result

        except Exception as err:
            return f"Erro ao selecionar jogador(es): {err}"

    def __del__(self):
        try:
            encerra_conn(self.connection)
        except:
            pass  # Ignora erros ao fechar a conexão