
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

# Tecnologias utilizada nesse projeto
Phyton Tkinter e Postegresql

# Instalando da biblioteca phyton para o front

# Instalação do PostgreSQL (Sistema de Gerenciamento de Banco de Dados)
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

# Guia de Uso do Docker com PostgreSQL
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

# Frontend
Iniciando o nextjs

antes de tudo é preciso ter o node instalado na máquina como é mostrado acima.
Rodando o projeto

para rodar o frontend do projeto basta instalar as dependências e rodar o servidor utilizando esses comandos:

npm i
npm run dev

basta isso, se estiver tudo certo.

# Backend
Instale as dependências

$ npm install

Rodando a aplicação

# development
$ npm run start

