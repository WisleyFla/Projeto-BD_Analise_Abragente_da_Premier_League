
# Trabalho de banco de dados
- Professora: Maristela Holanda;
- Alunos: Lucas, Ricardo, Valeria e Wisley
  
# ⚙️ Sistema de Gerenciamento da Premier League

Este projeto tem como objetivo desenvolver um Sistema de gerenciamento da premier league onde permite cadastrar, deletar, inserir e atualizar as entidades, elenco, time e funcionario

# ✅ Funcionalidades Principais

 - Cadastro de time;
 - Deletar time;
 - Atualizar seu time;
 - Inserir escudo de seu time;

 - Cadastro de funcionario;
 - Deletar funcionario
 - Atualizar funcionario;

 - Cadastro de elenco;
 - Deletar elenco;
 - Atualizar elenco;

# 🏗️ Estrutura do Projeto

    📊 Regras de Negócio: As regras de negócio definem as diretrizes e políticas que regem o funcionamento do sistema.

    💾 Banco de Dados: Uma parte essencial deste projeto é a definição do banco de dados, que armazenará informações cruciais sobre os recursos como: datalhes do time, nomes, sobre os funcionarios, nome, departamento, idade e etc, e nos times os nomes, imagem, mascote e etc.

    💻 Interface de Usuário: A interface será projetada de forma intuitiva, permitindo uma fácil navegação para todos os tipos de usuários.

# 🚀 Como Contribuir

    Para contribuir com este projeto, siga as diretrizes de contribuição no arquivo CONTRIBUTING.md.

    Se você encontrar problemas ou bugs, por favor, abra uma issue em nosso repositório.

# 💻 Tecnologias utilizada nesse projeto
Phyton Tkinter e Postegresql

# 💻 Instalando da biblioteca phyton para o front

1. Tkinter
    O tkinter já vem instalado com o Python, então você não precisa instalar nada adicionalmente. Você pode começar a usá-lo diretamente.

Exemplo de uso:
import tkinter as tk

root = tk.Tk()
root.title("Minha Aplicação")
root.geometry("300x200")

label = tk.Label(root, text="Olá, Tkinter!")
label.pack()

root.mainloop()

2. Pyscopg2

   É uma biblioteca Python para interagir com bancos de dados PostgreSQL, permitindo a execução de comandos SQL e a manipulação de dados diretamente.

Passo a passo:

    Abra o terminal ou prompt de comando.

    Execute o seguinte comando:
    bash

   pip install psycopg2


Exemplo de uso:

import psycopg2

# Conectando ao banco de dados
conn = psycopg2.connect(dbname="nome_do_banco", user="usuario", password="senha", host="localhost")

# Criando um cursor e executando uma consulta
cur = conn.cursor()
cur.execute("SELECT * FROM tabela")
print(cur.fetchall())

# Fechando a conexão
cur.close()
conn.close()


3. dotenv

    O dotenv é uma biblioteca Python que permite carregar variáveis de ambiente de um arquivo .env para o seu código.

Passo a passo:

    Abra o terminal ou prompt de comando.

    Execute o seguinte comando:
    bash

    pip install python-dotenv


Exemplo de uso:

"""Criação do arquivo .env: O arquivo .env deve ser colocado no mesmo diretório do seu código.
DB_USER=meu_usuario
DB_PASSWORD=minha_senha
DB_HOST=localhost
DB_PORT=5432
DB_NAME=meu_banco"""

import os
from dotenv import load_dotenv

# Carregar as variáveis de ambiente do arquivo .env
load_dotenv()

# Acessar variáveis de ambiente
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
print(f"Usuário: {db_user}, Senha: {db_password}")


4. OS 

   Biblioteca para acessar variáveis de ambiente e manipular o sistema de arquivos, já vem instalada.

Como a biblioteca os é usada aqui:

from kivy.app import App
from kivy.uix.label import Label

class MinhaApp(App):
    def build(self):
        return Label(text="Olá, Kivy!")

if __name__ == "__main__":
    MinhaApp().run()

5. wxPython

    O wxPython é outra biblioteca popular para criar interfaces gráficas. Para instalá-lo, use o pip.

Passo a passo:

    Abra o terminal ou prompt de comando.

    Execute o seguinte comando:
    bash
    Copy

    pip install wxPython

Exemplo de uso:

import wx

app = wx.App(False)
frame = wx.Frame(None, title="Minha Aplicação", size=(300, 200))
panel = wx.Panel(frame)
label = wx.StaticText(panel, label="Olá, wxPython!", pos=(100, 80))
frame.Show(True)
app.MainLoop()

# 💻 Instalação do PostgreSQL (Sistema de Gerenciamento de Banco de Dados)
Instalando o PostgreSQL

Para instalar o postgresql no linux basta executar o seguinte comando:

sudo apt install postgresql postgresql-contrib libpq-dev

Verifique a instalação do PostgreSQL

Verifique se o postgresql foi instalado corretamente digitando:

pg_config --version

Deve ser apresentado a versão atual do postegresql.
Configurando o PostgreSQL

Vamos entrar no console interativo do postgresql para criar um usuário privilegiado. Entre no terminal como o usuário do postgres:

sudo -i -u postgres

Inicie o terminal do PostgreSQL:

psql

Crie um usuário e garanta que tenha privilégios elevados:

CREATE USER 'nome' WITH PASSWORD 'senha';
ALTER USER 'nome' WITH SUPERUSER;

Altere os campos nome e senha para valores que desejar.

Para verificar que o usuário foi criado digite o comando

\du.

Para sair do terminal do PostgreSQL digite o comando

\q

# 📙 Guia de Uso do Docker com PostgreSQL
Pré-requisitos

    Docker instalado em seu sistema.
    Docker Compose (geralmente incluído com a instalação do Docker).

Configuração do Docker Compose

No diretório do projeto, verifique se existe um arquivo docker-compose.yml. Este arquivo contém as configurações necessárias para criar o contêiner PostgreSQL.
Iniciar o Banco de Dados PostgreSQL

Abra um terminal e navegue até o diretório do projeto onde está o arquivo docker-compose.yml.

    Para iniciar o contêiner PostgreSQL, execute o seguinte comando:

docker-compose up -d

Isso criará e iniciará o contêiner PostgreSQL em segundo plano (-d). Aguarde até que o contêiner esteja em execução.

    Você pode verificar o status do contêiner com o seguinte comando:

docker ps

Certifique-se de que o contêiner PostgreSQL esteja listado na saída.
Conectar-se ao Banco de Dados PostgreSQL

Para se conectar ao banco de dados PostgreSQL a partir do terminal, use o seguinte comando:

psql -h localhost -U postgres -d db

    -h localhost: Especifica o host onde o PostgreSQL está sendo executado (local).
    -U postgres: Especifica o nome de usuário (geralmente é "postgres" por padrão).
    -d db: Especifica o nome do banco de dados ao qual você deseja se conectar.
    Será solicitada a senha do usuário "postgres". Insira a senha configurada no arquivo docker-compose.yml (por padrão, é "postgres").

Você estará conectado ao banco de dados PostgreSQL e poderá executar comandos SQL.
Encerrar o Contêiner

Quando você terminar de trabalhar com o banco de dados, você pode parar e remover o contêiner PostgreSQL usando o seguinte comando:

docker-compose down

Isso desligará e removerá o contêiner PostgreSQL. Certifique-se de que nenhum dado importante seja perdido antes de executar este comando.

# 💻 Frontend
    Como o tkinter já vem instalado com o Python, você só precisa criar um arquivo Python (por exemplo, app_tkinter.py) com o código fornecido e executá-lo.

Passo a passo:

    Crie um arquivo chamado app_tkinter.py e cole o código abaixo:

    import tkinter as tk

    root = tk.Tk()
    root.title("Minha Aplicação")
    root.geometry("300x200")

    label = tk.Label(root, text="Olá, Tkinter!")
    label.pack()

    root.mainloop()

    Abra o terminal ou prompt de comando.

    Navegue até o diretório onde o arquivo app_tkinter.py está salvo.

    Execute o comando:
    bash

    python app_tkinter.py

# 💻 Backend
Instale as dependências

$ npm install



