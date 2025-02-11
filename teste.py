import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

# Supondo que as classes CRUDElenco, CRUDFuncionario e CRUDTime estejam em arquivos separados
from crud_elenco import CRUDElenco
from crud_funcionario import CRUDFuncionario
from crud_time import CRUDTime

class CRUDApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gerenciamento")
        self.root.geometry("400x300")

        # Inicializa as instâncias das classes CRUD
        self.crud_elenco = CRUDElenco()
        self.crud_funcionario = CRUDFuncionario()
        self.crud_time = CRUDTime()

        # Cria o menu principal
        self.create_menu()

    def create_menu(self):
        menubar = tk.Menu(self.root)

        # Menu Elenco
        elenco_menu = tk.Menu(menubar, tearoff=0)
        elenco_menu.add_command(label="Inserir", command=self.open_inserir_elenco)
        elenco_menu.add_command(label="Selecionar", command=self.open_selecionar_elenco)
        elenco_menu.add_command(label="Atualizar", command=self.open_atualizar_elenco)
        elenco_menu.add_command(label="Deletar", command=self.open_deletar_elenco)
        menubar.add_cascade(label="Elenco", menu=elenco_menu)

        # Menu Funcionário
        funcionario_menu = tk.Menu(menubar, tearoff=0)
        funcionario_menu.add_command(label="Inserir", command=self.open_inserir_funcionario)
        funcionario_menu.add_command(label="Selecionar", command=self.open_selecionar_funcionario)
        funcionario_menu.add_command(label="Atualizar", command=self.open_atualizar_funcionario)
        funcionario_menu.add_command(label="Deletar", command=self.open_deletar_funcionario)
        menubar.add_cascade(label="Funcionário", menu=funcionario_menu)

        # Menu Time
        time_menu = tk.Menu(menubar, tearoff=0)
        time_menu.add_command(label="Inserir", command=self.open_inserir_time)
        time_menu.add_command(label="Selecionar", command=self.open_selecionar_time)
        time_menu.add_command(label="Atualizar", command=self.open_atualizar_time)
        time_menu.add_command(label="Deletar", command=self.open_deletar_time)
        menubar.add_cascade(label="Time", menu=time_menu)

        self.root.config(menu=menubar)

    def open_inserir_elenco(self):
        self.open_crud_window("Inserir Elenco", self.crud_elenco.inserir)

    def open_selecionar_elenco(self):
        self.open_crud_window("Selecionar Elenco", self.crud_elenco.selecionar)

    def open_atualizar_elenco(self):
        self.open_crud_window("Atualizar Elenco", self.crud_elenco.atualizar)

    def open_deletar_elenco(self):
        self.open_crud_window("Deletar Elenco", self.crud_elenco.deletar)

    def open_inserir_funcionario(self):
        self.open_crud_window("Inserir Funcionário", self.crud_funcionario.inserir)

    def open_selecionar_funcionario(self):
        self.open_crud_window("Selecionar Funcionário", self.crud_funcionario.selecionar)

    def open_atualizar_funcionario(self):
        self.open_crud_window("Atualizar Funcionário", self.crud_funcionario.atualizar)

    def open_deletar_funcionario(self):
        self.open_crud_window("Deletar Funcionário", self.crud_funcionario.deletar)

    def open_inserir_time(self):
        self.open_crud_window("Inserir Time", self.crud_time.inserir)

    def open_selecionar_time(self):
        self.open_crud_window("Selecionar Time", self.crud_time.selecionar)

    def open_atualizar_time(self):
        self.open_crud_window("Atualizar Time", self.crud_time.atualizar)

    def open_deletar_time(self):
        self.open_crud_window("Deletar Time", self.crud_time.deletar)

    def open_crud_window(self, title, crud_function):
        window = tk.Toplevel(self.root)
        window.title(title)

        # Aqui você pode adicionar os campos de entrada necessários para a operação CRUD
        # Por exemplo, para inserir um jogador no elenco:
        if title == "Inserir Elenco":
            tk.Label(window, text="ID Jogador:").grid(row=0, column=0)
            id_jogador_entry = tk.Entry(window)
            id_jogador_entry.grid(row=0, column=1)

            tk.Label(window, text="Nome Jogador:").grid(row=1, column=0)
            nome_jogador_entry = tk.Entry(window)
            nome_jogador_entry.grid(row=1, column=1)

            tk.Label(window, text="Idade:").grid(row=2, column=0)
            idade_entry = tk.Entry(window)
            idade_entry.grid(row=2, column=1)

            tk.Label(window, text="Valor Mercado:").grid(row=3, column=0)
            valor_mercado_entry = tk.Entry(window)
            valor_mercado_entry.grid(row=3, column=1)

            tk.Label(window, text="Sigla:").grid(row=4, column=0)
            sigla_entry = tk.Entry(window)
            sigla_entry.grid(row=4, column=1)

            tk.Label(window, text="Sigla Posição:").grid(row=5, column=0)
            sigla_posicao_entry = tk.Entry(window)
            sigla_posicao_entry.grid(row=5, column=1)

            def submit():
                id_jogador = id_jogador_entry.get()
                nome_jogador = nome_jogador_entry.get()
                idade = idade_entry.get()
                valor_mercado = valor_mercado_entry.get()
                sigla = sigla_entry.get()
                sigla_posicao = sigla_posicao_entry.get()

                result = crud_function(id_jogador, nome_jogador, idade, valor_mercado, sigla, sigla_posicao)
                messagebox.showinfo("Resultado", result)

            tk.Button(window, text="Submit", command=submit).grid(row=6, column=0, columnspan=2)

        # Adicione condições semelhantes para outras operações CRUD

if __name__ == "__main__":
    root = tk.Tk()
    app = CRUDApp(root)
    root.mainloop()