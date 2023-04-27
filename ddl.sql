CREATE TABLE Autores (
    id INTEGER PRIMARY KEY,
    nome_completo VARCHAR(255),
    resumo_cv VARCHAR(255),
    colaborador_cesar INTEGER
);
 
ALTER TABLE Autores ADD CONSTRAINT FK_Autores_2
    FOREIGN KEY (id, ???)
    REFERENCES autores_artigos (autor_id, ???);