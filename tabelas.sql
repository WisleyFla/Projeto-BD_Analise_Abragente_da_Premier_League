CREATE DATABASE premier_league;
Use premier_league;
CREATE TABLE Times (
    id_times INT PRIMARY KEY,
    Nome_time VARCHAR(100) NOT NULL,
    Fundacao DATE,
    Mascote VARCHAR(50)
);

SELECT*FROM time;