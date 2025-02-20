/** Eliminar tablas si existen previamente **/
DROP TABLE IF EXISTS contenido;
DROP TABLE IF EXISTS episodios;
DROP TABLE IF EXISTS generos;
DROP TABLE IF EXISTS plataformas;
DROP TABLE IF EXISTS esde;
DROP TABLE IF EXISTS disponible;

PRAGMA foreign_keys = ON;

/** Estableciendo tablas **/
CREATE TABLE contenido (
    codc TEXT PRIMARY KEY, -- SQLite usa TEXT en lugar de varchar
    titulo TEXT NOT NULL,
    descripcion TEXT,
    visualizacion TEXT, -- Saber si estoy viendola o ya la he visto o está por ver para películas
    tipo TEXT NOT NULL
);

CREATE TABLE episodios (
    codc TEXT,
    temporada INTEGER, -- INTEGER para números
    episodios_totales INTEGER NOT NULL,
    episodios_vistos INTEGER,
    estado TEXT, -- Saber si está en Emisión o ha finalizado
    PRIMARY KEY (codc, temporada),
    FOREIGN KEY (codc) REFERENCES contenido (codc)
);

CREATE TABLE generos (
    codg TEXT PRIMARY KEY, -- TEXT en lugar de char(1)
    nomg TEXT NOT NULL
);

CREATE TABLE plataformas (
    codpl TEXT PRIMARY KEY, -- TEXT en lugar de varchar(10)
    nomg TEXT NOT NULL,
    url TEXT
);

CREATE TABLE esde (
    codc TEXT,
    codg TEXT,
    PRIMARY KEY (codc, codg),
    FOREIGN KEY (codc) REFERENCES contenido (codc),
    FOREIGN KEY (codg) REFERENCES generos (codg)
);

CREATE TABLE disponible (
    codc TEXT,
    codpl TEXT,
    url_disponible TEXT, -- La URL dentro de la plataforma donde se encuentra la serie
    PRIMARY KEY (codc, codpl),
    FOREIGN KEY (codc) REFERENCES contenido (codc),
    FOREIGN KEY (codpl) REFERENCES plataformas (codpl)
);
