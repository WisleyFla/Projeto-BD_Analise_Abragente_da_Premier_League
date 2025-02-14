from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QStyleFactory
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap
import os

# Importações locais
from crud_elenco import CRUDElenco
from crud_time import CRUDTime
from crud_funcionarios import CRUDFuncionario
from elenco_dialogs import InsertElencoDialog,SelectElencoDialog,DeleteElencoDialog,UpdateElencoDialog

from time_dialogs import InsertTimeDialog, SelectTimeDialog, UpdateTimeDialog, DeleteTimeDialog
from funcionarios_dialogs import InsertFuncionarioDialog, SelectFuncionarioDialog, UpdateFuncionarioDialog, DeleteFuncionarioDialog

class CRUDApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        
        # Initialize CRUD instances
        self.crud_elenco = CRUDElenco()
        self.crud_funcionario = CRUDFuncionario()
        self.crud_time = CRUDTime()

        # Create menu bar
        self.create_menu()

    def setup_ui(self):
        """Configura a interface do usuário"""
        self.setWindowTitle("Sistema de Gerenciamento - Premier League")
        self.resize(1000, 600)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #000000;  /* Azul escuro */
            }
            QLabel {
                font-size: 16px;
                color: #ffffff;
            }
            QPushButton {
                background-color: #1E3A5F;  /* Azul médio */
                color: white;
                padding: 5px 15px;
                border: none;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #2D4E7E;  /* Azul mais claro para hover */
            }
            QMenuBar {
                background-color: #1E3A5F;  /* Azul médio */
                color: white;
            }
            QMenuBar::item {
                background-color: transparent;
                padding: 8px 20px;
            }
            QMenuBar::item:selected {
                background-color: #2D4E7E;  /* Azul mais claro */
            }
            QMenu {
                background-color: #1E3A5F;  /* Azul médio */
                color: white;
                border: none;
            }
            QMenu::item:selected {
                background-color: #2D4E7E;  /* Azul mais claro */
            }
            QDialog {
                background-color: #0A1929;  /* Azul escuro */
            }
            QTableWidget {
                background-color: #1E3A5F;  /* Azul médio */
                color: white;
                gridline-color: #2D4E7E;  /* Azul mais claro */
            }
            QHeaderView::section {
                background-color: #2D4E7E;  /* Azul mais claro */
                color: white;
                padding: 5px;
            }
            QTableWidget::item:selected {
                background-color: #3A5F8E;  /* Azul ainda mais claro para seleção */
            }
            QLineEdit, QSpinBox, QComboBox {
                background-color: #1E3A5F;  /* Azul médio */
                color: white;
                border: 1px solid #2D4E7E;  /* Azul mais claro */
                padding: 5px;
                border-radius: 3px;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid none;
                border-right: 5px solid none;
                border-top: 5px solid white;
                width: 0;
                height: 0;
                margin-right: 5px;
            }
        """)

        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Add Premier League logo
        logo_label = QLabel()
        try:
            # Tenta diferentes caminhos para a imagem
            possible_paths = [
                "premier_league_logo.png",
                "premier_league_logo.jpg",
                "premier_league_logo.jpeg",
                "images/premier_league_logo.png",
                "images/premier_league_logo.jpg",
                "images/premier_league_logo.jpeg",
                os.path.join(os.path.dirname(__file__), "premier_league_logo.png"),
                os.path.join(os.path.dirname(__file__), "premier_league_logo.jpg"),
                os.path.join(os.path.dirname(__file__), "premier_league_logo.jpeg"),
                os.path.join(os.path.dirname(__file__), "images", "premier_league_logo.png"),
                os.path.join(os.path.dirname(__file__), "images", "premier_league_logo.jpg"),
                os.path.join(os.path.dirname(__file__), "images", "premier_league_logo.jpeg")
            ]
            
            pixmap = None
            for path in possible_paths:
                if os.path.exists(path):
                    pixmap = QPixmap(path)
                    if not pixmap.isNull():
                        break

            if pixmap and not pixmap.isNull():
                scaled_pixmap = pixmap.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                logo_label.setPixmap(scaled_pixmap)
            else:
                raise FileNotFoundError("Não foi possível carregar a imagem da logo")
                
        except Exception as e:
            print(f"Erro ao carregar a imagem: {e}")
            # Se falhar ao carregar a imagem, mostra um texto alternativo
            logo_label.setText("Premier League")
            logo_font = QFont("Arial", 32)
            logo_font.setBold(True)
            logo_label.setFont(logo_font)
            logo_label.setStyleSheet("color: white; margin: 20px;")

        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(logo_label)

        # Add welcome label with custom font
        welcome_label = QLabel("Bem-vindo ao Sistema de Gerenciamento\nPremier League")
        welcome_font = QFont("Arial", 24)
        welcome_font.setBold(True)
        welcome_label.setFont(welcome_font)
        welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(welcome_label)

        # Add subtitle
        subtitle = QLabel("Gerenciamento de Times, Elenco e Funcionários")
        subtitle_font = QFont("Arial", 14)
        subtitle.setFont(subtitle_font)
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(subtitle)

        # Add instructions
        instructions = QLabel(
            "\nInstruções:\n\n"
            "Use o menu 'Time' para gerenciar os times da Premier League\n"
            "Use o menu 'Elenco' para gerenciar os jogadores\n"
            "Use o menu 'Funcionários' para gerenciar a equipe técnica\n"
        )
        instructions.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(instructions)

    def create_menu(self):
        """Cria a barra de menu com todas as opções"""
        menubar = self.menuBar()

        # Time menu
        time_menu = menubar.addMenu("Time")
        time_menu.addAction("Inserir", lambda: InsertTimeDialog(self.crud_time, self).exec())
        time_menu.addAction("Visualizar", lambda: SelectTimeDialog(self.crud_time, self).exec())
        time_menu.addAction("Atualizar", lambda: UpdateTimeDialog(self.crud_time, self).exec())
        time_menu.addAction("Deletar", lambda: DeleteTimeDialog(self.crud_time, self).exec())

        # Elenco menu
        elenco_menu = menubar.addMenu("Elenco")
        elenco_menu.addAction("Inserir", lambda: InsertElencoDialog(self.crud_elenco, self).exec())
        elenco_menu.addAction("Visualizar", lambda: SelectElencoDialog(self.crud_elenco, self).exec())
        elenco_menu.addAction("Atualizar", lambda: UpdateElencoDialog(self.crud_elenco, self).exec())
        elenco_menu.addAction("Deletar", lambda: DeleteElencoDialog(self.crud_elenco, self).exec())

        # Funcionários menu
        funcionario_menu = menubar.addMenu("Funcionários")
        funcionario_menu.addAction("Inserir", lambda: InsertFuncionarioDialog(self.crud_funcionario, self).exec())
        funcionario_menu.addAction("Visualizar", lambda: SelectFuncionarioDialog(self.crud_funcionario, self).exec())
        funcionario_menu.addAction("Atualizar", lambda: UpdateFuncionarioDialog(self.crud_funcionario, self).exec())
        funcionario_menu.addAction("Deletar", lambda: DeleteFuncionarioDialog(self.crud_funcionario, self).exec())

def main():
    import sys
    
    # Create application
    app = QApplication(sys.argv)
    
    # Set application-wide style
    app.setStyle(QStyleFactory.create('Fusion'))
    
    # Create and show the main window
    window = CRUDApp()
    window.show()
    
    # Start the event loop
    sys.exit(app.exec())

if __name__ == "__main__":
    main()