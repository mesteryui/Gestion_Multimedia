-- Eliminar tablas si existen previamente (ordenado de manera que primero se eliminen las dependientes)
DROP TABLE IF EXISTS disponible;
DROP TABLE IF EXISTS esde;
DROP TABLE IF EXISTS episodios;
DROP TABLE IF EXISTS plataformas;
DROP TABLE IF EXISTS generos;
DROP TABLE IF EXISTS contenido;

-- Estableciendo tablas
CREATE TABLE contenido (
    codc TEXT PRIMARY KEY,
    titulo TEXT NOT NULL,
    descripcion TEXT,
    visualizacion TEXT, -- Indica si se está viendo, ya se vio o está pendiente
    tipo TEXT NOT NULL
);

CREATE TABLE episodios (
    codc TEXT,
    temporada INTEGER,
    episodios_totales INTEGER NOT NULL,
    episodios_vistos INTEGER,
    estado TEXT, -- Por ejemplo: "En Emisión" o "Finalizado"
    PRIMARY KEY (codc, temporada),
    FOREIGN KEY (codc) REFERENCES contenido (codc)
);

CREATE TABLE generos (
    codg TEXT PRIMARY KEY,
    nomg TEXT NOT NULL
);

CREATE TABLE plataformas (
    codpl TEXT PRIMARY KEY,
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
    url_disponible TEXT, -- URL de la plataforma donde se encuentra el contenido
    PRIMARY KEY (codc, codpl),
    FOREIGN KEY (codc) REFERENCES contenido (codc),
    FOREIGN KEY (codpl) REFERENCES plataformas (codpl)
);
