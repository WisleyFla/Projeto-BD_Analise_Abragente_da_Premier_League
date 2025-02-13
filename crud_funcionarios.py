from database import conecta_bd, encerra_conn

class CRUDFuncionario:
    def __init__(self):
        self.connection = conecta_bd()
        self.cursor = self.connection.cursor()
    
    def inserir(self, nome_funcionario, idade, profissao, sigla_departamento, sigla_time):
        try:
            # Buscar a maior matrícula existente
            self.cursor.execute("SELECT MAX(matricula) FROM funcionarios")
            max_matricula = self.cursor.fetchone()[0]
            
            # Gerar nova matrícula
            nova_matricula = 1 if max_matricula is None else max_matricula + 1
            
            cmd_insert = """
                INSERT INTO funcionarios (matricula, nome_funcionario, idade, profissao, sigla_departamento, sigla_time) 
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            valores = (nova_matricula, nome_funcionario, idade, profissao, sigla_departamento, sigla_time)
            self.cursor.execute(cmd_insert, valores)
            self.connection.commit()
            return f"Funcionário inserido com sucesso! Matrícula: {nova_matricula}"
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
    
    def atualizar(self, matricula_antiga, matricula, nome_funcionario, idade, profissao, sigla_departamento, sigla_time):
        try:
            cmd_update = """
                UPDATE funcionarios
                SET matricula = %s, nome_funcionario = %s, idade = %s, profissao = %s, sigla_departamento = %s, sigla_time = %s
                WHERE matricula = %s
            """
            valores = (matricula, nome_funcionario, idade, profissao, sigla_departamento, sigla_time, matricula_antiga)
            self.cursor.execute(cmd_update, valores)
            self.connection.commit()
            return "Funcionário atualizado com sucesso!"
        except Exception as err:
            return f"Erro ao atualizar funcionário: {err}"
    
    def selecionar(self, nome=None, sigla_time=None):
        try:
            if nome or sigla_time:
                cmd_select = """
                    SELECT f.matricula, f.nome_funcionario, f.idade, f.profissao, d.nome_departamento, t.nome_clube
                    FROM funcionarios f
                    JOIN departamentos d ON f.sigla_departamento = d.sigla_departamento
                    JOIN time t ON f.sigla_time = t.sigla
                    WHERE (f.nome_funcionario LIKE %s OR %s IS NULL)
                    AND (t.sigla = %s OR %s IS NULL)
                """
                self.cursor.execute(cmd_select, (f"%{nome}%", nome, sigla_time, sigla_time))
            else:
                cmd_select = """
                    SELECT f.matricula, f.nome_funcionario, f.idade, f.profissao, d.nome_departamento, t.nome_clube  
                    FROM funcionarios f
                    JOIN departamentos d ON f.sigla_departamento = d.sigla_departamento
                    JOIN time t ON f.sigla_time = t.sigla
                """
                self.cursor.execute(cmd_select)
            return self.cursor.fetchall()
        except Exception as err:
            return f"Erro ao selecionar funcionário: {err}"
    
    def __del__(self):
        encerra_conn(self.connection)