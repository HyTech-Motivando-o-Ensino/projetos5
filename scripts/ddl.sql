USE pj5data;

CREATE TABLE IF NOT EXISTS arquivos_xml (
    id INTEGER NOT NULL AUTO_INCREMENT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP, 
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    payload MEDIUMTEXT,
    status_extracao INTEGER,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS autores (
    id INTEGER NOT NULL AUTO_INCREMENT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    nome_completo VARCHAR(255),
    resumo_cv VARCHAR(255),
    colaborador_cesar INTEGER,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS artigos (
    id INTEGER NOT NULL AUTO_INCREMENT,
    natureza VARCHAR(255),
    titulo VARCHAR(255),
    ano DATE,
    idioma VARCHAR(100),
    doi VARCHAR(100) UNIQUE,
    periodico_revista_id INTEGER,
    pdf_file VARCHAR(100),
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS autores_artigos (
    autor_id INTEGER,
    artigo_id INTEGER,
    PRIMARY KEY (autor_id, artigo_id)
);

CREATE TABLE IF NOT EXISTS periodicos_revistas (
    id INTEGER NOT NULL AUTO_INCREMENT,
    issn VARCHAR(100),
    nome VARCHAR(100),
    estrato VARCHAR(50),
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS orientacoes (
    id INTEGER NOT NULL AUTO_INCREMENT,
    titulo VARCHAR(100),
    ano INTEGER,
    curso_id INTEGER,
    orientador_id INTEGER,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS cursos (
    id INTEGER NOT NULL AUTO_INCREMENT,
    nome VARCHAR(100) UNIQUE,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS orientacao_area_conhecimento (
    area_conhecimento_id INTEGER,
    orientacao_id INTEGER
);

CREATE TABLE IF NOT EXISTS grande_area_conhecimento (
    id INTEGER NOT NULL AUTO_INCREMENT,
	nome VARCHAR(255),
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS autores_area_conhecimento (
	autor_id INTEGER,
	area_conhecimento_id INTEGER,
	PRIMARY KEY (autor_id, area_conhecimento_id)
);

CREATE TABLE IF NOT EXISTS artigo_area_conhecimento (
	area_conhecimento_id INTEGER,
	artigo_id INTEGER,
	PRIMARY KEY (area_conhecimento_id, artigo_id)
);

IF NOT EXISTS (
    SELECT NULL
    FROM information_schema.TABLE_CONSTRAINTS
    WHERE
        CONSTRAINT_SCHEMA = DATABASE() AND
        CONSTRAINT_NAME = 'FK_autores_artigos_2' AND
        CONSTRAINT_TYPE = 'FOREIGN_KEY'
)
THEN
    ALTER TABLE autores_artigos ADD CONSTRAINT FK_autores_artigos_2
        FOREIGN KEY (autor_id)
        REFERENCES autores (id);
 
ALTER TABLE autores_artigos ADD CONSTRAINT FK_autores_artigos_3
    FOREIGN KEY (artigo_id)
    REFERENCES artigos (id);
 
ALTER TABLE artigos ADD CONSTRAINT FK_artigos_3
    FOREIGN KEY (periodico_revista_id)
    REFERENCES periodicos_revistas (id);
 
ALTER TABLE autores_artigos ADD CONSTRAINT FK_artigos_4
    FOREIGN KEY (artigo_id)
    REFERENCES artigos (id);
 
ALTER TABLE autores_artigos ADD CONSTRAINT FK_autores_2
    FOREIGN KEY (autor_id)
    REFERENCES autores (id);

ALTER TABLE orientacoes ADD CONSTRAINT FK_orientacoes_autores
    FOREIGN KEY (orientador_id)
    REFERENCES autores (id);

ALTER TABLE orientacoes ADD CONSTRAINT FK_orientacoes_cursos
    FOREIGN KEY (curso_id)
    REFERENCES cursos (id);

ALTER TABLE orientacao_area_conhecimento ADD CONSTRAINT FK_orienacao_area_conhecimento_area_conhecimento
    FOREIGN KEY (area_conhecimento_id)
    REFERENCES grande_area_conhecimento (id);

ALTER TABLE autores_area_conhecimento ADD CONSTRAINT
 FOREIGN KEY(autor_id) 
 REFERENCES autores(id);

ALTER TABLE autores_area_conhecimento ADD CONSTRAINT
 FOREIGN KEY(area_conhecimento_id) 
 REFERENCES grande_area_conhecimento(id);

ALTER TABLE artigo_area_conhecimento ADD CONSTRAINT
 FOREIGN KEY(area_conhecimento_id) 
 REFERENCES grande_area_conhecimento(id);

ALTER TABLE artigo_area_conhecimento ADD CONSTRAINT
 FOREIGN KEY(artigo_id) 
 REFERENCES artigos(id);
