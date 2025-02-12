-- Criação da Tabela Time (precisa existir antes de outras referências)
CREATE TABLE Time (
    Sigla VARCHAR(10) PRIMARY KEY,
    Nome_clube VARCHAR(100) NOT NULL,
    Fundacao DATE NOT NULL,
    Mascote VARCHAR(50),
    N_Titulos INT DEFAULT 0
);

-- Criação da Tabela Departamentos
CREATE TABLE Departamentos (
    SIGLA_departamento VARCHAR(10) PRIMARY KEY,
    Nome_departamento VARCHAR(50) NOT NULL
);

-- Criação da Tabela Funcionarios 
CREATE TABLE Funcionarios (
    Matricula SERIAL PRIMARY KEY,
    Nome_funcionario VARCHAR(100) NOT NULL,
    Idade INT CHECK (Idade > 0),
    Profissao VARCHAR(50) NOT NULL,
    SIGLA_departamento VARCHAR(10) REFERENCES Departamentos(SIGLA_departamento) ON DELETE SET NULL,
    Sigla_time VARCHAR(3) REFERENCES Time(Sigla) ON DELETE SET NULL
);

-- Criação da Tabela Posicao
CREATE TABLE Posicao (
    Sigla_posicao VARCHAR(10) PRIMARY KEY,
    Nome_posicao VARCHAR(50) NOT NULL
);

-- Criação da Tabela Elenco (depois de Time)
CREATE TABLE Elenco (
    ID_Jogador SERIAL PRIMARY KEY,
    Nome_jogador VARCHAR(100) NOT NULL,
    Idade INT CHECK (Idade > 0),
    Valor_mercado DECIMAL(15,2),
    Sigla VARCHAR(10) REFERENCES Time(Sigla) ON DELETE CASCADE
);

-- Criação da Tabela Classificacao
CREATE TABLE Classificacao (
    ID_Classificacao SERIAL PRIMARY KEY,
    Pontos INT DEFAULT 0,
    Vitoria INT DEFAULT 0,
    Empate INT DEFAULT 0,
    Derrota INT DEFAULT 0,
    Saldo_Gols INT DEFAULT 0,
    Gols_feitos INT DEFAULT 0,
    Gols_sofridos INT DEFAULT 0,
    Sigla VARCHAR(10) REFERENCES Time(Sigla) ON DELETE CASCADE
);

-- Criação da Tabela Estadio
CREATE TABLE Estadio (
    Nome_estadio VARCHAR(100) PRIMARY KEY,
    Ano_criacao INT CHECK (Ano_criacao > 1800),
    Gramado VARCHAR(50),
    Capacidade INT CHECK (Capacidade > 0),
    Sigla VARCHAR(10) REFERENCES Time(Sigla) ON DELETE CASCADE
);

-- Criação da Tabela Patrocinadores
CREATE TABLE Patrocinadores (
    ID_requerimento SERIAL PRIMARY KEY,
    Nome_patrocinio VARCHAR(100) NOT NULL,
    Tipo_acordo VARCHAR(50) NOT NULL,
    Valor DECIMAL(15,2),
    Duracao INT CHECK (Duracao > 0),
    Sigla VARCHAR(10) REFERENCES Time(Sigla) ON DELETE CASCADE
);

-- Criação da Tabela Rel (Relacionamento entre Time e Patrocinadores)
CREATE TABLE Rel (
    Sigla VARCHAR(10),
    ID_requerimento INT,
    PRIMARY KEY (Sigla, ID_requerimento),
    FOREIGN KEY (Sigla) REFERENCES Time(Sigla) ON DELETE CASCADE,
    FOREIGN KEY (ID_requerimento) REFERENCES Patrocinadores(ID_requerimento) ON DELETE CASCADE
);

-- Criação da Tabela Confronto
CREATE TABLE Confronto (
    Id_confronto SERIAL PRIMARY KEY,
    Gols_mandante INT DEFAULT 0,
    Gols_visitante INT DEFAULT 0
);

-- Criação da Tabela Jogos
CREATE TABLE Jogos (
    ID_Jogo SERIAL PRIMARY KEY,
    Data_jogo DATE NOT NULL,
    Rodada INT CHECK (Rodada > 0),
    Placar VARCHAR(10),
    Id_confronto INT REFERENCES Confronto(Id_confronto) ON DELETE CASCADE
);

-- Criação da Tabela Arbitros
CREATE TABLE Arbitros (
    ID_Arbitro SERIAL PRIMARY KEY,
    Nome_arbitro VARCHAR(100) NOT NULL
);

-- Criação da Tabela de Relacionamento Jogos_Arbitros
CREATE TABLE Jogos_Arbitros (
    ID_Jogo INT,
    ID_Arbitro INT,
    PRIMARY KEY (ID_Jogo, ID_Arbitro),
    FOREIGN KEY (ID_Jogo) REFERENCES Jogos(ID_Jogo) ON DELETE CASCADE,
    FOREIGN KEY (ID_Arbitro) REFERENCES Arbitros(ID_Arbitro) ON DELETE CASCADE
);

-- Criação da Tabela Rel11 (Relacionamento entre Sigla e Departamentos)
CREATE TABLE Rel11 (
    Sigla VARCHAR(10),
    SIGLA_departamento VARCHAR(10),
    PRIMARY KEY (Sigla, SIGLA_departamento),
    FOREIGN KEY (Sigla) REFERENCES Time(Sigla) ON DELETE CASCADE,
    FOREIGN KEY (SIGLA_departamento) REFERENCES Departamentos(SIGLA_departamento) ON DELETE CASCADE
);

-- Dados

-- Tabela time:

INSERT INTO Time (Sigla, Nome_clube, Fundacao, Mascote, N_Titulos) VALUES
('ARS', 'Arsenal', '1886-10-01', 'Gunnersaurus', 13),
('AST', 'Aston Villa', '1874-03-01', 'Hercules the Lion', 7),
('BOU', 'AFC Bournemouth', '1899-10-01', 'Cherry Bear', 0),
('BRE', 'Brentford', '1889-10-01', 'Buzz Bee', 0),
('BHA', 'Brighton & Hove Albion', '1901-10-01', 'Gully the Seagull', 0),
('BUR', 'Burnley', '1882-10-01', 'Bertie Bee', 2),
('CHE', 'Chelsea', '1905-03-10', 'Stamford the Lion', 6),
('CRY', 'Crystal Palace', '1905-09-01', 'Pete the Eagle', 0),
('EVE', 'Everton', '1878-10-01', 'Chang the Elephant', 9),
('FUL', 'Fulham', '1879-10-01', 'Billy the Badger', 0),
('LIV', 'Liverpool', '1892-06-03', 'Mighty Red', 19),
('LUT', 'Luton Town', '1885-04-11', 'Happy Harry', 0),
('MCI', 'Manchester City', '1880-11-23', 'Moonchester', 9),
('MUN', 'Manchester United', '1878-10-01', 'Fred the Red', 20),
('NEW', 'Newcastle United', '1892-12-09', 'Monty Magpie', 4),
('NFO', 'Nottingham Forest', '1865-10-01', 'Robin Hood', 1),
('SHE', 'Sheffield United', '1889-10-01', 'Captain Blade', 1),
('TOT', 'Tottenham Hotspur', '1882-09-05', 'Chirpy Cockerel', 2),
('WHU', 'West Ham United', '1895-06-05', 'Hammerhead', 0),
('WOL', 'Wolverhampton Wanderers', '1877-10-01', 'Wolfie & Wendy', 3);

-- Tabela patrocinadores:

INSERT INTO Patrocinadores (Nome_patrocinio, Tipo_acordo, Valor, Duracao, Sigla) VALUES
('Adidas', 'Material Esportivo', 10000000.00, 5, 'ARS'),
('Castore', 'Material Esportivo', 8000000.00, 4, 'AST'),
('Dafabet', 'Aposta Esportiva', 6000000.00, 3, 'BOU'),
('Hollywoodbets', 'Aposta Esportiva', 7000000.00, 3, 'BRE'),
('Nike', 'Material Esportivo', 12000000.00, 5, 'BHA'),
('Classic Football Shirts', 'Patrocínio Principal', 5000000.00, 2, 'BUR'),
('Nike', 'Material Esportivo', 15000000.00, 5, 'CHE'),
('Cinch', 'Patrocínio Principal', 7500000.00, 3, 'CRY'),
('Hummel', 'Material Esportivo', 7000000.00, 4, 'EVE'),
('Adidas', 'Material Esportivo', 6000000.00, 3, 'FUL'),
('Standard Chartered', 'Banco', 40000000.00, 6, 'LIV'),
('Umbro', 'Material Esportivo', 5000000.00, 3, 'LUT'),
('Puma', 'Material Esportivo', 6500000.00, 5, 'MCI'),
('Adidas', 'Material Esportivo', 9000000.00, 4, 'MUN'),
('Castore', 'Material Esportivo', 7500000.00, 4, 'NEW'),
('Ideagen', 'Software', 5000000.00, 3, 'NFO'),
('Errea', 'Material Esportivo', 4500000.00, 3, 'SHE'),
('AIA', 'Seguros', 45000000.00, 8, 'TOT'),
('Betway', 'Aposta Esportiva', 10000000.00, 4, 'WHU'),
('Castore', 'Material Esportivo', 6000000.00, 4, 'WOL');

-- Tabela confronto:

INSERT INTO Confronto (Gols_mandante, Gols_visitante) VALUES
(2, 1),  -- Arsenal vs Manchester United
(3, 0),  -- Manchester City vs Chelsea
(1, 1),  -- Liverpool vs Tottenham
(4, 2),  -- Newcastle vs Aston Villa
(0, 2),  -- Brentford vs West Ham
(2, 2),  -- Brighton vs Everton
(3, 1),  -- Manchester United vs Arsenal
(1, 3),  -- Chelsea vs Manchester City
(2, 2),  -- Tottenham vs Liverpool
(0, 1),  -- Aston Villa vs Newcastle
(1, 4),  -- West Ham vs Brentford
(2, 0),  -- Everton vs Brighton
(1, 0),  -- Arsenal vs Chelsea
(3, 2),  -- Liverpool vs Manchester City
(2, 1),  -- Tottenham vs Aston Villa
(1, 2),  -- Newcastle vs Brentford
(0, 3),  -- Brighton vs West Ham
(1, 1),  -- Everton vs Manchester United
(2, 3),  -- Chelsea vs Tottenham
(3, 3);  -- Manchester City vs Arsenal

-- Tabela jogos:

INSERT INTO Jogos (Data_jogo, Rodada, Placar, Id_confronto) VALUES
('2023-08-12', 1, '2-1', 1),  -- Arsenal vs Manchester United
('2023-08-13', 1, '3-0', 2),  -- Manchester City vs Chelsea
('2023-08-19', 2, '1-1', 3),  -- Liverpool vs Tottenham
('2023-08-20', 2, '4-2', 4),  -- Newcastle vs Aston Villa
('2023-08-26', 3, '0-2', 5),  -- Brentford vs West Ham
('2023-08-27', 3, '2-2', 6),  -- Brighton vs Everton
('2023-09-02', 4, '3-1', 7),  -- Manchester United vs Arsenal
('2023-09-03', 4, '1-3', 8),  -- Chelsea vs Manchester City
('2023-09-16', 5, '2-2', 9),  -- Tottenham vs Liverpool
('2023-09-17', 5, '0-1', 10), -- Aston Villa vs Newcastle
('2023-09-23', 6, '1-4', 11), -- West Ham vs Brentford
('2023-09-24', 6, '2-0', 12), -- Everton vs Brighton
('2023-09-30', 7, '1-0', 13), -- Arsenal vs Chelsea
('2023-10-01', 7, '3-2', 14), -- Liverpool vs Manchester City
('2023-10-07', 8, '2-1', 15), -- Tottenham vs Aston Villa
('2023-10-08', 8, '1-2', 16), -- Newcastle vs Brentford
('2023-10-21', 9, '0-3', 17), -- Brighton vs West Ham
('2023-10-22', 9, '1-1', 18), -- Everton vs Manchester United
('2023-10-28', 10, '2-3', 19), -- Chelsea vs Tottenham
('2023-10-29', 10, '3-3', 20); -- Manchester City vs Arsenal

-- Tabela posicao:

INSERT INTO Posicao (Sigla_posicao, Nome_posicao) VALUES
('GOL', 'Goleiro'),
('ZAG', 'Zagueiro'),
('LD', 'Lateral Direito'),
('LE', 'Lateral Esquerdo'),
('VOL', 'Volante'),
('MC', 'Meio-Campista'),
('MEI', 'Meia Atacante'),
('PE', 'Ponta Esquerda'),
('PD', 'Ponta Direita'),
('CA', 'Centroavante');

-- Tabela Elenco:

-- Alterar a tabela elenco para incluir a posicao
ALTER TABLE Elenco ADD COLUMN Sigla_posicao VARCHAR(10);
ALTER TABLE Elenco ADD CONSTRAINT fk_posicao FOREIGN KEY (Sigla_posicao) REFERENCES Posicao(Sigla_posicao);

-- Arsenal:

INSERT INTO Elenco (Nome_jogador, Idade, Valor_mercado, Sigla, Sigla_posicao) VALUES
('Aaron Ramsdale', 26, 45000000.00, 'ARS', 'GOL'),
('William Saliba', 23, 85000000.00, 'ARS', 'ZAG'),
('Gabriel Magalhães', 26, 55000000.00, 'ARS', 'ZAG'),
('Ben White', 26, 60000000.00, 'ARS', 'LD'),
('Takehiro Tomiyasu', 25, 35000000.00, 'ARS', 'LE'),
('Declan Rice', 25, 120000000.00, 'ARS', 'VOL'),
('Jorginho', 32, 25000000.00, 'ARS', 'MC'),
('Martin Ødegaard', 25, 110000000.00, 'ARS', 'MEI'),
('Leandro Trossard', 29, 50000000.00, 'ARS', 'PE'),
('Bukayo Saka', 22, 120000000.00, 'ARS', 'PD'),
('Gabriel Jesus', 26, 90000000.00, 'ARS', 'CA'),
('Eddie Nketiah', 25, 40000000.00, 'ARS', 'CA'),
('Kai Havertz', 24, 75000000.00, 'ARS', 'MEI'),
('Fabio Vieira', 23, 30000000.00, 'ARS', 'MC'),
('Jakub Kiwior', 24, 30000000.00, 'ARS', 'ZAG');

-- Manchester City:

INSERT INTO Elenco (Nome_jogador, Idade, Valor_mercado, Sigla, Sigla_posicao) VALUES
('Ederson', 30, 50000000.00, 'MCI', 'GOL'),
('Rúben Dias', 27, 80000000.00, 'MCI', 'ZAG'),
('John Stones', 29, 65000000.00, 'MCI', 'ZAG'),
('Kyle Walker', 34, 25000000.00, 'MCI', 'LD'),
('João Cancelo', 30, 55000000.00, 'MCI', 'LE'),
('Rodri', 27, 100000000.00, 'MCI', 'VOL'),
('Kevin De Bruyne', 33, 80000000.00, 'MCI', 'MC'),
('Bernardo Silva', 30, 70000000.00, 'MCI', 'MEI'),
('Jack Grealish', 29, 65000000.00, 'MCI', 'PE'),
('Phil Foden', 24, 110000000.00, 'MCI', 'PD'),
('Erling Haaland', 24, 180000000.00, 'MCI', 'CA'),
('Julián Álvarez', 25, 90000000.00, 'MCI', 'CA'),
('Mateo Kovacic', 30, 50000000.00, 'MCI', 'MC'),
('Nathan Aké', 29, 45000000.00, 'MCI', 'ZAG'),
('Manuel Akanji', 28, 40000000.00, 'MCI', 'ZAG');

-- Manchester United:

INSERT INTO Elenco (Nome_jogador, Idade, Valor_mercado, Sigla, Sigla_posicao) VALUES
('André Onana', 28, 35000000.00, 'MUN', 'GOL'),
('Raphaël Varane', 30, 40000000.00, 'MUN', 'ZAG'),
('Lisandro Martínez', 26, 50000000.00, 'MUN', 'ZAG'),
('Diogo Dalot', 25, 35000000.00, 'MUN', 'LD'),
('Luke Shaw', 29, 40000000.00, 'MUN', 'LE'),
('Casemiro', 32, 30000000.00, 'MUN', 'VOL'),
('Bruno Fernandes', 30, 85000000.00, 'MUN', 'MC'),
('Mason Mount', 26, 60000000.00, 'MUN', 'MEI'),
('Antony', 24, 50000000.00, 'MUN', 'PD'),
('Marcus Rashford', 27, 90000000.00, 'MUN', 'PE'),
('Rasmus Højlund', 21, 75000000.00, 'MUN', 'CA'),
('Christian Eriksen', 32, 25000000.00, 'MUN', 'MC'),
('Scott McTominay', 27, 30000000.00, 'MUN', 'MC'),
('Harry Maguire', 31, 20000000.00, 'MUN', 'ZAG'),
('Aaron Wan-Bissaka', 26, 30000000.00, 'MUN', 'LD');

-- Liverpool:

INSERT INTO Elenco (Nome_jogador, Idade, Valor_mercado, Sigla, Sigla_posicao) VALUES
('Alisson Becker', 31, 50000000.00, 'LIV', 'GOL'),
('Virgil van Dijk', 32, 50000000.00, 'LIV', 'ZAG'),
('Ibrahima Konaté', 25, 60000000.00, 'LIV', 'ZAG'),
('Trent Alexander-Arnold', 26, 90000000.00, 'LIV', 'LD'),
('Andrew Robertson', 30, 40000000.00, 'LIV', 'LE'),
('Alexis Mac Allister', 25, 70000000.00, 'LIV', 'MC'),
('Dominik Szoboszlai', 24, 65000000.00, 'LIV', 'MEI'),
('Curtis Jones', 23, 40000000.00, 'LIV', 'MC'),
('Mohamed Salah', 32, 120000000.00, 'LIV', 'PD'),
('Luis Díaz', 27, 75000000.00, 'LIV', 'PE'),
('Darwin Núñez', 25, 80000000.00, 'LIV', 'CA'),
('Wataru Endo', 31, 20000000.00, 'LIV', 'VOL'),
('Joe Gomez', 27, 35000000.00, 'LIV', 'ZAG'),
('Diogo Jota', 28, 70000000.00, 'LIV', 'CA'),
('Cody Gakpo', 25, 60000000.00, 'LIV', 'MEI');

-- Chelsea:

INSERT INTO Elenco (Nome_jogador, Idade, Valor_mercado, Sigla, Sigla_posicao) VALUES
('Robert Sánchez', 26, 25000000.00, 'CHE', 'GOL'),
('Thiago Silva', 39, 3000000.00, 'CHE', 'ZAG'),
('Levi Colwill', 21, 60000000.00, 'CHE', 'ZAG'),
('Reece James', 24, 70000000.00, 'CHE', 'LD'),
('Ben Chilwell', 27, 50000000.00, 'CHE', 'LE'),
('Moises Caicedo', 23, 90000000.00, 'CHE', 'VOL'),
('Enzo Fernández', 23, 100000000.00, 'CHE', 'MC'),
('Conor Gallagher', 24, 55000000.00, 'CHE', 'MC'),
('Raheem Sterling', 29, 60000000.00, 'CHE', 'PD'),
('Mykhailo Mudryk', 23, 40000000.00, 'CHE', 'PE'),
('Nicolas Jackson', 23, 50000000.00, 'CHE', 'CA'),
('Cole Palmer', 21, 80000000.00, 'CHE', 'MEI'),
('Christopher Nkunku', 26, 85000000.00, 'CHE', 'MEI'),
('Axel Disasi', 26, 45000000.00, 'CHE', 'ZAG'),
('Malo Gusto', 21, 35000000.00, 'CHE', 'LD');

-- Tottenham Hotspur:

INSERT INTO Elenco (Nome_jogador, Idade, Valor_mercado, Sigla, Sigla_posicao) VALUES
('Hugo Lloris', 37, 10000000.00, 'TOT', 'GOL'),
('Cristian Romero', 25, 55000000.00, 'TOT', 'ZAG'),
('Micky van de Ven', 22, 40000000.00, 'TOT', 'ZAG'),
('Pedro Porro', 24, 30000000.00, 'TOT', 'LD'),
('Ivan Perišić', 34, 10000000.00, 'TOT', 'LE'),
('Yves Bissouma', 27, 35000000.00, 'TOT', 'VOL'),
('Pierre-Emile Højbjerg', 28, 45000000.00, 'TOT', 'VOL'),
('James Maddison', 27, 70000000.00, 'TOT', 'MC'),
('Dejan Kulusevski', 24, 60000000.00, 'TOT', 'PD'),
('Son Heung-min', 31, 80000000.00, 'TOT', 'PE'),
('Richarlison', 26, 55000000.00, 'TOT', 'CA'),
('Manor Solomon', 24, 25000000.00, 'TOT', 'MEI'),
('Emerson Royal', 25, 30000000.00, 'TOT', 'LD'),
('Davinson Sánchez', 27, 20000000.00, 'TOT', 'ZAG'),
('Oliver Skipp', 23, 25000000.00, 'TOT', 'MC');

-- Newcastle United:

INSERT INTO Elenco (Nome_jogador, Idade, Valor_mercado, Sigla, Sigla_posicao) VALUES
('Nick Pope', 31, 25000000.00, 'NEW', 'GOL'),
('Kieran Trippier', 33, 30000000.00, 'NEW', 'LD'),
('Sven Botman', 23, 60000000.00, 'NEW', 'ZAG'),
('Fabian Schär', 32, 25000000.00, 'NEW', 'ZAG'),
('Dan Burn', 33, 10000000.00, 'NEW', 'LE'),
('Bruno Guimarães', 26, 70000000.00, 'NEW', 'VOL'),
('Joelinton', 27, 50000000.00, 'NEW', 'MC'),
('Joe Willock', 24, 40000000.00, 'NEW', 'MC'),
('Miguel Almirón', 30, 40000000.00, 'NEW', 'PD'),
('Alexander Isak', 24, 70000000.00, 'NEW', 'CA'),
('Anthony Gordon', 22, 45000000.00, 'NEW', 'PE'),
('Callum Wilson', 31, 25000000.00, 'NEW', 'CA'),
('Matt Targett', 29, 10000000.00, 'NEW', 'LE'),
('Sean Longstaff', 26, 30000000.00, 'NEW', 'MC'),
('Emil Krafth', 29, 10000000.00, 'NEW', 'LD');

-- Aston Villa:

INSERT INTO Elenco (Nome_jogador, Idade, Valor_mercado, Sigla, Sigla_posicao) VALUES
('Emi Martínez', 32, 25000000.00, 'AST', 'GOL'),
('Matty Cash', 27, 25000000.00, 'AST', 'LD'),
('Ezri Konsa', 26, 35000000.00, 'AST', 'ZAG'),
('Tyrone Mings', 31, 25000000.00, 'AST', 'ZAG'),
('Lucas Digne', 30, 20000000.00, 'AST', 'LE'),
('Boubacar Kamara', 24, 45000000.00, 'AST', 'VOL'),
('Douglas Luiz', 25, 50000000.00, 'AST', 'MC'),
('John McGinn', 29, 35000000.00, 'AST', 'MC'),
('Leon Bailey', 26, 25000000.00, 'AST', 'PD'),
('Ollie Watkins', 28, 50000000.00, 'AST', 'CA'),
('Emiliano Buendía', 27, 35000000.00, 'AST', 'MEI'),
('Jacob Ramsey', 22, 40000000.00, 'AST', 'MC'),
('Philippe Coutinho', 31, 20000000.00, 'AST', 'MEI'),
('Cameron Archer', 22, 15000000.00, 'AST', 'CA'),
('Ashley Young', 38, 5000000.00, 'AST', 'LE');

-- Brighton & Hove Albion:

INSERT INTO Elenco (Nome_jogador, Idade, Valor_mercado, Sigla, Sigla_posicao) VALUES
('Robert Sánchez', 26, 25000000.00, 'BHA', 'GOL'),
('Lewis Dunk', 31, 35000000.00, 'BHA', 'ZAG'),
('Adam Webster', 28, 25000000.00, 'BHA', 'ZAG'),
('Pervis Estupiñán', 25, 40000000.00, 'BHA', 'LE'),
('Joel Veltman', 32, 10000000.00, 'BHA', 'LD'),
('Moisés Caicedo', 23, 90000000.00, 'BHA', 'VOL'),
('Alexis Mac Allister', 24, 60000000.00, 'BHA', 'MC'),
('Kaoru Mitoma', 26, 40000000.00, 'BHA', 'PE'),
('Leandro Trossard', 28, 35000000.00, 'BHA', 'PD'),
('Danny Welbeck', 33, 15000000.00, 'BHA', 'CA'),
('Evan Ferguson', 19, 25000000.00, 'BHA', 'CA'),
('Solly March', 29, 25000000.00, 'BHA', 'MEI'),
('Jakub Moder', 24, 20000000.00, 'BHA', 'MC'),
('Julio Enciso', 19, 20000000.00, 'BHA', 'PE'),
('Deniz Undav', 27, 20000000.00, 'BHA', 'CA');

-- Wolverhampton Wanderers:

INSERT INTO Elenco (Nome_jogador, Idade, Valor_mercado, Sigla, Sigla_posicao) VALUES
('José Sá', 30, 15000000.00, 'WOL', 'GOL'),
('Max Kilman', 26, 25000000.00, 'WOL', 'ZAG'),
('Craig Dawson', 33, 10000000.00, 'WOL', 'ZAG'),
('Rayan Aït-Nouri', 22, 25000000.00, 'WOL', 'LE'),
('Jonny Castro', 29, 15000000.00, 'WOL', 'LD'),
('João Moutinho', 37, 5000000.00, 'WOL', 'MC'),
('Matheus Nunes', 25, 45000000.00, 'WOL', 'VOL'),
('Raul Jiménez', 33, 15000000.00, 'WOL', 'CA'),
('Pedro Neto', 23, 40000000.00, 'WOL', 'PD'),
('Daniel Podence', 28, 25000000.00, 'WOL', 'PE'),
('Hwang Hee-chan', 27, 15000000.00, 'WOL', 'PD'),
('Gonçalo Guedes', 27, 20000000.00, 'WOL', 'PE'),
('Boubacar Traoré', 23, 20000000.00, 'WOL', 'VOL'),
('Adama Traoré', 27, 15000000.00, 'WOL', 'PD'),
('Luke Cundle', 20, 5000000.00, 'WOL', 'MC');

-- Brentford:

INSERT INTO Elenco (Nome_jogador, Idade, Valor_mercado, Sigla, Sigla_posicao) VALUES
('David Raya', 28, 30000000.00, 'BRE', 'GOL'),
('Ethan Pinnock', 30, 15000000.00, 'BRE', 'ZAG'),
('Pontus Jansson', 32, 10000000.00, 'BRE', 'ZAG'),
('Mads Roerslev', 24, 15000000.00, 'BRE', 'LD'),
('Rico Henry', 26, 20000000.00, 'BRE', 'LE'),
('Christian Nørgaard', 29, 25000000.00, 'BRE', 'VOL'),
('Vitaly Janelt', 25, 25000000.00, 'BRE', 'MC'),
('Bryan Mbeumo', 24, 30000000.00, 'BRE', 'PE'),
('Ivan Toney', 27, 60000000.00, 'BRE', 'CA'),
('Yoane Wissa', 27, 20000000.00, 'BRE', 'PD'),
('Frank Onyeka', 26, 15000000.00, 'BRE', 'VOL'),
('Saman Ghoddos', 30, 10000000.00, 'BRE', 'MEI'),
('Keane Lewis-Potter', 23, 10000000.00, 'BRE', 'PE'),
('Shandon Baptiste', 25, 10000000.00, 'BRE', 'MC'),
('Ben Mee', 34, 5000000.00, 'BRE', 'ZAG');

-- Fulham:

INSERT INTO Elenco (Nome_jogador, Idade, Valor_mercado, Sigla, Sigla_posicao) VALUES
('Bernd Leno', 31, 10000000.00, 'FUL', 'GOL'),
('Antonee Robinson', 26, 20000000.00, 'FUL', 'LD'),
('Tosin Adarabioyo', 25, 25000000.00, 'FUL', 'ZAG'),
('Tim Ream', 37, 5000000.00, 'FUL', 'ZAG'),
('Kenny Tete', 27, 15000000.00, 'FUL', 'LE'),
('Joao Palhinha', 28, 35000000.00, 'FUL', 'VOL'),
('Andreas Pereira', 27, 25000000.00, 'FUL', 'MC'),
('Harrison Reed', 29, 15000000.00, 'FUL', 'MC'),
('Willian', 35, 5000000.00, 'FUL', 'PE'),
('Raúl Jiménez', 33, 15000000.00, 'FUL', 'CA'),
('Aleksandar Mitrović', 29, 40000000.00, 'FUL', 'CA'),
('Bobby De Cordova-Reid', 28, 15000000.00, 'FUL', 'PD'),
('Carlos Vinícius', 28, 10000000.00, 'FUL', 'CA'),
('Lukas Radebe', 29, 10000000.00, 'FUL', 'MC'),
('Paulinha', 28, 15000000.00, 'FUL', 'VOL');

-- Crystal Palace:

INSERT INTO Elenco (Nome_jogador, Idade, Valor_mercado, Sigla, Sigla_posicao) VALUES
('Vicente Guaita', 37, 5000000.00, 'CRY', 'GOL'),
('Joachim Andersen', 27, 30000000.00, 'CRY', 'ZAG'),
('Marc Guéhi', 23, 35000000.00, 'CRY', 'ZAG'),
('Tyrick Mitchell', 24, 25000000.00, 'CRY', 'LE'),
('Joel Ward', 34, 5000000.00, 'CRY', 'LD'),
('Cheikhou Kouyaté', 34, 10000000.00, 'CRY', 'VOL'),
('Luka Milivojević', 33, 10000000.00, 'CRY', 'MC'),
('Eberechi Eze', 25, 45000000.00, 'CRY', 'MEI'),
('Jordan Ayew', 32, 15000000.00, 'CRY', 'PD'),
('Wilfried Zaha', 31, 50000000.00, 'CRY', 'PE'),
('Odsonne Édouard', 25, 25000000.00, 'CRY', 'CA'),
('Jean-Philippe Mateta', 26, 20000000.00, 'CRY', 'CA'),
('Nathaniel Clyne', 32, 10000000.00, 'CRY', 'LD'),
('Jairo Riedewald', 27, 10000000.00, 'CRY', 'MC'),
('Chris Richards', 23, 15000000.00, 'CRY', 'ZAG');

-- Bournemouth:

INSERT INTO Elenco (Nome_jogador, Idade, Valor_mercado, Sigla, Sigla_posicao) VALUES
('Neto', 34, 15000000.00, 'BOU', 'GOL'),
('Marcos Senesi', 26, 20000000.00, 'BOU', 'ZAG'),
('Chris Mepham', 26, 15000000.00, 'BOU', 'ZAG'),
('Jefferson Lerma', 29, 20000000.00, 'BOU', 'VOL'),
('Philip Billing', 28, 25000000.00, 'BOU', 'MC'),
('Lloyd Kelly', 25, 20000000.00, 'BOU', 'LE'),
('Adam Smith', 32, 10000000.00, 'BOU', 'LD'),
('Marcus Tavernier', 24, 30000000.00, 'BOU', 'MEI'),
('Ryan Christie', 29, 15000000.00, 'BOU', 'MEI'),
('Dominic Solanke', 26, 25000000.00, 'BOU', 'CA'),
('Philip Billing', 28, 25000000.00, 'BOU', 'MC'),
('Jaidon Anthony', 24, 15000000.00, 'BOU', 'PE'),
('Dango Ouattara', 21, 20000000.00, 'BOU', 'PE'),
('Emiliano Marcondes', 29, 10000000.00, 'BOU', 'MEI'),
('Antoine Semenyo', 23, 10000000.00, 'BOU', 'CA');

-- Nottingham Forest:

INSERT INTO Elenco (Nome_jogador, Idade, Valor_mercado, Sigla, Sigla_posicao) VALUES
('Dean Henderson', 26, 20000000.00, 'NFO', 'GOL'),
('Willy Boly', 32, 15000000.00, 'NFO', 'ZAG'),
('Scott McKenna', 27, 20000000.00, 'NFO', 'ZAG'),
('Renan Lodi', 25, 25000000.00, 'NFO', 'LE'),
('Neco Williams', 23, 20000000.00, 'NFO', 'LD'),
('Orel Mangala', 25, 20000000.00, 'NFO', 'VOL'),
('Morgan Gibbs-White', 24, 30000000.00, 'NFO', 'MC'),
('Jesse Lingard', 31, 15000000.00, 'NFO', 'MEI'),
('Taiwo Awoniyi', 26, 25000000.00, 'NFO', 'CA'),
('Brennan Johnson', 22, 40000000.00, 'NFO', 'PE'),
('Emmanuel Dennis', 26, 15000000.00, 'NFO', 'CA'),
('Serge Aurier', 31, 10000000.00, 'NFO', 'LD'),
('Jack Colback', 34, 5000000.00, 'NFO', 'MC'),
('Cheikhou Kouyaté', 34, 10000000.00, 'NFO', 'VOL'),
('Harry Toffolo', 28, 10000000.00, 'NFO', 'LE');

-- Sheffield United:

INSERT INTO Elenco (Nome_jogador, Idade, Valor_mercado, Sigla, Sigla_posicao) VALUES
('Wes Foderingham', 32, 6000000.00, 'SHE', 'GOL'),
('John Egan', 31, 12000000.00, 'SHE', 'ZAG'),
('Chris Basham', 35, 5000000.00, 'SHE', 'ZAG'),
('Max Lowe', 26, 7000000.00, 'SHE', 'LE'),
('George Baldock', 30, 10000000.00, 'SHE', 'LD'),
('Sander Berge', 26, 20000000.00, 'SHE', 'VOL'),
('James McAtee', 21, 15000000.00, 'SHE', 'MC'),
('Oliver Norwood', 33, 8000000.00, 'SHE', 'MC'),
('Iliman Ndiaye', 23, 25000000.00, 'SHE', 'PE'),
('Billy Sharp', 37, 3000000.00, 'SHE', 'CA'),
('Ben Osborn', 29, 10000000.00, 'SHE', 'MEI'),
('Anel Ahmedhodžić', 24, 18000000.00, 'SHE', 'ZAG'),
('Tommy Doyle', 21, 10000000.00, 'SHE', 'MC'),
('Daniel Jebbison', 20, 12000000.00, 'SHE', 'CA');

-- Burnley:

INSERT INTO Elenco (Nome_jogador, Idade, Valor_mercado, Sigla, Sigla_posicao) VALUES
('James Trafford', 22, 8000000.00, 'BUR', 'GOL'),
('Jordan Beyer', 24, 15000000.00, 'BUR', 'ZAG'),
('Hannes Delcroix', 25, 10000000.00, 'BUR', 'ZAG'),
('Vitaliy Mykolenko', 24, 12000000.00, 'BUR', 'LE'),
('Connor Roberts', 28, 7000000.00, 'BUR', 'LD'),
('Jack Cork', 34, 5000000.00, 'BUR', 'VOL'),
('Josh Brownhill', 28, 8000000.00, 'BUR', 'MC'),
('Lyle Foster', 23, 10000000.00, 'BUR', 'CA'),
('Nathan Redmond', 29, 10000000.00, 'BUR', 'PE'),
('Sander Berge', 26, 18000000.00, 'BUR', 'MC'),
('Ashley Barnes', 35, 2000000.00, 'BUR', 'CA'),
('Anass Zaroury', 23, 15000000.00, 'BUR', 'PE'),
('Zeki Amdouni', 25, 20000000.00, 'BUR', 'CA'),
('Johann Gudmundsson', 33, 4000000.00, 'BUR', 'MEI');

-- Luton Town:

INSERT INTO Elenco (Nome_jogador, Idade, Valor_mercado, Sigla, Sigla_posicao) VALUES
('Thomas Kaminski', 30, 6000000.00, 'LUT', 'GOL'),
('Allan Campbell', 25, 8000000.00, 'LUT', 'ZAG'),
('Reece Burke', 26, 7000000.00, 'LUT', 'ZAG'),
('Mads Andersen', 27, 8000000.00, 'LUT', 'ZAG'),
('Amari’i Bell', 29, 5000000.00, 'LUT', 'LE'),
('Jordan Clark', 30, 6000000.00, 'LUT', 'MC'),
('Tom Lockyer', 29, 7000000.00, 'LUT', 'ZAG'),
('Elijah Adebayo', 25, 10000000.00, 'LUT', 'CA'),
('Carlton Morris', 28, 15000000.00, 'LUT', 'CA'),
('Pelly-Ruddock Mpanzu', 30, 5000000.00, 'LUT', 'MC'),
('Luke Freeman', 31, 4000000.00, 'LUT', 'MEI'),
('Luke Berry', 29, 6000000.00, 'LUT', 'MC'),
('Fred Onyedinma', 26, 7000000.00, 'LUT', 'PE'),
('Dan Potts', 29, 5000000.00, 'LUT', 'LE');

-- Everton:

INSERT INTO Elenco (Nome_jogador, Idade, Valor_mercado, Sigla, Sigla_posicao) VALUES
('Jordan Pickford', 29, 25000000.00, 'EVE', 'GOL'),
('Ben Godfrey', 25, 15000000.00, 'EVE', 'ZAG'),
('James Tarkowski', 30, 20000000.00, 'EVE', 'ZAG'),
('Yerry Mina', 30, 10000000.00, 'EVE', 'ZAG'),
('Seamus Coleman', 34, 5000000.00, 'EVE', 'LD'),
('Vitaliy Mykolenko', 24, 10000000.00, 'EVE', 'LE'),
('Alex Iwobi', 27, 25000000.00, 'EVE', 'MEI'),
('Abdoulaye Doucouré', 30, 10000000.00, 'EVE', 'VOL'),
('Dwight McNeil', 24, 25000000.00, 'EVE', 'PE'),
('Dominic Calvert-Lewin', 26, 40000000.00, 'EVE', 'CA'),
('Neal Maupay', 27, 15000000.00, 'EVE', 'CA'),
('Amadou Onana', 22, 25000000.00, 'EVE', 'VOL'),
('James Garner', 22, 12000000.00, 'EVE', 'MC'),
('Andros Townsend', 32, 5000000.00, 'EVE', 'PE');

-- West Ham United:

INSERT INTO Elenco (Nome_jogador, Idade, Valor_mercado, Sigla, Sigla_posicao) VALUES
('Alphonse Areola', 30, 10000000.00, 'WHU', 'GOL'),
('Kurt Zouma', 29, 20000000.00, 'WHU', 'ZAG'),
('Angelo Ogbonna', 35, 6000000.00, 'WHU', 'ZAG'),
('Aaron Cresswell', 34, 5000000.00, 'WHU', 'LE'),
('Vladimir Coufal', 31, 10000000.00, 'WHU', 'LD'),
('Declan Rice', 24, 80000000.00, 'WHU', 'VOL'),
('Lucas Paquetá', 26, 50000000.00, 'WHU', 'MC'),
('Tomas Souček', 29, 20000000.00, 'WHU', 'VOL'),
('Jarrod Bowen', 27, 30000000.00, 'WHU', 'PE'),
('Michail Antonio', 33, 15000000.00, 'WHU', 'CA'),
('Saïd Benrahma', 28, 20000000.00, 'WHU', 'MEI'),
('Danny Ings', 31, 10000000.00, 'WHU', 'CA'),
('Maxwel Cornet', 27, 20000000.00, 'WHU', 'PE'),
('Ben Johnson', 23, 10000000.00, 'WHU', 'LD');

-- Tabela arbitros:

INSERT INTO arbitros (id_arbitro, nome_arbitro)
VALUES
(1, 'Anthony Taylor'),
(2, 'Michael Oliver'),
(3, 'Chris Kavanagh'),
(4, 'Simon Hooper'),
(5, 'Paul Tierney'),
(6, 'Andy Madley'),
(7, 'John Brooks'),
(8, 'Robert Jones'),
(9, 'Tim Robinson'),
(10, 'Jarred Gillett'),
(11, 'Craig Pawson'),
(12, 'Stuart Attwell'),
(13, 'David Coote'),
(14, 'Samuel Barrott'),
(15, 'Michael Salisbury'),
(16, 'Darren England'),
(17, 'Peter Bankes'),
(18, 'Thomas Bramall'),
(19, 'Tony Harrington'),
(20, 'Graham Scott'),
(21, 'Darren Bond'),
(22, 'Joshua Smith'),
(23, 'Samuel Allison'),
(24, 'Matthew Donohue'),
(25, 'Lewis Smith'),
(26, 'Rebecca Welch'),
(27, 'Robert Madley'),
(28, 'Sunny Singh');

-- Tabela jogos_arbitros:

INSERT INTO Jogos_Arbitros (ID_Jogo, ID_Arbitro) VALUES
(1, 1),  -- Jogo 1 arbitrado por Anthony Taylor
(1, 2),  -- Jogo 1 também tem Michael Oliver como assistente
(2, 3),  -- Jogo 2 arbitrado por Chris Kavanagh
(2, 4),  
(3, 5),  
(3, 6),  
(4, 7),  
(4, 8),  
(5, 9),  
(5, 10),  
(6, 11),  
(6, 12),  
(7, 13),  
(7, 14),  
(8, 15),  
(8, 16),  
(9, 17),  
(9, 18),  
(10, 19),  
(10, 20),  
(11, 21),  
(11, 22),  
(12, 23),  
(12, 24),  
(13, 25),  
(13, 26),  
(14, 27),  
(14, 28);

-- Tabela estadio:

INSERT INTO Estadio (Nome_estadio, Ano_criacao, Gramado, Capacidade, Sigla) VALUES
('Emirates Stadium', 2006, 'Grama Natural', 60704, 'ARS'),
('Villa Park', 1897, 'Grama Natural', 42682, 'AST'),
('Vitality Stadium', 1910, 'Grama Natural', 11307, 'BOU'),
('Gtech Community Stadium', 2020, 'Grama Natural', 17250, 'BRE'),
('Amex Stadium', 2011, 'Grama Natural', 31800, 'BHA'),
('Turf Moor', 1883, 'Grama Natural', 21944, 'BUR'),
('Stamford Bridge', 1877, 'Grama Natural', 40343, 'CHE'),
('Selhurst Park', 1924, 'Grama Natural', 25486, 'CRY'),
('Goodison Park', 1892, 'Grama Natural', 39414, 'EVE'),
('Craven Cottage', 1896, 'Grama Natural', 25700, 'FUL'),
('Anfield', 1884, 'Grama Natural', 53394, 'LIV'),
('Kenilworth Road', 1905, 'Grama Natural', 11880, 'LUT'),
('Etihad Stadium', 2003, 'Grama Natural', 53400, 'MCI'),
('Old Trafford', 1910, 'Grama Natural', 74310, 'MUN'),
('St. James Park', 1892, 'Grama Natural', 52305, 'NEW'),
('City Ground', 1898, 'Grama Natural', 30445, 'NFO'),
('Bramall Lane', 1855, 'Grama Natural', 32050, 'SHE'),
('Tottenham Hotspur Stadium', 2019, 'Grama Híbrida', 62850, 'TOT'),
('London Stadium', 2012, 'Grama Natural', 62500, 'WHU'),
('Molineux Stadium', 1889, 'Grama Natural', 31750, 'WOL');

-- Tabela departamentos:

INSERT INTO Departamentos (SIGLA_departamento, Nome_departamento) VALUES
('Futebol', 'Departamento de Futebol'),
('Marketing', 'Departamento de Marketing'),
('Financeiro', 'Departamento Financeiro'),
('Médico', 'Departamento Médico');

-- Tabela rel11:

INSERT INTO Rel11 (Sigla, SIGLA_departamento) VALUES
-- Departamento de Futebol
('ARS', 'Futebol'),
('MCI', 'Futebol'),
('MUN', 'Futebol'),
('LIV', 'Futebol'),
('CHE', 'Futebol'),
('TOT', 'Futebol'),
('NEW', 'Futebol'),
('AST', 'Futebol'),
('WHU', 'Futebol'),
('BHA', 'Futebol'),
('BRE', 'Futebol'),
('FUL', 'Futebol'),
('CRY', 'Futebol'),
('BOU', 'Futebol'),
('WOL', 'Futebol'),
('EVE', 'Futebol'),
('NFO', 'Futebol'),
('BUR', 'Futebol'),
('SHE', 'Futebol'),
('LUT', 'Futebol'),

-- Departamento de Marketing
('ARS', 'Marketing'),
('MCI', 'Marketing'),
('MUN', 'Marketing'),
('LIV', 'Marketing'),
('CHE', 'Marketing'),
('TOT', 'Marketing'),
('NEW', 'Marketing'),
('AST', 'Marketing'),
('WHU', 'Marketing'),
('BHA', 'Marketing'),

-- Departamento Financeiro
('ARS', 'Financeiro'),
('MCI', 'Financeiro'),
('MUN', 'Financeiro'),
('LIV', 'Financeiro'),
('CHE', 'Financeiro'),

-- Departamento Médico
('ARS', 'Médico'),
('MCI', 'Médico'),
('MUN', 'Médico'),
('LIV', 'Médico'),
('CHE', 'Médico'),
('TOT', 'Médico'),
('NEW', 'Médico'),
('AST', 'Médico');

-- Tabela rel:

INSERT INTO Rel (Sigla, ID_requerimento) VALUES
('ARS', 1),  -- Arsenal patrocinado pela Adidas
('MCI', 2),  -- Man City patrocinado pela Puma
('MUN', 3),  -- Man United patrocinado pela Adidas
('LIV', 4),  -- Liverpool patrocinado pela Standard Chartered
('CHE', 5),  -- Chelsea patrocinado pela Nike
('TOT', 6),  -- Tottenham patrocinado pela AIA
('NEW', 7),  -- Newcastle patrocinado pela Castore
('AST', 8),  -- Aston Villa patrocinado pela Cazoo
('WHU', 9),  -- West Ham patrocinado pela Betway
('BHA', 10), -- Brighton patrocinado pela American Express
('BRE', 11), -- Brentford patrocinado pela Hollywoodbets
('FUL', 12), -- Fulham patrocinado pela W88
('CRY', 13), -- Crystal Palace patrocinado pela Cinch
('BOU', 14), -- Bournemouth patrocinado pela Dafabet
('WOL', 15), -- Wolves patrocinado pela Castore
('EVE', 16), -- Everton patrocinado pela Hummel
('NFO', 17), -- Nottingham patrocinado pela Ideagen
('BUR', 18), -- Burnley patrocinado pela Classic Football Shirts
('SHE', 19), -- Sheffield United patrocinado pela Errea
('LUT', 20); -- Luton Town patrocinado pela Umbro

-- Tabela classificacao:

INSERT INTO Classificacao (Sigla, Pontos, Vitoria, Empate, Derrota, Saldo_Gols, Gols_feitos, Gols_sofridos) VALUES
('MCI', 91, 28, 7, 3, 62, 96, 34),  -- 1º Manchester City (Campeão)
('ARS', 89, 28, 5, 5, 61, 91, 30),  -- 2º Arsenal
('LIV', 82, 24, 10, 4, 45, 87, 42), -- 3º Liverpool
('AST', 70, 21, 7, 10, 20, 76, 56), -- 4º Aston Villa
('TOT', 68, 20, 8, 10, 18, 74, 56), -- 5º Tottenham
('NEW', 66, 19, 9, 10, 22, 77, 55), -- 6º Newcastle
('MUN', 60, 18, 6, 14, -2, 57, 59), -- 7º Manchester United
('WHU', 58, 16, 10, 12, -3, 61, 64), -- 8º West Ham
('BHA', 55, 15, 10, 13, -1, 62, 63), -- 9º Brighton
('BRE', 52, 14, 10, 14, 0, 58, 58),  -- 10º Brentford
('FUL', 50, 13, 11, 14, -4, 55, 59), -- 11º Fulham
('CRY', 48, 12, 12, 14, -6, 52, 58), -- 12º Crystal Palace
('CHE', 47, 12, 11, 15, -8, 50, 58), -- 13º Chelsea
('BOU', 45, 12, 9, 17, -10, 48, 58), -- 14º Bournemouth
('WOL', 43, 11, 10, 17, -12, 47, 59), -- 15º Wolves
('EVE', 41, 10, 11, 17, -15, 45, 60), -- 16º Everton
('NFO', 39, 9, 12, 17, -20, 40, 60), -- 17º Nottingham Forest
('BUR', 35, 8, 11, 19, -25, 38, 63), -- 18º Burnley (Rebaixado)
('SHE', 32, 7, 11, 20, -30, 35, 65), -- 19º Sheffield United (Rebaixado)
('LUT', 30, 7, 9, 22, -35, 32, 67);  -- 20º Luton Town (Rebaixado)

-- Tabela funcionarios:

INSERT INTO Funcionarios (Nome_funcionario, Idade, Profissao, SIGLA_departamento, Sigla_time) VALUES
-- Departamento de Futebol
('Carlos Eduardo', 45, 'Técnico', 'Futebol', 'ARS'),
('Marcos Silva', 38, 'Auxiliar Técnico', 'Futebol', 'MCI'),
('Fernando Souza', 50, 'Preparador Físico', 'Futebol', 'MUN'),
('José Ricardo', 42, 'Treinador de Goleiros', 'Futebol', 'LIV'),
('Luiz Felipe', 39, 'Analista de Desempenho', 'Futebol', 'CHE'),
('Paulo César', 47, 'Massagista', 'Futebol', 'TOT'),
('Bruno Mendes', 41, 'Coordenador Técnico', 'Futebol', 'NEW'),
('Rafael Cardoso', 35, 'Scout', 'Futebol', 'AST'),
('Thiago Santos', 40, 'Supervisor Técnico', 'Futebol', 'WHU'),
('Diego Ferreira', 33, 'Treinador Sub-20', 'Futebol', 'BHA'),
('Lucas Moura', 44, 'Preparador Físico Sub-20', 'Futebol', 'BRE'),
('Vinícius Almeida', 38, 'Observador Técnico', 'Futebol', 'FUL'),
('Anderson Costa', 43, 'Coordenador da Base', 'Futebol', 'CRY'),
('Fábio Lima', 37, 'Psicólogo Esportivo', 'Futebol', 'BOU'),
('Eduardo Tavares', 46, 'Gerente de Futebol', 'Futebol', 'WOL'),
('Gustavo Nogueira', 48, 'Gestor de Contratações', 'Futebol', 'EVE'),
('Alexandre Santos', 36, 'Olheiro', 'Futebol', 'NFO'),
('João Pedro', 32, 'Tático', 'Futebol', 'BUR'),
('Henrique Lima', 45, 'Preparador de Condicionamento', 'Futebol', 'SHE'),
('Carlos Santana', 39, 'Analista de Jogadas', 'Futebol', 'LUT'),

-- Departamento de Marketing
('Ana Paula', 32, 'Gerente de Marketing', 'Marketing', 'ARS'),
('Ricardo Mendes', 40, 'Analista de Mídia', 'Marketing', 'MCI'),
('Juliana Castro', 29, 'Social Media', 'Marketing', 'MUN'),
('Vanessa Oliveira', 34, 'Coordenadora de Comunicação', 'Marketing', 'LIV'),
('Cláudio Ramos', 37, 'Gerente de Publicidade', 'Marketing', 'CHE'),
('Fernanda Martins', 28, 'Redatora Publicitária', 'Marketing', 'TOT'),
('Thiago Lopes', 31, 'Designer Gráfico', 'Marketing', 'NEW'),
('Isabela Souza', 30, 'Fotógrafa', 'Marketing', 'AST'),
('Lucas Ribeiro', 35, 'Produtor Audiovisual', 'Marketing', 'WHU'),
('Camila Dias', 27, 'Estrategista Digital', 'Marketing', 'BHA'),
('Gabriela Alves', 29, 'Especialista em SEO', 'Marketing', 'BRE'),
('Eduardo Teixeira', 41, 'Diretor de Comunicação', 'Marketing', 'FUL'),
('Roberta Nunes', 33, 'Executiva de Patrocínios', 'Marketing', 'CRY'),
('Fábio Oliveira', 38, 'Planejador de Campanhas', 'Marketing', 'BOU'),
('Beatriz Souza', 36, 'Analista de Redes Sociais', 'Marketing', 'WOL'),
('Renato Farias', 39, 'Gerente de Relacionamento com a Torcida', 'Marketing', 'EVE'),
('Luciana Torres', 28, 'Produtora de Conteúdo', 'Marketing', 'NFO'),
('Bruno Santiago', 30, 'Coordenador de Eventos', 'Marketing', 'BUR'),
('Camila Freitas', 29, 'Assessora de Imprensa', 'Marketing', 'SHE'),
('Pedro Henrique', 32, 'Fotógrafo de Campo', 'Marketing', 'LUT'),

-- Departamento Financeiro
('Roberto Lima', 52, 'Diretor Financeiro', 'Financeiro', 'ARS'),
('Mariana Alves', 37, 'Analista Contábil', 'Financeiro', 'MCI'),
('Paulo Henrique', 41, 'Tesoureiro', 'Financeiro', 'MUN'),
('Bruno Almeida', 40, 'Gerente de Finanças', 'Financeiro', 'LIV'),
('Rodrigo Martins', 45, 'Analista de Custos', 'Financeiro', 'CHE'),
('Daniel Souza', 39, 'Controlador Financeiro', 'Financeiro', 'TOT'),
('Fernanda Lopes', 31, 'Analista de Planejamento', 'Financeiro', 'NEW'),
('Carla Mendes', 35, 'Consultora Financeira', 'Financeiro', 'AST'),
('Lucas Tavares', 50, 'Auditor Interno', 'Financeiro', 'WHU'),
('Tatiane Borges', 44, 'Contadora', 'Financeiro', 'BHA'),
('Ricardo Farias', 37, 'Especialista em Investimentos', 'Financeiro', 'BRE'),
('Alex Nascimento', 46, 'Gerente de Orçamentos', 'Financeiro', 'FUL'),
('Beatriz Mendes', 38, 'Analista de Pagamentos', 'Financeiro', 'CRY'),
('João Batista', 42, 'Analista Fiscal', 'Financeiro', 'BOU'),
('Renata Lima', 30, 'Supervisora de Contas', 'Financeiro', 'WOL'),
('Patrícia Castro', 29, 'Analista de Recebíveis', 'Financeiro', 'EVE'),
('Carlos Ramos', 41, 'Coordenador Financeiro', 'Financeiro', 'NFO'),
('Eduardo Santos', 47, 'Analista de Contratos', 'Financeiro', 'BUR'),
('Mateus Oliveira', 35, 'Gestor de Recursos', 'Financeiro', 'SHE'),
('Daniel Rocha', 43, 'Analista de Gestão de Riscos', 'Financeiro', 'LUT'),

-- Departamento Médico
('Dra. Camila Rezende', 48, 'Médica do Clube', 'Médico', 'ARS'),
('Dr. João Peixoto', 50, 'Fisioterapeuta', 'Médico', 'MCI'),
('Carla Rodrigues', 34, 'Nutricionista', 'Médico', 'MUN'),
('Marcelo Duarte', 42, 'Preparador Físico Médico', 'Médico', 'LIV'),
('Fernanda Sampaio', 39, 'Coordenadora Médica', 'Médico', 'CHE'),
('Lucas Farias', 36, 'Ortopedista', 'Médico', 'TOT'),
('Rafaela Silva', 32, 'Psicóloga Esportiva', 'Médico', 'NEW'),
('Eduardo Campos', 45, 'Massagista', 'Médico', 'AST'),
('Bruna Oliveira', 31, 'Terapeuta Ocupacional', 'Médico', 'WHU'),
('Guilherme Costa', 38, 'Fisiologista', 'Médico', 'BHA'),
('Vinícius Rocha', 44, 'Especialista em Reabilitação', 'Médico', 'BRE'),
('Fernanda Souza', 33, 'Enfermeira Esportiva', 'Médico', 'FUL'),
('Rodrigo Pereira', 41, 'Cardiologista', 'Médico', 'CRY'),
('Jéssica Mendes', 37, 'Nutricionista Clínica', 'Médico', 'BOU'),
('Henrique Nunes', 46, 'Médico de Emergência', 'Médico', 'WOL'),
('Gustavo Amaral', 48, 'Supervisor Médico', 'Médico', 'EVE'),
('Lucas Carvalho', 35, 'Fisioterapeuta Sub-20', 'Médico', 'NFO'),
('Roberta Andrade', 39, 'Neurocientista do Esporte', 'Médico', 'BUR'),
('Ricardo Pacheco', 50, 'Analista de Saúde Esportiva', 'Médico', 'SHE'),
('Marcelo Antunes', 43, 'Terapeuta Físico', 'Médico', 'LUT');

CREATE OR REPLACE PROCEDURE AtualizarTitulosTime(
    IN sigla_time VARCHAR(10),
    IN novos_titulos INT
)
LANGUAGE plpgsql
AS $$
BEGIN
    -- Atualiza o número de títulos do time
    UPDATE Time
    SET N_Titulos = novos_titulos
    WHERE Sigla = sigla_time;

    -- Verifica se a atualização foi bem-sucedida
    IF FOUND THEN
        RAISE NOTICE 'Número de títulos do time % atualizado para %.', sigla_time, novos_titulos;
    ELSE
        RAISE NOTICE 'Time com sigla % não encontrado.', sigla_time;
    END IF;
END;
$$;

CREATE OR REPLACE VIEW ClassificacaoDetalhada AS
SELECT
    T.Sigla,
    T.Nome_clube,
    C.Pontos,
    C.Vitoria,
    C.Empate,
    C.Derrota,
    C.Saldo_Gols,
    C.Gols_feitos,
    C.Gols_sofridos
FROM
    Classificacao C
JOIN
    Time T ON C.Sigla = T.Sigla
ORDER BY
    C.Pontos DESC;