import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

# Supondo que as classes CRUDElenco, CRUDFuncionario e CRUDTime estejam em arquivos separados
from crud_elenco import CRUDElenco
from crud_funcionarios import CRUDFuncionario
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
        window = tk.Toplevel(self.root)
        window.title("Inserir Elenco")

        # Campos de entrada
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
            # Coletar dados dos campos de entrada
            id_jogador = id_jogador_entry.get()
            nome_jogador = nome_jogador_entry.get()
            idade = idade_entry.get()
            valor_mercado = valor_mercado_entry.get()
            sigla = sigla_entry.get()
            sigla_posicao = sigla_posicao_entry.get()

            # Chamar o método inserir da classe CRUDElenco
            resultado = self.crud_elenco.inserir(id_jogador, nome_jogador, idade, valor_mercado, sigla, sigla_posicao)

            # Exibir resultado em uma messagebox
            messagebox.showinfo("Resultado", resultado)

        # Botão para submeter os dados
        tk.Button(window, text="Submit", command=submit).grid(row=6, column=0, columnspan=2)

    def open_selecionar_elenco(self):
        window = tk.Toplevel(self.root)
        window.title("Selecionar Jogador")

        tk.Label(window, text="ID do Jogador (opcional):").grid(row=0, column=0)
        id_jogador_entry = tk.Entry(window)
        id_jogador_entry.grid(row=0, column=1)

        def submit():
            id_jogador = id_jogador_entry.get() or None
            result = self.crud_elenco.selecionar(id_jogador)

            # Verifica se há resultados
            if not result:
                messagebox.showinfo("Resultado", "Nenhum jogador encontrado.")
                return

            # Cria uma nova janela para exibir a tabela
            table_window = tk.Toplevel(window)
            table_window.title("Resultados da Consulta")

            # Cria a Treeview (tabela)
            columns = ("ID", "Nome", "Idade", "Valor de Mercado", "Sigla", "Sigla Posição")
            tree = ttk.Treeview(table_window, columns=columns, show="headings")

            # Define os cabeçalhos das colunas
            for col in columns:
                tree.heading(col, text=col)

            # Insere os dados na tabela
            for row in result:
                tree.insert("", "end", values=row)

            # Adiciona a tabela à janela
            tree.grid(row=0, column=0, sticky="nsew")

            # Adiciona uma barra de rolagem
            scrollbar = ttk.Scrollbar(table_window, orient="vertical", command=tree.yview)
            tree.configure(yscroll=scrollbar.set)
            scrollbar.grid(row=0, column=1, sticky="ns")

        tk.Button(window, text="Selecionar", command=submit).grid(row=1, column=0, columnspan=2)

    def open_atualizar_elenco(self):
        window = tk.Toplevel(self.root)
        window.title("Atualizar Jogador")

        tk.Label(window, text="ID do Jogador:").grid(row=0, column=0)
        id_jogador_entry = tk.Entry(window)
        id_jogador_entry.grid(row=0, column=1)

        tk.Label(window, text="Nome do Jogador:").grid(row=1, column=0)
        nome_jogador_entry = tk.Entry(window)
        nome_jogador_entry.grid(row=1, column=1)

        tk.Label(window, text="Idade:").grid(row=2, column=0)
        idade_entry = tk.Entry(window)
        idade_entry.grid(row=2, column=1)

        tk.Label(window, text="Valor de Mercado:").grid(row=3, column=0)
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

            result = self.crud_elenco.atualizar(id_jogador, nome_jogador, idade, valor_mercado, sigla, sigla_posicao)
            messagebox.showinfo("Resultado", result)

        tk.Button(window, text="Atualizar", command=submit).grid(row=6, column=0, columnspan=2)

    def open_deletar_elenco(self):
        window = tk.Toplevel(self.root)
        window.title("Deletar Jogador")

        tk.Label(window, text="ID do Jogador:").grid(row=0, column=0)
        id_jogador_entry = tk.Entry(window)
        id_jogador_entry.grid(row=0, column=1)

        def submit():
            id_jogador = id_jogador_entry.get()
            result = self.crud_elenco.deletar(id_jogador)
            messagebox.showinfo("Resultado", result)

        tk.Button(window, text="Deletar", command=submit).grid(row=1, column=0, columnspan=2)

    def open_inserir_funcionario(self):
        window = tk.Toplevel(self.root)
        window.title("Inserir Funcionário")

        # Campos de entrada
        tk.Label(window, text="Matrícula:").grid(row=0, column=0)
        matricula_entry = tk.Entry(window)
        matricula_entry.grid(row=0, column=1)

        tk.Label(window, text="Nome:").grid(row=1, column=0)
        nome_funcionario_entry = tk.Entry(window)
        nome_funcionario_entry.grid(row=1, column=1)

        tk.Label(window, text="Idade:").grid(row=2, column=0)
        idade_entry = tk.Entry(window)
        idade_entry.grid(row=2, column=1)

        tk.Label(window, text="Profissão:").grid(row=3, column=0)
        profissao_entry = tk.Entry(window)
        profissao_entry.grid(row=3, column=1)

        tk.Label(window, text="Sigla do Departamento:").grid(row=4, column=0)
        sigla_departamento_entry = tk.Entry(window)
        sigla_departamento_entry.grid(row=4, column=1)

        tk.Label(window, text="Sigla do Time:").grid(row=5, column=0)
        sigla_time_entry = tk.Entry(window)
        sigla_time_entry.grid(row=5, column=1)

        def submit():
            try:
                # Coletar dados dos campos de entrada
                matricula = matricula_entry.get()
                nome_funcionario = nome_funcionario_entry.get()
                idade = idade_entry.get()
                profissao = profissao_entry.get()
                sigla_departamento = sigla_departamento_entry.get()
                sigla_time = sigla_time_entry.get()

                # Validar se todos os campos foram preenchidos
                if not all([matricula, nome_funcionario, idade, profissao, sigla_departamento, sigla_time]):
                    raise ValueError("Todos os campos devem ser preenchidos!")

                # Validar se idade é um número
                if not idade.isdigit():
                    raise ValueError("A idade deve ser um número inteiro!")

                # Chamar o método inserir da classe CRUDFuncionario
                resultado = self.crud_funcionario.inserir(matricula, nome_funcionario, int(idade), profissao, sigla_departamento, sigla_time)

                # Exibir resultado em uma messagebox
                messagebox.showinfo("Resultado", resultado)

            except ValueError as ve:
                messagebox.showerror("Erro de Validação", str(ve))
            except Exception as e:
                messagebox.showerror("Erro", f"Ocorreu um erro ao processar a solicitação: {str(e)}")

            # Botão para submeter os dados
        tk.Button(window, text="Submit", command=submit).grid(row=6, column=0, columnspan=2)

    def open_selecionar_funcionario(self):
        window = tk.Toplevel(self.root)
        window.title("Selecionar Funcionário")

        tk.Label(window, text="Matrícula do Funcionário (opcional):").grid(row=0, column=0)
        matricula_entry = tk.Entry(window)
        matricula_entry.grid(row=0, column=1)

        def submit():
            matricula = matricula_entry.get() or None
            result = self.crud_funcionario.selecionar(matricula)

            # Verifica se há resultados
            if not result:
                messagebox.showinfo("Resultado", "Nenhum funcionário encontrado.")
                return

            # Cria uma nova janela para exibir a tabela
            table_window = tk.Toplevel(window)
            table_window.title("Resultados da Consulta")

            # Cria a Treeview (tabela)
            columns = ("Matrícula", "Nome", "Idade", "Profissão", "Sigla do Departamento", "Sigla do Time")
            tree = ttk.Treeview(table_window, columns=columns, show="headings")

            # Define os cabeçalhos das colunas
            for col in columns:
                tree.heading(col, text=col)

            # Insere os dados na tabela
            for row in result:
                tree.insert("", "end", values=row)

            # Adiciona a tabela à janela
            tree.grid(row=0, column=0, sticky="nsew")

            # Adiciona uma barra de rolagem
            scrollbar = ttk.Scrollbar(table_window, orient="vertical", command=tree.yview)
            tree.configure(yscroll=scrollbar.set)
            scrollbar.grid(row=0, column=1, sticky="ns")

        tk.Button(window, text="Selecionar", command=submit).grid(row=1, column=0, columnspan=2)

    def open_atualizar_funcionario(self):
        window = tk.Toplevel(self.root)
        window.title("Atualizar Funcionário")

        # Campos de entrada
        tk.Label(window, text="Matrícula:").grid(row=0, column=0)
        matricula_entry = tk.Entry(window)
        matricula_entry.grid(row=0, column=1)

        tk.Label(window, text="Nome:").grid(row=1, column=0)
        nome_funcionario_entry = tk.Entry(window)
        nome_funcionario_entry.grid(row=1, column=1)

        tk.Label(window, text="Idade:").grid(row=2, column=0)
        idade_entry = tk.Entry(window)
        idade_entry.grid(row=2, column=1)

        tk.Label(window, text="Profissão:").grid(row=3, column=0)
        profissao_entry = tk.Entry(window)
        profissao_entry.grid(row=3, column=1)

        tk.Label(window, text="Sigla do Departamento:").grid(row=4, column=0)
        sigla_departamento_entry = tk.Entry(window)
        sigla_departamento_entry.grid(row=4, column=1)

        tk.Label(window, text="Sigla do Time:").grid(row=5, column=0)
        sigla_time_entry = tk.Entry(window)
        sigla_time_entry.grid(row=5, column=1)

        def submit():
            try:
                # Coletar dados dos campos de entrada
                matricula = matricula_entry.get()
                nome_funcionario = nome_funcionario_entry.get()
                idade = idade_entry.get()
                profissao = profissao_entry.get()
                sigla_departamento = sigla_departamento_entry.get()
                sigla_time = sigla_time_entry.get()

                # Validar se todos os campos foram preenchidos
                if not all([matricula, nome_funcionario, idade, profissao, sigla_departamento, sigla_time]):
                    raise ValueError("Todos os campos devem ser preenchidos!")

                # Validar se idade é um número
                if not idade.isdigit():
                    raise ValueError("A idade deve ser um número inteiro!")

                # Chamar o método atualizar da classe CRUDFuncionario
                resultado = self.crud_funcionario.atualizar(matricula, nome_funcionario, int(idade), profissao, sigla_departamento, sigla_time)

                # Exibir resultado em uma messagebox
                messagebox.showinfo("Resultado", resultado)

            except ValueError as ve:
                messagebox.showerror("Erro de Validação", str(ve))
            except Exception as e:
                messagebox.showerror("Erro", f"Ocorreu um erro ao processar a solicitação: {str(e)}")

        # Botão para submeter os dados
        tk.Button(window, text="Atualizar", command=submit).grid(row=6, column=0, columnspan=2)

    def open_deletar_funcionario(self):
        window = tk.Toplevel(self.root)
        window.title("Deletar Funcionário")

        tk.Label(window, text="Matrícula:").grid(row=0, column=0)
        matricula_entry = tk.Entry(window)
        matricula_entry.grid(row=0, column=1)

        def submit():
            matricula = matricula_entry.get()
            resultado = self.crud_funcionario.deletar(matricula)
            messagebox.showinfo("Resultado", resultado)

        tk.Button(window, text="Deletar", command=submit).grid(row=1, column=0, columnspan=2)

    def open_inserir_time(self):
        window = tk.Toplevel(self.root)
        window.title("Inserir Time")

        tk.Label(window, text="Sigla:").grid(row=0, column=0)
        sigla_entry = tk.Entry(window)
        sigla_entry.grid(row=0, column=1)

        tk.Label(window, text="Nome do Clube:").grid(row=1, column=0)
        nome_clube_entry = tk.Entry(window)
        nome_clube_entry.grid(row=1, column=1)

        tk.Label(window, text="Ano de Fundação:").grid(row=2, column=0)
        fundacao_entry = tk.Entry(window)
        fundacao_entry.grid(row=2, column=1)

        tk.Label(window, text="Mascote:").grid(row=3, column=0)
        mascote_entry = tk.Entry(window)
        mascote_entry.grid(row=3, column=1)

        tk.Label(window, text="Número de Títulos:").grid(row=4, column=0)
        n_titulos_entry = tk.Entry(window)
        n_titulos_entry.grid(row=4, column=1)

         # Botão para selecionar imagem
        tk.Label(window, text="Escudo do Time (JPG):").grid(row=5, column=0)
        self.caminho_imagem = tk.StringVar()  # Variável para armazenar o caminho da imagem
        tk.Button(window, text="Selecionar Imagem", command=self.selecionar_imagem).grid(row=5, column=1)

        def submit():
            sigla = sigla_entry.get()
            nome_clube = nome_clube_entry.get()
            fundacao = fundacao_entry.get()
            mascote = mascote_entry.get()
            n_titulos = n_titulos_entry.get()
            caminho_imagem = self.caminho_imagem.get()
            resultado = self.crud_time.inserir(sigla, nome_clube, fundacao, mascote, n_titulos, caminho_imagem)
            messagebox.showinfo("Resultado", resultado)

        tk.Button(window, text="Inserir", command=submit).grid(row=5, column=0, columnspan=2)

    def open_selecionar_time(self):
        window = tk.Toplevel(self.root)
        window.title("Selecionar Time")

        tk.Label(window, text="Sigla do Time (opcional):").grid(row=0, column=0)
        sigla_entry = tk.Entry(window)
        sigla_entry.grid(row=0, column=1)

        def submit():
            sigla = sigla_entry.get() or None
            result = self.crud_time.selecionar(sigla)

            if not result:
                messagebox.showinfo("Resultado", "Nenhum time encontrado.")
                return

            table_window = tk.Toplevel(window)
            table_window.title("Resultados da Consulta")
            columns = ("Sigla", "Nome do Clube", "Fundação", "Mascote", "Nº de Títulos")
            tree = ttk.Treeview(table_window, columns=columns, show="headings")

            for col in columns:
                tree.heading(col, text=col)

            for row in result:
                tree.insert("", "end", values=row)

            tree.grid(row=0, column=0, sticky="nsew")
            scrollbar = ttk.Scrollbar(table_window, orient="vertical", command=tree.yview)
            tree.configure(yscroll=scrollbar.set)
            scrollbar.grid(row=0, column=1, sticky="ns")

        tk.Button(window, text="Selecionar", command=submit).grid(row=1, column=0, columnspan=2)

    def open_atualizar_time(self):
        window = tk.Toplevel(self.root)
        window.title("Atualizar Time")

        tk.Label(window, text="Sigla:").grid(row=0, column=0)
        sigla_entry = tk.Entry(window)
        sigla_entry.grid(row=0, column=1)

        tk.Label(window, text="Nome do Clube:").grid(row=1, column=0)
        nome_clube_entry = tk.Entry(window)
        nome_clube_entry.grid(row=1, column=1)

        tk.Label(window, text="Ano de Fundação:").grid(row=2, column=0)
        fundacao_entry = tk.Entry(window)
        fundacao_entry.grid(row=2, column=1)

        tk.Label(window, text="Mascote:").grid(row=3, column=0)
        mascote_entry = tk.Entry(window)
        mascote_entry.grid(row=3, column=1)

        tk.Label(window, text="Número de Títulos:").grid(row=4, column=0)
        n_titulos_entry = tk.Entry(window)
        n_titulos_entry.grid(row=4, column=1)

        def submit():
            sigla = sigla_entry.get()
            nome_clube = nome_clube_entry.get()
            fundacao = fundacao_entry.get()
            mascote = mascote_entry.get()
            n_titulos = n_titulos_entry.get()
            result = self.crud_time.atualizar(sigla, nome_clube, fundacao, mascote, n_titulos)
            messagebox.showinfo("Resultado", result)

        tk.Button(window, text="Atualizar", command=submit).grid(row=5, column=0, columnspan=2)

    def open_deletar_time(self):
        window = tk.Toplevel(self.root)
        window.title("Deletar Time")

        tk.Label(window, text="Sigla do Time:").grid(row=0, column=0)
        sigla_entry = tk.Entry(window)
        sigla_entry.grid(row=0, column=1)

        def submit():
            sigla = sigla_entry.get()
            result = self.crud_time.deletar(sigla)
            messagebox.showinfo("Resultado", result)

        tk.Button(window, text="Deletar", command=submit).grid(row=1, column=0, columnspan=2)

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