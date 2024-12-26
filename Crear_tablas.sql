/** Eliminar tablas si existen previamente**/
drop table if exists contenido cascade;
drop table if exists episodios cascade;
drop table if exists generos cascade;
drop table if exists plataformas cascade;
drop table if exists esde cascade;
drop table if exists disponible cascade;


/** Estableciendo tablas**/
create table contenido(
codc varchar(8),
titulo varchar(255) not null,
descripcion TEXT,
visualizacion varchar(9), /** Saber si estoy viendola o ya la he visto o esta por ver para peliculas**/
tipo varchar(50) not null,
primary key (codc)
);

create table episodios(
codc varchar(8),
temporada int, /** Aqui se añddiria el numero de temporada de esta manera se identificara a partir de la serie y la temporada**/
episodios_totales int NOT NULL,
episodios_vistos int,
estado varchar(16), /**Si es una serie o anime saber si esta en Emision o ha finalizado**/
primary key(codc,temporada),
foreign key(codc) references contenido(codc)
);

create table generos(
codg char(1),
nomg varchar(100) not null,
primary key (codg)
);

create table plataformas(
codpl varchar(10),
nomg varchar(100) not null,
url varchar(255),
primary key (codpl)
);

create table esde(
codc varchar(8),
codg char(1),
primary key(codc,codg),
foreign key (codc) references contenido,
foreign key (codg) references generos
);

create table disponible(
codc varchar(8),
codpl varchar(10),
url_disponible varchar(400), /**La url dentro de la plataforma donde se encuentra la serie por ejemplo
si esta en Netfilix esto incluiria la url de Netflix y el resto hasta la serie no se como hacerlo de forma que coja la url de plataformas y le añada lo que necesito**/
primary key (codc,codpl),
foreign key (codc) references contenido,
foreign key (codpl) references plataformas
);

