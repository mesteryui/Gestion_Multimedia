from accederBaseDatos import *

database = conectar_base()
def anadir_descripcion(titulo,descripcion):
    database[1].execute(f"update contenido set descripcion='{descripcion}' where titulo='{titulo}';")
    database[0].commit()

def generar_codigo_contenido(tipo):
    """
    Pasando el tipo de contenido a añadir creamos el numero que se le añade al codigo
    :param tipo: el tipo de contenido a añadir
    :return: (numero ultimo codc)+1 o 1 si no existen codigos con la letra para ese tipo definido
    """
    database[1].execute(f"select codc from contenido where tipo='{tipo}'")
    letra = tipo[0].lower()
    lista = database[1].fetchall()
    if len(lista)==0:
        return 1
    else:
        lista_ordenada = sorted(lista, key=lambda x: int(x[0][1:]))
        resultado = lista_ordenada[len(lista_ordenada)-1][0]
        resultado = resultado.replace(letra,"")
        return int(resultado)+1

def generar_codigo_plataforma():
    database[1].execute("select codpl from plataformas;")
    lista = database[1].fetchall()
    lista_ordenada = sorted(lista, key=lambda x: int(x[0][2:]))
    resultado = lista_ordenada[len(lista_ordenada) - 1][0]
    resultado = resultado.replace("pl","")
    return int(resultado) + 1

def obtenercodigo_contenido(titulo):
    """
    Obtener el codigo de un item de contenido
    :param titulo: el titulo del contenido
    :return: el codigo de ese contenido
    """
    database[1].execute(f"select codc from contenido where titulo='{titulo}'")
    episodio = database[1].fetchone()
    return episodio[0]

def obtener_episodios_tipo_contenido(tipo):
    database[1].execute(f"select titulo,episodios_vistos,episodios_totales from contenido,episodios where episodios.codc=contenido.codc and tipo='{tipo}'")
    datos = database[1].fetchall()
    articul = "las" if tipo=="Serie" else "los"
    articul2 = "el" if tipo=="Anime" else "la"
    print(f"De {articul} {tipo.lower()}s se tiene la siguiente informacion:\n")
    for dato in datos:
        print(f"De {articul2} {tipo.lower()} {dato[0]} se han visto {dato[1]} de {dato[2]} episodios\n")

def insertar_contenido_plataforma(titulo,nombreplataforma):
    """
    Insertar contenido a plataforma
    :param titulo: el titulo del contenido
    :param nombreplataforma: el nombre de la plataforma
    :return:
    """
    codc = obtenercodigo_contenido(titulo)
    database[1].execute(f"select codpl from plataformas where nomg='{nombreplataforma}'")
    codpl = database[1].fetchone()[0]
    database[1].execute(f"insert into disponible values('{codc}','{codpl}')")
    database[0].commit()
def saber_plataforma_veo_contenido(titulo):
    """
    Te permite ver la plataforma en la que ves un contenido
    :param titulo: el titulo del contenido
    """
    database[1].execute(
        f"select nomg,url,tipo from contenido join disponible on contenido.codc=disponible.codc join plataformas on plataformas.codpl=disponible.codpl where titulo='{titulo}';")
    plataformas = database[1].fetchall()
    tipo = plataformas[0][2]
    tipo = tipo.lower()
    for plataforma in plataformas:
        if tipo == "anime":
            print(f"El {tipo} {titulo} es visto desde {plataforma[0]} cuya url es {plataforma[1]}\n")
        else:
            print(f"La {tipo} {titulo} es vista desde {plataforma[0]} cuya url es {plataforma[1]}\n")


def episodios_saber(titulo):
    """
    Nos permite saber cuantos episodios hemos visto de una serie o anime
    :param titulo: el titulo de esa serie o anime
    """
    database[1].execute(
        f"select episodios_vistos,episodios_totales,tipo from contenido,episodios where titulo='{titulo}' and episodios.codc=contenido.codc;")
    episodios = database[1].fetchall()
    vistos = 0 if episodios[0][0] is None else episodios[0][0]
    tipo = episodios[0][2]
    tipo = tipo.lower()
    if tipo == "anime":
        print(f"Del {tipo} {titulo} han sido vistos {vistos} de {episodios[0][1]} episodios\n")
    else:
        print(f"De la {tipo} {titulo} han sido vistos {vistos} de {episodios[0][1]} episodios\n")





def anadirepisodios_vistos(titulo, ep_vistos):
    """
    Permite añadir episodios nuevos despues de haber definido la serie/anime o demás
    :param titulo: el titulo de la serie o anime
    :param ep_vistos: los episodios vistos
    """
    codigo = obtenercodigo_contenido(titulo)
    database[1].execute(f"update episodios set episodios_vistos='{ep_vistos}' where codc='{codigo}'")
    database[0].commit()


def saber_episodios_vistos(titulo):
    database[1].execute(f"select titulo,episodios_vistos,episodios_totales from contenido,episodios where titulo='{titulo}' and episodios.codc=contenido.codc;")
    return database[1].fetchall()


def main():
    op1 = 0
    while op1 < 5:
        print("1.Introducir Datos\n2.Ver datos\n3.Eliminar Dato\n4.Actualizar dato\n5.Salir")
        op1 = int(input())
        if op1 == 1:
            print("1.Contenido\n2.Plataformas\n3.Generos\n4.Contenido-Plataforma\n5.")
            op2 = int(input())
            if op2 == 1:
                titulo = input("Introduzca el titulo del contenido:")
                descripcion = input("Introduzca descripcion del contenido:")
                tipo = input("Introduzca el tipo de contenido")
                cod = tipo[0].lower()
                num = generar_codigo_contenido(tipo)
                codc = cod + str(num)
                database[1].execute(f"insert into contenido values('{codc}','{titulo}','{descripcion}','{tipo}')")
                database[0].commit()
                if tipo == "Serie" or "Anime":
                    print("Introduzca un numero:")
                    episodios_totales = input("Dime cuantos episodios tiene el contenido:")
                    database[1].execute(f"insert into episodios values('{codc}',1,'{episodios_totales}')")
                    database[0].commit()
                    opcion = input("Desea añadir los episodios vistos en caso de que haya visto alguno:")
                    opcion = opcion.lower()
                    if opcion == "si":
                        ep_vistos = input("Introduzca los episodios vistos:")
                        anadirepisodios_vistos(titulo,ep_vistos)
                    else:
                        continue
            elif op2 == 2:
                codpl = generar_codigo_plataforma()
                nompl = input("Introduzca el nombre de la plataforma:")
                url = input("Introduzca el enlace de acceso a la plataforma:")
                database[1].execute(f"insert into plataformas values('pl{codpl}','{nompl}','{url}')")
                database[0].commit()
            elif op2 == 4:
                titulo = input("Introduzca el titulo de la serie:")
                nombre_plat = input("Introduzca el nombre de la plataforma")
                insertar_contenido_plataforma(titulo,nombre_plat)


        elif op1 == 2:
            print(
                "1.Cuantos Episodios se han visto de un anime/serie especifico\n2.Saber cuantos episodios se han visto de animes/series\n3.En que plataforma veo contenido")
            op2 = int(input())
            if op2 == 1:
                titulo = input("Titulo de la serie/anime:")
                episodios_saber(titulo)
            elif op2 == 2:
                tipo = input("Introduce el tipo de contenido")
                obtener_episodios_tipo_contenido(tipo)
            elif op2 == 3:
                titulo = input("Dime el titulo del contenido:")
                saber_plataforma_veo_contenido(titulo)


        elif op1 == 4:
            print("1.Contenido\n2.Episodios\n3.Plataformas")
            op8 = int(input())
            if op8 == 1:
                print("1.Añadir descripcion")
                op9 = int(input())
                if op9 == 1:
                    titulo = input("Introduce el titulo del contenido al que deseas añadir la descripcion:")
                    descripcion = input("Introduce la descripcion a añadir")
                    anadir_descripcion(titulo,descripcion)

            elif op8 == 2:
                titulo = input("Introduzca el titulo del anime/serie:")
                ep_vistos = input("Introduzca en numero los episodios vistos:")
                anadirepisodios_vistos(titulo,ep_vistos)


if __name__ == '__main__':
    if database is psycopg2.Error:
        exit(0)
    else:
        main()
        cerrar_conexion(database)
