from PyQt6.QtWidgets import QApplication, QWidget, QFileDialog, QMessageBox
from PyQt6.QtCore import Qt
from database import conecta_bd, encerra_conn

class CRUDTime:
    def __init__(self):
        self.connection = conecta_bd()
        self.cursor = self.connection.cursor()
        self.escudo_binario = None  # Inicializa a variável para armazenar a imagem

    def selecionar_imagem(self):
        filetypes = "Imagens (*.jpg *.jpeg *.png *.gif *.bmp);;Todos os arquivos (*)"
        
        filename, _ = QFileDialog.getOpenFileName(
            None, 
            'Selecione o Escudo do Time', 
            '', 
            filetypes
        )
        
        if filename:
            try:
                # Ler o arquivo como dados binários
                with open(filename, 'rb') as file:
                    self.escudo_binario = file.read()
                
                # Exibir nome do arquivo selecionado
                nome_arquivo = filename.split('/')[-1]
                print(f"Imagem selecionada: {nome_arquivo}")
                QMessageBox.information(None, "Sucesso", f"Imagem selecionada: {nome_arquivo}")
                return True

            except Exception as e:
                self.escudo_binario = None
                print(f"Erro ao carregar imagem: {str(e)}")
                QMessageBox.critical(None, "Erro", f"Não foi possível carregar a imagem: {str(e)}")
                return False
        return False

    def inserir(self, sigla, nome_clube, fundacao, mascote, n_titulos):
        try:
            # Validações básicas
            if not all([sigla, nome_clube, fundacao, mascote, n_titulos]):
                raise ValueError("Todos os campos são obrigatórios!")
            
            # Converter data de dia/mes/ano para ano/mes/dia
            try:
                # Validar formato da data
                dia, mes, ano = fundacao.split('/')
                
                # Validar componentes da data
                dia = int(dia)
                mes = int(mes)
                ano = int(ano)
                
                # Validar intervalo de valores
                if not (1 <= mes <= 12 and 1 <= dia <= 31 and ano > 0):
                    raise ValueError("Data inválida")
                
                # Converter para formato ano-mes-dia
                fundacao_formatada = f"{ano}-{mes:02d}-{dia:02d}"
            except (ValueError, TypeError) as e:
                raise ValueError("Formato de data inválido. Use dia/mes/ano (ex: 15/08/1990)")

            # Verifica se a sigla já existe
            self.cursor.execute("SELECT Sigla FROM Time WHERE Sigla = %s", (sigla,))
            if self.cursor.fetchone():
                raise ValueError("Time com esta sigla já existe!")

            cmd_insert = """
                INSERT INTO Time (Sigla, Nome_clube, Fundacao, Mascote, N_Titulos, Escudo)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            valores = (sigla, nome_clube, fundacao_formatada, mascote, n_titulos, self.escudo_binario)
            self.cursor.execute(cmd_insert, valores)
            self.connection.commit()
            
            # Limpa o escudo binário após a inserção
            self.escudo_binario = None
            return "Time inserido com sucesso!"
        
        except ValueError as ve:
            self.connection.rollback()
            return f"Erro de validação: {str(ve)}"
        except Exception as err:
            self.connection.rollback()
            return f"Erro ao inserir time: {err}"

    def deletar(self, sigla):
        try:
            if not sigla:
                raise ValueError("A sigla do time é obrigatória!")

            # Verifica se o time existe
            self.cursor.execute("SELECT Sigla FROM Time WHERE Sigla = %s", (sigla,))
            if not self.cursor.fetchone():
                raise ValueError("Time não encontrado!")

            # Comando para deletar o time
            cmd_delete_time = "DELETE FROM Time WHERE Sigla = %s"
            self.cursor.execute(cmd_delete_time, (sigla,))
            
            # Commit da transação
            self.connection.commit()
            return "Time e dados relacionados deletados com sucesso!"
        
        except ValueError as ve:
            self.connection.rollback()
            return f"Erro de validação: {str(ve)}"
        except Exception as err:
            self.connection.rollback()
            return f"Erro ao deletar time: {err}"

    def atualizar(self, sigla, nome_clube, fundacao, mascote, n_titulos):
        try:
            # Validações básicas
            if not all([sigla, nome_clube, fundacao, mascote, n_titulos]):
                raise ValueError("Todos os campos são obrigatórios!")

            # Converter data de dia/mes/ano para ano/mes/dia
            try:
                # Validar formato da data
                dia, mes, ano = fundacao.split('/')
                
                # Validar componentes da data
                dia = int(dia)
                mes = int(mes)
                ano = int(ano)
                
                # Validar intervalo de valores
                if not (1 <= mes <= 12 and 1 <= dia <= 31 and ano > 0):
                    raise ValueError("Data inválida")
                
                # Converter para formato ano-mes-dia
                fundacao_formatada = f"{ano}-{mes:02d}-{dia:02d}"
            except (ValueError, TypeError) as e:
                raise ValueError("Formato de data inválido. Use dia/mes/ano (ex: 15/08/1990)")

            # Verifica se o time existe
            self.cursor.execute("SELECT Sigla FROM Time WHERE Sigla = %s", (sigla,))
            if not self.cursor.fetchone():
                raise ValueError("Time não encontrado!")

            # Comando para atualizar os dados do time
            cmd_update_time = """
                UPDATE Time
                SET Nome_clube = %s, Fundacao = %s, Mascote = %s, N_Titulos = %s
                WHERE Sigla = %s
            """
            valores_time = (nome_clube, fundacao_formatada, mascote, n_titulos, sigla)
            self.cursor.execute(cmd_update_time, valores_time)
            
            # Atualiza o escudo se houver um novo
            if self.escudo_binario is not None:
                cmd_update_escudo = "UPDATE Time SET Escudo = %s WHERE Sigla = %s"
                self.cursor.execute(cmd_update_escudo, (self.escudo_binario, sigla))
                self.escudo_binario = None  # Limpa o escudo após a atualização
            
            # Commit da transação
            self.connection.commit()
            return "Time atualizado com sucesso!"
        
        except ValueError as ve:
            self.connection.rollback()
            return f"Erro de validação: {str(ve)}"
        except Exception as err:
            self.connection.rollback()
            return f"Erro ao atualizar time: {err}"

    def selecionar(self, sigla=None):
        try:
            if sigla:
                # Busca um time específico
                cmd_select = """
                    SELECT 
                        Sigla, 
                        Nome_clube, 
                        TO_CHAR(Fundacao, 'DD/MM/YYYY'), 
                        Mascote, 
                        N_Titulos, 
                        Escudo 
                    FROM Time 
                    WHERE Sigla = %s
                """
                self.cursor.execute(cmd_select, (sigla,))
            else:
                # Busca todos os times
                cmd_select = """
                    SELECT 
                        Sigla, 
                        Nome_clube, 
                        TO_CHAR(Fundacao, 'DD/MM/YYYY'), 
                        Mascote, 
                        N_Titulos, 
                        Escudo 
                    FROM Time
                """
                self.cursor.execute(cmd_select)
            
            resultados = self.cursor.fetchall()
            
            # Se não encontrou nenhum resultado
            if not resultados:
                return "Nenhum time encontrado."
                
            return resultados
            
        except Exception as err:
            return f"Erro ao selecionar time: {err}"

    def __del__(self):
        """Destrutor da classe - fecha a conexão com o banco de dados"""
        try:
            encerra_conn(self.connection)
        except:
            pass  # Ignora erros ao fechar a conexão

# Teste da classe
if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    crud = CRUDTime()
    
    # Exemplo de uso
    resultado = crud.selecionar()
    print("Times cadastrados:", resultado)
    
    sys.exit(app.exec())