from PyQt6.QtWidgets import (QDialog, QLabel, QLineEdit, QPushButton, 
                           QGridLayout, QMessageBox, QTableWidget, 
                           QTableWidgetItem, QComboBox)
from PyQt6.QtCore import Qt
from database import conecta_bd

class InsertElencoDialog(QDialog):
    def __init__(self, crud_elenco, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Inserir Jogador")
        self.crud_elenco = crud_elenco
        self.setup_ui()

    def setup_ui(self):
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        self.resize(400, 300)

        # Create form fields
        self.nome_jogador_edit = QLineEdit()
        self.idade_edit = QLineEdit()
        self.valor_mercado_edit = QLineEdit()
        
        # Criar ComboBoxes para times e posições
        self.time_combo = QComboBox()
        self.posicao_combo = QComboBox()
        
        # Carregar dados nos ComboBoxes
        self.carregar_times()
        self.carregar_posicoes()

        # Add labels and fields to layout
        self.layout.addWidget(QLabel("Nome do Jogador:"), 0, 0)
        self.layout.addWidget(self.nome_jogador_edit, 0, 1)
        self.layout.addWidget(QLabel("Idade:"), 1, 0)
        self.layout.addWidget(self.idade_edit, 1, 1)
        self.layout.addWidget(QLabel("Valor de Mercado:"), 2, 0)
        self.layout.addWidget(self.valor_mercado_edit, 2, 1)
        self.layout.addWidget(QLabel("Time:"), 3, 0)
        self.layout.addWidget(self.time_combo, 3, 1)
        self.layout.addWidget(QLabel("Posição:"), 4, 0)
        self.layout.addWidget(self.posicao_combo, 4, 1)

        # Add submit button
        self.submit_btn = QPushButton("Inserir")
        self.submit_btn.clicked.connect(self.submit)
        self.layout.addWidget(self.submit_btn, 6, 0, 1, 2)

    def carregar_times(self):
        try:
            # Conectar ao banco de dados
            connection = conecta_bd()
            cursor = connection.cursor()
            
            # Buscar todos os times
            cursor.execute("SELECT sigla, nome_clube FROM time ORDER BY nome_clube")
            times = cursor.fetchall()
            
            # Adicionar times ao ComboBox
            for sigla, nome in times:
                self.time_combo.addItem(f"{nome} ({sigla})", sigla)
                
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao carregar times: {str(e)}")
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'connection' in locals():
                connection.close()

    def carregar_posicoes(self):
        try:
            # Conectar ao banco de dados
            connection = conecta_bd()
            cursor = connection.cursor()
            
            # Buscar todas as posições
            cursor.execute("SELECT sigla_posicao, nome_posicao FROM posicao ORDER BY nome_posicao")
            posicoes = cursor.fetchall()
            
            # Adicionar posições ao ComboBox
            for sigla, nome in posicoes:
                self.posicao_combo.addItem(f"{nome} ({sigla})", sigla)
                
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao carregar posições: {str(e)}")
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'connection' in locals():
                connection.close()

    def submit(self):
        try:
            # Obter a sigla do time e da posição selecionados
            sigla_time = self.time_combo.currentData()
            sigla_posicao = self.posicao_combo.currentData()
            
            if not sigla_time or not sigla_posicao:
                QMessageBox.warning(self, "Aviso", "Selecione um time e uma posição!")
                return

            # Validações básicas
            if not all([
                self.nome_jogador_edit.text(),
                self.idade_edit.text(),
                self.valor_mercado_edit.text()
            ]):
                QMessageBox.warning(self, "Aviso", "Todos os campos são obrigatórios!")
                return

            # Validar idade
            try:
                idade = int(self.idade_edit.text())
                if idade < 15 or idade > 50:
                    raise ValueError("Idade deve estar entre 15 e 50 anos")
            except ValueError as e:
                QMessageBox.warning(self, "Aviso", str(e))
                return

            # Validar valor de mercado
            try:
                valor = float(self.valor_mercado_edit.text().replace(',', '.'))
                if valor < 0:
                    raise ValueError("Valor de mercado não pode ser negativo")
            except ValueError as e:
                QMessageBox.warning(self, "Aviso", "Valor de mercado inválido")
                return

            result = self.crud_elenco.inserir(
                nome_jogador=self.nome_jogador_edit.text(),
                idade=self.idade_edit.text(),
                valor_mercado=self.valor_mercado_edit.text().replace(',', '.'),
                sigla=sigla_time,
                sigla_posicao=sigla_posicao
            )
            QMessageBox.information(self, "Resultado", result)
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Erro", str(e))

class SelectElencoDialog(QDialog):
    def __init__(self, crud_elenco, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Selecionar Jogador")
        self.crud_elenco = crud_elenco
        self.setup_ui()

    def setup_ui(self):
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        self.resize(800, 400)

        # Create search fields
        self.nome_jogador_edit = QLineEdit()
        self.time_combo = QComboBox()
        
        # Carregar times no ComboBox
        self.carregar_times()

        # Add search fields to layout
        self.layout.addWidget(QLabel("Nome do Jogador (opcional):"), 0, 0)
        self.layout.addWidget(self.nome_jogador_edit, 0, 1)
        self.layout.addWidget(QLabel("Time (opcional):"), 1, 0)
        self.layout.addWidget(self.time_combo, 1, 1)

        # Add search button
        search_btn = QPushButton("Buscar")
        search_btn.clicked.connect(self.search)
        self.layout.addWidget(search_btn, 2, 0, 1, 2)

        # Create table
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            "ID", "Nome", "Idade", "Valor Mercado", 
            "Sigla Time", "Nome Clube", "Sigla Posição", "Nome Posição"
        ])
        self.layout.addWidget(self.table, 3, 0, 1, 2)

    def carregar_times(self):
        try:
            # Conectar ao banco de dados
            connection = conecta_bd()
            cursor = connection.cursor()
            
            # Buscar todos os times
            cursor.execute("SELECT sigla, nome_clube FROM time ORDER BY nome_clube")
            times = cursor.fetchall()
            
            # Adicionar opção em branco
            self.time_combo.addItem("Todos os Times", "")
            
            # Adicionar times ao ComboBox
            for sigla, nome in times:
                self.time_combo.addItem(f"{nome} ({sigla})", sigla)
                
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao carregar times: {str(e)}")
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'connection' in locals():
                connection.close()

    def search(self):
        nome_jogador = self.nome_jogador_edit.text() or None
        sigla = self.time_combo.currentData()
        result = self.crud_elenco.selecionar(nome_jogador, sigla)
        
        self.table.setRowCount(0)
        if isinstance(result, str):  # Error message
            QMessageBox.warning(self, "Aviso", result)
            return
            
        for row_idx, row_data in enumerate(result):
            self.table.insertRow(row_idx)
            for col_idx, cell_data in enumerate(row_data):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(cell_data)))

class DeleteElencoDialog(QDialog):
    def __init__(self, crud_elenco, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Deletar Jogador")
        self.crud_elenco = crud_elenco
        self.setup_ui()

    def setup_ui(self):
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        self.resize(400, 200)

        # Create delete fields
        self.nome_jogador_edit = QLineEdit()
        self.time_combo = QComboBox()
        
        # Carregar times no ComboBox
        self.carregar_times()

        # Add fields to layout
        self.layout.addWidget(QLabel("Nome do Jogador:"), 0, 0)
        self.layout.addWidget(self.nome_jogador_edit, 0, 1)
        self.layout.addWidget(QLabel("Time:"), 1, 0)
        self.layout.addWidget(self.time_combo, 1, 1)

        # Add delete button
        delete_btn = QPushButton("Deletar")
        delete_btn.clicked.connect(self.submit)
        self.layout.addWidget(delete_btn, 2, 0, 1, 2)

    def carregar_times(self):
        try:
            # Conectar ao banco de dados
            connection = conecta_bd()
            cursor = connection.cursor()
            
            # Buscar todos os times
            cursor.execute("SELECT sigla, nome_clube FROM time ORDER BY nome_clube")
            times = cursor.fetchall()
            
            # Adicionar times ao ComboBox
            for sigla, nome in times:
                self.time_combo.addItem(f"{nome} ({sigla})", sigla)
                
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao carregar times: {str(e)}")
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'connection' in locals():
                connection.close()

    def submit(self):
        try:
            # Validações básicas
            nome = self.nome_jogador_edit.text()
            sigla = self.time_combo.currentData()
            
            if not nome or not sigla:
                QMessageBox.warning(self, "Aviso", "Nome do jogador e time são obrigatórios!")
                return

            # Confirmação
            resposta = QMessageBox.question(
                self,
                "Confirmar Exclusão",
                f"Tem certeza que deseja deletar o jogador {nome} do time {self.time_combo.currentText()}?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )

            if resposta == QMessageBox.StandardButton.Yes:
                result = self.crud_elenco.deletar(nome_jogador=nome, sigla=sigla)
                QMessageBox.information(self, "Resultado", result)
                self.accept()
            
        except Exception as e:
            QMessageBox.critical(self, "Erro", str(e))

from PyQt6.QtWidgets import (QDialog, QLabel, QLineEdit, QPushButton, 
                           QGridLayout, QMessageBox, QComboBox)
from database import conecta_bd

class UpdateElencoDialog(QDialog):
    def __init__(self, crud_elenco, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Atualizar Jogador")
        self.crud_elenco = crud_elenco
        self.setup_ui()

    def setup_ui(self):
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        self.resize(400, 400)

        # Create time selection ComboBox
        self.time_combo = QComboBox()
        self.jogador_combo = QComboBox()
        
        # Carregar times no ComboBox
        self.carregar_times()

        # Add time selection to layout first
        self.layout.addWidget(QLabel("Selecione o Time:"), 0, 0)
        self.layout.addWidget(self.time_combo, 0, 1)

        # Add jogador selection
        self.layout.addWidget(QLabel("Selecione o Jogador:"), 1, 0)
        self.layout.addWidget(self.jogador_combo, 1, 1)

        # Connect time selection to update jogador list
        self.time_combo.currentIndexChanged.connect(self.carregar_jogadores)

        # Create form fields
        self.nome_jogador_edit = QLineEdit()
        self.idade_edit = QLineEdit()
        self.valor_mercado_edit = QLineEdit()
        
        # Criar ComboBoxes para times e posições
        self.time_edicao_combo = QComboBox()
        self.posicao_combo = QComboBox()
        
        # Carregar dados nos ComboBoxes
        self.carregar_times_edicao()
        self.carregar_posicoes()

        # Connect jogador selection to populate fields
        self.jogador_combo.currentIndexChanged.connect(self.popular_campos)

        # Add labels and fields to layout
        self.layout.addWidget(QLabel("Nome do Jogador:"), 2, 0)
        self.layout.addWidget(self.nome_jogador_edit, 2, 1)
        self.layout.addWidget(QLabel("Idade:"), 3, 0)
        self.layout.addWidget(self.idade_edit, 3, 1)
        self.layout.addWidget(QLabel("Valor de Mercado:"), 4, 0)
        self.layout.addWidget(self.valor_mercado_edit, 4, 1)
        self.layout.addWidget(QLabel("Time:"), 5, 0)
        self.layout.addWidget(self.time_edicao_combo, 5, 1)
        self.layout.addWidget(QLabel("Posição:"), 6, 0)
        self.layout.addWidget(self.posicao_combo, 6, 1)

        # Add submit button
        submit_btn = QPushButton("Atualizar")
        submit_btn.clicked.connect(self.submit)
        self.layout.addWidget(submit_btn, 7, 0, 1, 2)

    def carregar_times(self):
        try:
            connection = conecta_bd()
            cursor = connection.cursor()
            
            cursor.execute("SELECT sigla, nome_clube FROM time ORDER BY nome_clube")
            times = cursor.fetchall()
            
            self.time_combo.clear()
            
            for sigla, nome in times:
                self.time_combo.addItem(f"{nome} ({sigla})", sigla)
                
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao carregar times: {str(e)}")
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'connection' in locals():
                connection.close()

    def carregar_jogadores(self):
        try:
            sigla = self.time_combo.currentData()
            
            self.jogador_combo.clear()
            
            if not sigla:
                return

            connection = conecta_bd()
            cursor = connection.cursor()
            
            cursor.execute("""
                SELECT nome_jogador 
                FROM elenco 
                WHERE sigla = %s 
                ORDER BY nome_jogador
            """, (sigla,))
            jogadores = cursor.fetchall()
            
            for (jogador,) in jogadores:
                self.jogador_combo.addItem(jogador)
                
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao carregar jogadores: {str(e)}")
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'connection' in locals():
                connection.close()

    def carregar_times_edicao(self):
        try:
            connection = conecta_bd()
            cursor = connection.cursor()
            
            cursor.execute("SELECT sigla, nome_clube FROM time ORDER BY nome_clube")
            times = cursor.fetchall()
            
            for sigla, nome in times:
                self.time_edicao_combo.addItem(f"{nome} ({sigla})", sigla)
                
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao carregar times: {str(e)}")
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'connection' in locals():
                connection.close()

    def carregar_posicoes(self):
        try:
            connection = conecta_bd()
            cursor = connection.cursor()
            
            cursor.execute("SELECT sigla_posicao, nome_posicao FROM posicao ORDER BY nome_posicao")
            posicoes = cursor.fetchall()
            
            for sigla, nome in posicoes:
                self.posicao_combo.addItem(f"{nome} ({sigla})", sigla)
                
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao carregar posições: {str(e)}")
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'connection' in locals():
                connection.close()

    def popular_campos(self):
        nome_jogador = self.jogador_combo.currentText()
        sigla_time = self.time_combo.currentData()
        
        if not nome_jogador or not sigla_time:
            self.limpar_campos()
            return

        try:
            connection = conecta_bd()
            cursor = connection.cursor()
            
            cursor.execute("""
                SELECT nome_jogador, idade, valor_mercado, sigla, sigla_posicao
                FROM elenco 
                WHERE nome_jogador = %s AND sigla = %s
            """, (nome_jogador, sigla_time))
            
            resultado = cursor.fetchone()
            
            if resultado:
                self.nome_jogador_edit.setText(str(resultado[0]))
                self.idade_edit.setText(str(resultado[1]))
                self.valor_mercado_edit.setText(str(resultado[2]))
                
                sigla_time_index = self.time_edicao_combo.findData(resultado[3])
                if sigla_time_index != -1:
                    self.time_edicao_combo.setCurrentIndex(sigla_time_index)
                
                sigla_posicao_index = self.posicao_combo.findData(resultado[4])
                if sigla_posicao_index != -1:
                    self.posicao_combo.setCurrentIndex(sigla_posicao_index)
            
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao buscar dados do jogador: {str(e)}")
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'connection' in locals():
                connection.close()

    def limpar_campos(self):
        self.nome_jogador_edit.clear()
        self.idade_edit.clear()
        self.valor_mercado_edit.clear()
        self.time_edicao_combo.setCurrentIndex(0)
        self.posicao_combo.setCurrentIndex(0)

    def submit(self):
        try:
            # Validações básicas
            if not all([
                self.nome_jogador_edit.text(),
                self.idade_edit.text(),
                self.valor_mercado_edit.text()
            ]):
                QMessageBox.warning(self, "Aviso", "Todos os campos são obrigatórios!")
                return

            # Validar idade
            try:
                idade = int(self.idade_edit.text())
                if idade < 15 or idade > 50:
                    raise ValueError("Idade deve estar entre 15 e 50 anos")
            except ValueError as e:
                QMessageBox.warning(self, "Aviso", str(e))
                return

            # Validar valor de mercado
            try:
                valor = float(self.valor_mercado_edit.text().replace(',', '.'))
                if valor < 0:
                    raise ValueError("Valor de mercado não pode ser negativo")
            except ValueError as e:
                QMessageBox.warning(self, "Aviso", "Valor de mercado inválido")
                return

            # Obter siglas do time e posição
            sigla_time = self.time_edicao_combo.currentData()
            sigla_posicao = self.posicao_combo.currentData()

            # Obter o nome original do jogador
            nome_jogador_original = self.jogador_combo.currentText()

            result = self.crud_elenco.atualizar(
                nome_jogador_antigo=nome_jogador_original,
                nome_jogador=self.nome_jogador_edit.text(),
                idade=self.idade_edit.text(),
                valor_mercado=self.valor_mercado_edit.text().replace(',', '.'),
                sigla=sigla_time,
                sigla_posicao=sigla_posicao
            )
            
            QMessageBox.information(self, "Resultado", result)
            
            # Atualizar a lista de jogadores após a atualização
            sigla_atual = self.time_combo.currentData()
            self.carregar_jogadores()
            
            # Se o time não mudou, reselecionar o jogador atualizado
            if sigla_time == sigla_atual:
                novo_nome_index = self.jogador_combo.findText(self.nome_jogador_edit.text())
                if novo_nome_index != -1:
                    self.jogador_combo.setCurrentIndex(novo_nome_index)
            
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Erro", str(e))