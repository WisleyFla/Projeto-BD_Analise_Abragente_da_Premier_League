from PyQt6.QtWidgets import (QDialog, QLabel, QLineEdit, QPushButton, 
                           QGridLayout, QMessageBox, QTableWidget, 
                           QTableWidgetItem, QComboBox)
from PyQt6.QtGui import QRegularExpressionValidator
from PyQt6.QtCore import Qt, QRegularExpression
from database import conecta_bd

class CRUDDialog(QDialog):
    def __init__(self, title, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setModal(True)
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        self.resize(400, 300)

class InsertTimeDialog(CRUDDialog):
    def __init__(self, crud_time, parent=None):
        super().__init__("Inserir Time", parent)
        self.crud_time = crud_time

        # Create form fields
        self.sigla_edit = QLineEdit()
        self.nome_clube_edit = QLineEdit()
        
        # Create date input with mask and validation
        self.fundacao_edit = QLineEdit()
        # Create a regex validator for date format DD/MM/YYYY
        date_validator = QRegularExpressionValidator(QRegularExpression(r'^\d{2}/\d{2}/\d{4}$'))
        self.fundacao_edit.setValidator(date_validator)
        self.fundacao_edit.setPlaceholderText("DD/MM/AAAA")
        
        self.mascote_edit = QLineEdit()
        self.n_titulos_edit = QLineEdit()

        # Add labels and fields to layout
        self.layout.addWidget(QLabel("Sigla:"), 0, 0)
        self.layout.addWidget(self.sigla_edit, 0, 1)
        self.layout.addWidget(QLabel("Nome do Clube:"), 1, 0)
        self.layout.addWidget(self.nome_clube_edit, 1, 1)
        self.layout.addWidget(QLabel("Data de Fundação:"), 2, 0)
        self.layout.addWidget(self.fundacao_edit, 2, 1)
        self.layout.addWidget(QLabel("Mascote:"), 3, 0)
        self.layout.addWidget(self.mascote_edit, 3, 1)
        self.layout.addWidget(QLabel("Número de Títulos:"), 4, 0)
        self.layout.addWidget(self.n_titulos_edit, 4, 1)

        # Add image selection button
        self.select_image_btn = QPushButton("Selecionar Escudo")
        self.select_image_btn.clicked.connect(self.select_image)
        self.layout.addWidget(self.select_image_btn, 5, 0, 1, 2)

        # Add submit button
        submit_btn = QPushButton("Inserir")
        submit_btn.clicked.connect(self.submit)
        self.layout.addWidget(submit_btn, 6, 0, 1, 2)

    def select_image(self):
        self.crud_time.selecionar_imagem()

    def submit(self):
        try:
            # Adicionar validação específica para data
            fundacao = self.fundacao_edit.text()
            
            # Verificar se a data está no formato correto
            if not QRegularExpression(r'^\d{2}/\d{2}/\d{4}$').match(fundacao).hasMatch():
                QMessageBox.warning(self, "Erro", "Formato de data inválido. Use DD/MM/AAAA")
                return
            
            # Tentar converter para confirmar validade
            try:
                dia, mes, ano = map(int, fundacao.split('/'))
                
                # Validações adicionais
                if not (1 <= mes <= 12 and 1 <= dia <= 31 and ano > 0):
                    raise ValueError("Data inválida")
            except ValueError:
                QMessageBox.warning(self, "Erro", "Data inválida. Verifique dia, mês e ano.")
                return

            result = self.crud_time.inserir(
                self.sigla_edit.text(),
                self.nome_clube_edit.text(),
                fundacao,
                self.mascote_edit.text(),
                self.n_titulos_edit.text()
            )
            QMessageBox.information(self, "Resultado", result)
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Erro", str(e))

class SelectTimeDialog(CRUDDialog):
    def __init__(self, crud_time, parent=None):
        super().__init__("Selecionar Time", parent)
        self.crud_time = crud_time

        # Create time selection ComboBox
        self.time_combo = QComboBox()
        self.carregar_times()

        # Add time selection to layout
        self.layout.addWidget(QLabel("Selecione o Time (opcional):"), 0, 0)
        self.layout.addWidget(self.time_combo, 0, 1)

        # Add search button
        search_btn = QPushButton("Buscar")
        search_btn.clicked.connect(self.search)
        self.layout.addWidget(search_btn, 1, 0, 1, 2)

        # Create table
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Sigla", "Nome do Clube", "Fundação", "Mascote", "Nº Títulos"])
        self.layout.addWidget(self.table, 2, 0, 1, 2)

    def carregar_times(self):
        try:
            # Conectar ao banco de dados
            connection = conecta_bd()
            cursor = connection.cursor()
            
            # Adicionar opção de todos os times
            self.time_combo.addItem("Todos os Times", "")
            
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

    def search(self):
        sigla = self.time_combo.currentData()
        result = self.crud_time.selecionar(sigla)
        
        self.table.setRowCount(0)
        if isinstance(result, str):  # Error message
            QMessageBox.warning(self, "Aviso", result)
            return
            
        for row_idx, row_data in enumerate(result):
            self.table.insertRow(row_idx)
            for col_idx, cell_data in enumerate(row_data):
                if cell_data is not None:  # Skip binary data (escudo)
                    self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(cell_data)))

class UpdateTimeDialog(CRUDDialog):
    def __init__(self, crud_time, parent=None):
        super().__init__("Atualizar Time", parent)
        self.crud_time = crud_time

        # Create time selection ComboBox
        self.time_combo = QComboBox()
        self.carregar_times()

        # Create form fields
        self.sigla_edit = QLineEdit()
        self.sigla_edit.setReadOnly(True)  # Make sigla read-only after selection
        
        self.nome_clube_edit = QLineEdit()
        
        # Create date input with mask and validation
        self.fundacao_edit = QLineEdit()
        # Create a regex validator for date format DD/MM/YYYY
        date_validator = QRegularExpressionValidator(QRegularExpression(r'^\d{2}/\d{2}/\d{4}$'))
        self.fundacao_edit.setValidator(date_validator)
        self.fundacao_edit.setPlaceholderText("DD/MM/AAAA")
        
        self.mascote_edit = QLineEdit()
        self.n_titulos_edit = QLineEdit()

        # Add time selection to layout first
        self.layout.addWidget(QLabel("Selecione o Time:"), 0, 0)
        self.layout.addWidget(self.time_combo, 0, 1)

        # Connect time selection to populate fields
        self.time_combo.currentIndexChanged.connect(self.popular_campos)

        # Add fields to layout
        self.layout.addWidget(QLabel("Sigla:"), 1, 0)
        self.layout.addWidget(self.sigla_edit, 1, 1)
        self.layout.addWidget(QLabel("Nome do Clube:"), 2, 0)
        self.layout.addWidget(self.nome_clube_edit, 2, 1)
        self.layout.addWidget(QLabel("Data de Fundação:"), 3, 0)
        self.layout.addWidget(self.fundacao_edit, 3, 1)
        self.layout.addWidget(QLabel("Mascote:"), 4, 0)
        self.layout.addWidget(self.mascote_edit, 4, 1)
        self.layout.addWidget(QLabel("Número de Títulos:"), 5, 0)
        self.layout.addWidget(self.n_titulos_edit, 5, 1)

        # Add image selection button
        self.select_image_btn = QPushButton("Selecionar Escudo")
        self.select_image_btn.clicked.connect(self.select_image)
        self.layout.addWidget(self.select_image_btn, 6, 0, 1, 2)

        # Add submit button
        submit_btn = QPushButton("Atualizar")
        submit_btn.clicked.connect(self.submit)
        self.layout.addWidget(submit_btn, 7, 0, 1, 2)

    def select_image(self):
        self.crud_time.selecionar_imagem()

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

    def popular_campos(self):
        # Obter a sigla do time selecionado
        sigla = self.time_combo.currentData()
        
        if not sigla:
            # Limpar campos se nenhum time for selecionado
            self.sigla_edit.clear()
            self.nome_clube_edit.clear()
            self.fundacao_edit.clear()
            self.mascote_edit.clear()
            self.n_titulos_edit.clear()
            return

        try:
            # Buscar dados do time selecionado
            connection = conecta_bd()
            cursor = connection.cursor()
            
            cursor.execute("""
                SELECT sigla, nome_clube, 
                       TO_CHAR(Fundacao, 'DD/MM/YYYY'), 
                       mascote, n_titulos 
                FROM time 
                WHERE sigla = %s
            """, (sigla,))
            
            resultado = cursor.fetchone()
            
            if resultado:
                # Preencher campos com os dados do time
                self.sigla_edit.setText(str(resultado[0]))
                self.nome_clube_edit.setText(str(resultado[1]))
                self.fundacao_edit.setText(str(resultado[2]))
                self.mascote_edit.setText(str(resultado[3]))
                self.n_titulos_edit.setText(str(resultado[4]))
            
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao buscar dados do time: {str(e)}")
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'connection' in locals():
                connection.close()

    def submit(self):
        try:
            # Adicionar validação específica para data
            fundacao = self.fundacao_edit.text()
            
            # Verificar se a data está no formato correto
            if not QRegularExpression(r'^\d{2}/\d{2}/\d{4}$').match(fundacao).hasMatch():
                QMessageBox.warning(self, "Erro", "Formato de data inválido. Use DD/MM/AAAA")
                return
            
            # Tentar converter para confirmar validade
            try:
                dia, mes, ano = map(int, fundacao.split('/'))
                
                # Validações adicionais
                if not (1 <= mes <= 12 and 1 <= dia <= 31 and ano > 0):
                    raise ValueError("Data inválida")
            except ValueError:
                QMessageBox.warning(self, "Erro", "Data inválida. Verifique dia, mês e ano.")
                return

            result = self.crud_time.atualizar(
                self.sigla_edit.text(),
                self.nome_clube_edit.text(),
                fundacao,
                self.mascote_edit.text(),
                self.n_titulos_edit.text()
            )
            QMessageBox.information(self, "Resultado", result)
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Erro", str(e))

class DeleteTimeDialog(CRUDDialog):
    def __init__(self, crud_time, parent=None):
        super().__init__("Deletar Time", parent)
        self.crud_time = crud_time

        # Create time selection ComboBox
        self.time_combo = QComboBox()
        self.carregar_times()

        # Add time selection to layout
        self.layout.addWidget(QLabel("Selecione o Time:"), 0, 0)
        self.layout.addWidget(self.time_combo, 0, 1)

        # Add delete button
        delete_btn = QPushButton("Deletar")
        delete_btn.clicked.connect(self.submit)
        self.layout.addWidget(delete_btn, 1, 0, 1, 2)

    def carregar_times(self):
        try:
            # Conectar ao banco de dados
            connection = conecta_bd()
            cursor = connection.cursor()
            
            # Buscar todos os times
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
            # Obter a sigla do time selecionado
            sigla = self.time_combo.currentData()
            nome_clube = self.time_combo.currentText()
            
            # Confirmação
            resposta = QMessageBox.question(
                self,
                "Confirmar Exclusão",
                f"Tem certeza que deseja deletar o time {nome_clube}?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )

            if resposta == QMessageBox.StandardButton.Yes:
                result = self.crud_time.deletar(sigla)
                QMessageBox.information(self, "Resultado", result)
                self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Erro", str(e))