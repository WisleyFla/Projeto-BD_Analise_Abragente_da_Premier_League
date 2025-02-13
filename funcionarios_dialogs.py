from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QPushButton, QSpinBox, QComboBox, QMessageBox, QTableWidget,
    QTableWidgetItem, QWidget
)
from PyQt6.QtCore import Qt

class InsertFuncionarioDialog(QDialog):
    def __init__(self, crud_funcionario, parent=None):
        super().__init__(parent)
        self.crud_funcionario = crud_funcionario
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Inserir Funcionário")
        layout = QVBoxLayout(self)

        # Nome
        self.nome_edit = QLineEdit()
        layout.addWidget(QLabel("Nome:"))
        layout.addWidget(self.nome_edit)

        # Idade
        self.idade_spin = QSpinBox()
        self.idade_spin.setRange(18, 100)
        layout.addWidget(QLabel("Idade:"))
        layout.addWidget(self.idade_spin)

        # Profissão
        self.profissao_edit = QLineEdit()
        layout.addWidget(QLabel("Profissão:"))
        layout.addWidget(self.profissao_edit)

        # Departamento
        self.departamento_combo = QComboBox()
        self.load_departamentos()
        layout.addWidget(QLabel("Departamento:"))
        layout.addWidget(self.departamento_combo)

        # Time
        self.time_combo = QComboBox()
        self.load_times()
        layout.addWidget(QLabel("Time:"))
        layout.addWidget(self.time_combo)

        # Buttons
        button_layout = QHBoxLayout()
        save_button = QPushButton("Salvar")
        save_button.clicked.connect(self.save_funcionario)
        cancel_button = QPushButton("Cancelar")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)

    def load_departamentos(self):
        try:
            self.crud_funcionario.cursor.execute("""
                SELECT sigla_departamento, nome_departamento 
                FROM departamentos
                ORDER BY nome_departamento
            """)
            departamentos = self.crud_funcionario.cursor.fetchall()
            self.departamento_combo.clear()
            for sigla, nome in departamentos:
                self.departamento_combo.addItem(nome, sigla)
        except Exception as e:
            print(f"Erro ao carregar departamentos: {e}")

    def load_times(self):
        try:
            self.crud_funcionario.cursor.execute("""
                SELECT sigla, nome_clube 
                FROM time
                ORDER BY nome_clube
            """)
            times = self.crud_funcionario.cursor.fetchall()
            self.time_combo.clear()
            for sigla, nome in times:
                self.time_combo.addItem(nome, sigla)
        except Exception as e:
            print(f"Erro ao carregar times: {e}")

    def save_funcionario(self):
        nome = self.nome_edit.text()
        idade = self.idade_spin.value()
        profissao = self.profissao_edit.text()
        departamento = self.departamento_combo.currentData()
        time = self.time_combo.currentData()

        if not all([nome, profissao, departamento, time]):
            QMessageBox.warning(self, "Erro", "Todos os campos são obrigatórios!")
            return

        result = self.crud_funcionario.inserir(nome, idade, profissao, departamento, time)
        QMessageBox.information(self, "Resultado", result)
        if "sucesso" in result.lower():
            self.accept()

class SelectFuncionarioDialog(QDialog):
    def __init__(self, crud_funcionario, parent=None):
        super().__init__(parent)
        self.crud_funcionario = crud_funcionario
        self.setup_ui()
        self.load_funcionarios()

    def setup_ui(self):
        self.setWindowTitle("Visualizar Funcionários")
        self.setMinimumWidth(800)
        layout = QVBoxLayout(self)

        # Search fields
        search_layout = QHBoxLayout()
        self.search_name = QLineEdit()
        self.search_name.setPlaceholderText("Buscar por nome...")
        self.search_name.textChanged.connect(self.load_funcionarios)
        search_layout.addWidget(self.search_name)
        layout.addLayout(search_layout)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "Matrícula", "Nome", "Idade", "Profissão", 
            "Departamento", "Time"
        ])
        layout.addWidget(self.table)

        # Close button
        close_button = QPushButton("Fechar")
        close_button.clicked.connect(self.accept)
        layout.addWidget(close_button)

    def load_funcionarios(self):
        search_name = self.search_name.text()
        funcionarios = self.crud_funcionario.selecionar(nome=search_name if search_name else None)
        
        self.table.setRowCount(0)
        if isinstance(funcionarios, str):  # Se for uma mensagem de erro
            QMessageBox.warning(self, "Erro", funcionarios)
            return
            
        for row, func in enumerate(funcionarios):
            self.table.insertRow(row)
            for col, value in enumerate(func):
                item = QTableWidgetItem(str(value))
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.table.setItem(row, col, item)

class UpdateFuncionarioDialog(QDialog):
    def __init__(self, crud_funcionario, parent=None):
        super().__init__(parent)
        self.crud_funcionario = crud_funcionario
        self.selected_matricula = None
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Atualizar Funcionário")
        self.setMinimumWidth(800)
        layout = QVBoxLayout(self)

        # Search section
        search_layout = QHBoxLayout()
        self.search_name = QLineEdit()
        self.search_name.setPlaceholderText("Buscar por nome...")
        self.search_name.textChanged.connect(self.load_funcionarios)
        search_layout.addWidget(self.search_name)
        layout.addLayout(search_layout)

        # Table for selecting employee
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "Matrícula", "Nome", "Idade", "Profissão", 
            "Departamento", "Time"
        ])
        self.table.itemClicked.connect(self.employee_selected)
        layout.addWidget(self.table)

        # Update form (initially hidden)
        self.update_form = QWidget()
        form_layout = QVBoxLayout(self.update_form)

        # Fields for updating
        self.nome_edit = QLineEdit()
        form_layout.addWidget(QLabel("Nome:"))
        form_layout.addWidget(self.nome_edit)

        self.idade_spin = QSpinBox()
        self.idade_spin.setRange(18, 100)
        form_layout.addWidget(QLabel("Idade:"))
        form_layout.addWidget(self.idade_spin)

        self.profissao_edit = QLineEdit()
        form_layout.addWidget(QLabel("Profissão:"))
        form_layout.addWidget(self.profissao_edit)

        # Departamento
        self.departamento_combo = QComboBox()
        self.load_departamentos()
        form_layout.addWidget(QLabel("Departamento:"))
        form_layout.addWidget(self.departamento_combo)

        # Time
        self.time_combo = QComboBox()
        self.load_times()
        form_layout.addWidget(QLabel("Time:"))
        form_layout.addWidget(self.time_combo)

        # Buttons
        button_layout = QHBoxLayout()
        save_button = QPushButton("Salvar")
        save_button.clicked.connect(self.update_funcionario)
        cancel_button = QPushButton("Cancelar")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)
        form_layout.addLayout(button_layout)

        self.update_form.hide()
        layout.addWidget(self.update_form)

        self.load_funcionarios()

    def load_departamentos(self):
        try:
            self.crud_funcionario.cursor.execute("""
                SELECT sigla_departamento, nome_departamento 
                FROM departamentos
                ORDER BY nome_departamento
            """)
            departamentos = self.crud_funcionario.cursor.fetchall()
            self.departamento_combo.clear()
            for sigla, nome in departamentos:
                self.departamento_combo.addItem(nome, sigla)
        except Exception as e:
            print(f"Erro ao carregar departamentos: {e}")

    def load_times(self):
        try:
            self.crud_funcionario.cursor.execute("""
                SELECT sigla, nome_clube 
                FROM time
                ORDER BY nome_clube
            """)
            times = self.crud_funcionario.cursor.fetchall()
            self.time_combo.clear()
            for sigla, nome in times:
                self.time_combo.addItem(nome, sigla)
        except Exception as e:
            print(f"Erro ao carregar times: {e}")

    def load_funcionarios(self):
        search_name = self.search_name.text()
        funcionarios = self.crud_funcionario.selecionar(nome=search_name if search_name else None)
        
        self.table.setRowCount(0)
        if isinstance(funcionarios, str):  # Se for uma mensagem de erro
            QMessageBox.warning(self, "Erro", funcionarios)
            return
            
        for row, func in enumerate(funcionarios):
            self.table.insertRow(row)
            for col, value in enumerate(func):
                item = QTableWidgetItem(str(value))
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.table.setItem(row, col, item)

    def employee_selected(self, item):
        row = item.row()
        self.selected_matricula = int(self.table.item(row, 0).text())
        
        # Fill update form with selected employee data
        self.nome_edit.setText(self.table.item(row, 1).text())
        self.idade_spin.setValue(int(self.table.item(row, 2).text()))
        self.profissao_edit.setText(self.table.item(row, 3).text())
        
        # Find and set the correct index for department and team
        dept_name = self.table.item(row, 4).text()
        team_name = self.table.item(row, 5).text()
        
        # Set department
        for i in range(self.departamento_combo.count()):
            if self.departamento_combo.itemText(i) == dept_name:
                self.departamento_combo.setCurrentIndex(i)
                break
                
        # Set team
        for i in range(self.time_combo.count()):
            if self.time_combo.itemText(i) == team_name:
                self.time_combo.setCurrentIndex(i)
                break
        
        self.update_form.show()

    def update_funcionario(self):
        if not self.selected_matricula:
            return

        result = self.crud_funcionario.atualizar(
            self.selected_matricula,
            self.selected_matricula,  # Keep same matricula
            self.nome_edit.text(),
            self.idade_spin.value(),
            self.profissao_edit.text(),
            self.departamento_combo.currentData(),
            self.time_combo.currentData()
        )
        
        QMessageBox.information(self, "Resultado", result)
        if "sucesso" in result.lower():
            self.load_funcionarios()
            self.update_form.hide()

class DeleteFuncionarioDialog(QDialog):
    def __init__(self, crud_funcionario, parent=None):
        super().__init__(parent)
        self.crud_funcionario = crud_funcionario
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Deletar Funcionário")
        self.setMinimumWidth(800)
        layout = QVBoxLayout(self)

        # Search field
        search_layout = QHBoxLayout()
        self.search_name = QLineEdit()
        self.search_name.setPlaceholderText("Buscar por nome...")
        self.search_name.textChanged.connect(self.load_funcionarios)
        search_layout.addWidget(self.search_name)
        layout.addLayout(search_layout)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "Matrícula", "Nome", "Idade", "Profissão", 
            "Departamento", "Time"
        ])
        layout.addWidget(self.table)

        # Buttons
        button_layout = QHBoxLayout()
        delete_button = QPushButton("Deletar Selecionado")
        delete_button.clicked.connect(self.delete_selected)
        cancel_button = QPushButton("Cancelar")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(delete_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)

        self.load_funcionarios()

    def load_funcionarios(self):
        search_name = self.search_name.text()
        funcionarios = self.crud_funcionario.selecionar(nome=search_name if search_name else None)
        
        self.table.setRowCount(0)
        if isinstance(funcionarios, str):  # Se for uma mensagem de erro
            QMessageBox.warning(self, "Erro", funcionarios)
            return
            
        for row, func in enumerate(funcionarios):
            self.table.insertRow(row)
            for col, value in enumerate(func):
                item = QTableWidgetItem(str(value))
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.table.setItem(row, col, item)

    def delete_selected(self):
        selected_items = self.table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Erro", "Por favor, selecione um funcionário para deletar!")
            return

        row = selected_items[0].row()
        matricula = int(self.table.item(row, 0).text())
        nome = self.table.item(row, 1).text()

        reply = QMessageBox.question(
            self,
            "Confirmar Exclusão",
            f"Tem certeza que deseja deletar o funcionário {nome}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            result = self.crud_funcionario.deletar(matricula)
            QMessageBox.information(self, "Resultado", result)
            if "sucesso" in result.lower():
                self.load_funcionarios()