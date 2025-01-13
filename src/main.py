from accederBaseDatos import conectar_base,cerrar_conexion
from utils import generar_numero_nuevo_codigo, generar_codigo_genero

database = conectar_base()  # Obtenemos la conexion a la base de datos y un cursor el cual sera util en todas las funciones que hagamos


def mostrar_contenido(tipo:str) -> dict:
    """
    Pasandole el tipo de contenido nos muestra tod-o lo que hay de ese contenido
    :param tipo: el tipo de contenido
    :return: los contenidos en un diccionario
    """
    database[1].execute(f"select titulo from contenido where tipo='{tipo}'")
    contenidos = database[1].fetchall()  # Guardamos esos contenidos
    num = 0
    diccionario_titulos = dict()  # Definimos un diccionario donde se guardaran los numeros
    for contenido in contenidos:
        num += 1
        diccionario_titulos[num] = contenido[0]
        print(f"{num}.{contenido[0]}")

    return diccionario_titulos


def obtener_titulo_de_titulos(tipo:str):
    """
    Obtiene el titulo que le indiquemos aprovechando la funcion mostrar_contenido
    Args:
        tipo: el tipo de contenido lo necesitamos para la funcion mostrar_contenido
    Returns:
        El titulo si tod salio bien si no vuelve a iniciar la funcion main
    """
    titulos = mostrar_contenido(tipo)  # Mostrar los contenidos de un tipo y obtener diccionario de titulos numeros
    opcion = int(input("Introduzca una opcion en numero:"))  # Pedir una opcion
    titulo = titulos.get(opcion, "nose")  # Obtener el titulo correspondiente a esa opcion o devolver nose si no existe
    if titulo == "nose":  # Si es nose
        print("Lo siento esa opcion no es valida")  # Indicamos que la opcion no es valida
        main()  # Volvemos a la funcion main
    else:
        return titulo  # Devolvemos el titulo


def anadir_descripcion(titulo, descripcion):
    """
    Añadir descripcion al contenido
    :param titulo: el titulo del contenido
    :param descripcion: la descipcion a añadir
    """
    database[1].execute(
        f"update contenido set descripcion='{descripcion}' where titulo='{titulo}';")  # Añadir descripcion a un contenido
    database[0].commit()





def generar_codigo_contenido(tipo:str) -> str:
    """
    Pasando el tipo de contenido a añadir creamos el numero que se le añade al codigo y luego lo unimos a la letra
    :param tipo: el tipo de contenido a añadir
    :return: letra + (numero_contenido + 1)
    """
    # Ejecutamos la consulta para obtener los codigos
    letra = tipo[0].lower()  # Obtenemos la letra del tipo sacando el primer elemento como minuscula
    database[1].execute(f"select codc from contenido where tipo='{tipo}'")  # Obtenemos todos los codigos
    lista = database[1].fetchall()
    numero = generar_numero_nuevo_codigo(lista,letra)
    return letra + str(numero)


def generar_codigo_plataforma() -> str:
    """
    Generar el codigo numerico para plataformas
    Returns:
        El codigo de la plataforma
    """
    database[1].execute("select codpl from plataformas;")  # Obtener los codigos de las plataformas
    lista = database[1].fetchall()  # Guardarlos en una lista
    numero = generar_numero_nuevo_codigo(lista,"pl")
    return "pl" + str(numero)




def obtenercodigo_contenido(titulo) -> str:
    """
    Obtener el codigo de un item de contenido
    :param titulo: el titulo del contenido
    :return: el codigo de ese contenido
    """
    database[1].execute(f"select codc from contenido where titulo='{titulo}'")
    codc = database[1].fetchone()
    return codc[0]

def mostrar_generos_contendio(titulo):
    codc = obtenercodigo_contenido(titulo)
    database[1].execute(f"select tipo from contenido where codc='{codc}'")
    tipo = database[1].fetchone()[0]
    database[1].execute(f"select nomg from generos where codg in (select codg from esde where codc=(select codc from contenido where titulo='{titulo}'));")
    lista_generos = database[1].fetchall()
    longitud_lista_generos = len(lista_generos)-1
    texto_genero = ""
    for index,genero in enumerate(lista_generos):
        if index == longitud_lista_generos:
            texto_genero += genero[0]
        else:
            texto_genero += genero[0] + ","
    print(f"{tipo} {titulo} es de los siguientes generos:"
          f" {texto_genero}")
def obtener_episodios_tipo_contenido(tipo):
    database[1].execute(
        f"select titulo,coalesce(episodios_vistos,0),episodios_totales from contenido,episodios where episodios.codc=contenido.codc and tipo='{tipo}'")
    datos = database[1].fetchall()
    articul = "De las" if tipo == "Serie" or tipo == "Pelicula" else "De los"
    articul2 = "Del" if tipo == "Anime" else "De la"
    print(f"{articul} {tipo.lower()}s se tiene la siguiente informacion:\n")
    for dato in datos:
        print(f"{articul2} {tipo.lower()} {dato[0]} se han visto {dato[1]} de {dato[2]} episodios\n")


def insertar_contenido_plataforma(titulo, codpl):
    """
    Insertar contenido a plataforma
    :param titulo: el titulo del contenido
    :param  codpl: el codigo de la plataforma
    :return:
    """
    codc = obtenercodigo_contenido(titulo)
    database[1].execute(f"insert into disponible values('{codc}','{codpl}',null)")
    database[0].commit()


def saber_plataforma_veo_contenido(titulo):
    """
    Te permite ver la plataforma en la que ves un contenido
    :param titulo: el titulo del contenido
    """
    plataformas = database[1].execute(
        f"select nomg,url,tipo from contenido join disponible on contenido.codc=disponible.codc join plataformas on plataformas.codpl=disponible.codpl where titulo='{titulo}';").fetchall()
    for plataforma in plataformas:
        tipo = plataforma[2].lower()
        if tipo == "anime":
            print(f"El {tipo} {titulo} es visto desde {plataforma[0]} cuya url es {plataforma[1]}\n")
        else:
            print(f"La {tipo} {titulo} es vista desde {plataforma[0]} cuya url es {plataforma[1]}\n")


def episodios_saber_temporada(titulo, temporada):
    database[1].execute(
        f"select coalesce(episodios_vistos,0), episodios_totales from contenido JOIN episodios ON contenido.codc = episodios.codc where titulo='{titulo}' and temporad={temporada};")
    episodios = database[1].fetchall()
    temporad = pasar_temporada_letra(temporada)
    print(f"De {titulo} en su {temporad} temporad: {episodios[0][0]}/{episodios[0][1]} episodios vistos.\n")


def pasar_temporada_letra(temporada:int) -> str:
    """
    Pasa las temporadas de numero a letra
    Args:
        temporada: La temporada en numero
    Returns:
        La temporada en letra o si no muchas despues
    """
    temporadas = {
        1: "primera",
        2: "segunda",
        3: "tercera",
        4: "cuarta",
        5: "quinta",
        6: "sexta",
        7: "séptima",
        8: "octava",
        9: "novena",
        10: "décima",
        11: "undécima",
        12: "duodécima",
        13: "decimotercera",
        14: "decimocuarta",
        15: "decimoquinta",
        16: "decimosexta"
    }
    return temporadas.get(temporada, "muchas despues")


def episodios_saber(titulo):
    """
    Muestra la cantidad de episodios vistos de un contenido específico.
    :param titulo: Título del contenido
    """
    database[1].execute(f"select coalesce(episodios_vistos,0), episodios_totales,temporada from contenido JOIN episodios ON contenido.codc = episodios.codc where titulo='{titulo}';")
    episodios = database[1].fetchall()
    for episodio in episodios:
        temporada = pasar_temporada_letra(episodio[2])
        print(f"De {titulo} en su {temporada} temporada: {episodio[0]}/{episodio[1]} episodios vistos.\n")


def anadirepisodios_vistos(titulo, ep_vistos, temporada):
    """
    Permite añadir episodios nuevos despues de haber definido la serie/anime o demás
    :param temporada: la temporada
    :param titulo: el titulo de la serie o anime
    :param ep_vistos: los episodios vistos
    """
    codigo = obtenercodigo_contenido(titulo)
    database[1].execute(
        f"update episodios set episodios_vistos='{ep_vistos}' where codc='{codigo}' and temporada={temporada}")
    database[0].commit()


def modificar_episodios_totales(titulo, ep_totales, temporada):
    codigo = obtenercodigo_contenido(titulo)
    database[1].execute(
        f"update episodios set episodios_totales='{ep_totales}' where codc='{codigo}' and temporada={temporada};")
    database[0].commit()


def visto_un_episodio(titulo, temporada):
    """
    Permite incrementar en ultimo un episodio visto
    :param temporada: la temporada de la que lo has visto
    :param titulo: el titulo de la serie/anime o lo que sea
    """
    codigo = obtenercodigo_contenido(titulo)
    database[1].execute(
        f"select episodios_vistos,episodios_totales from episodios where codc='{codigo}' and temporada={temporada}")
    lista = database[1].fetchone()
    vistos = int(lista[0]) + 1
    totales = int(lista[1])
    if vistos <= totales:  # Si los episodios vistos son menos que el total entonces podemos añadir uno más
        database[1].execute(
            f"update episodios set episodios_vistos={str(vistos)} where codc='{codigo}' and temporada={temporada}")
        database[0].commit()
    else:
        print("Si añadimos un visto más la cantidad de vistos superara al total de episodios")


def cuantos_veo_y_visto_contenido(tipo):
    database[1].execute(
        f"select count(codc) from contenido where tipo='{tipo}' and codc in (select codc from episodios where episodios_vistos<episodios_totales);")
    viendo = database[1].fetchone()
    database[1].execute(
        f"select count(codc) from contenido where select count(codc) from contenido where tipo='{tipo}' and codc in (select codc from episodios where episodios_vistos=episodios_totales);")
    visto = database[1].fetchone()
    return viendo[0], visto[0]


def mostrar_plataformas() -> dict:
    """
    Muestra las plataformas que hay disponibles y crea un diccionario con los codigos asignados a un numero
    Returns:
        Diccionario con los codigos asignados al numero
    """
    plataformas = database[1].execute("select codpl,nomg from plataformas").fetchall()
    cod_plat = dict()
    num = 0
    for plataforma in plataformas:
        num += 1
        print(f"{num}.{plataforma[1]}")
        cod_plat[num] = plataforma[0]
    return cod_plat


def obtener_plataforma_plataformas() -> str:
    """
    Obtener el codigo de una plataforma seleccionando opcion numerica
    Returns:
        El codigo de la plataforma sino devuelve nose
    """
    plataformas = mostrar_plataformas()
    op = int(input("Introduzca en numero la opcion:"))
    return plataformas.get(op, "nose")


def introducir_contenido_genero(titulo, genero):
    codigo_cont = obtenercodigo_contenido(titulo)
    codigo_gen = generar_codigo_genero(genero)
    database[1].execute(f"insert into esde values('{codigo_cont}','{codigo_gen}')")
    database[0].commit()


def insertar_temporada(titulo, temporada, ep_totales, ep_vistos, estado):
    """
    Inserta una temporada de una serie la cual no haya sido vista en su totalidad
    :param titulo: el titulo
    :param temporada: la temporada
    :param ep_totales: los episodios totales
    :param ep_vistos: los episodios ya vistos
    :param estado: el estado es decir si ya ha finalizado
    """
    codc = obtenercodigo_contenido(titulo)
    database[1].execute(f"insert into episodios values('{codc}',{temporada},{ep_totales},{ep_vistos},'{estado}');")
    database[0].commit()


def insertar_temporada_vista(titulo, temporada, ep_totales, estado):
    """
    Insertar una temporada en caso de que este vista
    Args:
        titulo: El titulo del contenido
        temporada: La temporada de la serie
        ep_totales: Los episodios totales al hacerlo para una temporada
        estado: El estado en caso de que este finalizada o no
    """
    codc = obtenercodigo_contenido(titulo)
    database[1].execute(f"insert into episodios values('{codc}',{temporada},{ep_totales},{ep_totales},'{estado}');")
    database[0].commit()

def obtener_temporadas(titulo:str)-> list:
    codc = obtenercodigo_contenido(titulo)
    database[1].execute(f"select temporada from episodios where codc='{codc}'")
    return database[1].fetchall()

def cambiar_episoidos_si_visto(temporada, episodios_totales, codc):
    """
    Cambiar si al añadir la temporada los episodios ya estan vistos
    :param temporada: la temporada
    :param episodios_totales: los episodios totales
    :param codc: el codigo de la serie
    :return:
    """
    database[1].execute(
        f"update episodios set episodios_vistos={episodios_totales} where codc='{codc}' and temporada={temporada}")
    database[0].commit()


def cambiar_visualizacion_contenido(titulo, visualizacion):
    database[1].execute(f"update contenido set visualizacion='{visualizacion}' where titulo='{titulo}'")
    database[0].commit()

def main():
    opcion_menu_1 = 0
    while opcion_menu_1 != 5:
        print("1.Introducir Datos\n2.Ver datos\n3.Eliminar Dato\n4.Actualizar dato\n5.Salir")
        opcion_menu_1 = int(input("Seleccione una opción: "))
        if opcion_menu_1 == 1:  # Añadir contenido
            print(
                "1.Contenido\n2.Plataformas\n3.Generos\n4.Contenido-Plataforma\n5.Insertar episodios contenido\n6.Insertar Contenido-Genero\n7.Añadir nueva temporada a una serie")
            opcion_anadir_datos = int(input())
            if opcion_anadir_datos == 1:  # Añadir un nuevo contenido
                titulo = input("Introduzca el titulo del contenido:")
                descripcion = input("Introduzca descripcion del contenido:")
                tipo = input("Introduzca el tipo de contenido").title()
                codc = generar_codigo_contenido(tipo)
                database[1].execute(f"insert into contenido values('{codc}','{titulo}','{descripcion}',null,'{tipo}')")
                database[0].commit()
                if tipo == "Serie" or tipo == "Anime":
                    temporada = input("Digame en numero la temporada:")
                    episodios_totales = input("Dime cuantos episodios tiene el contenido:")
                    visualizacion = input("Dime la visualizacion (si esta visto o no):")
                    estado = input("Digame el estado en el que esta la temporada(si lo sabe):")
                    database[1].execute(
                        f"insert into episodios values('{codc}',{temporada},{episodios_totales},null,'{estado}')")
                    database[0].commit()
                    if visualizacion == "si":
                        database[1].execute(f"update contenido set visualizacion='{visualizacion} where codc='{codc}'")
                        cambiar_episoidos_si_visto(temporada, episodios_totales, codc)
                    else:
                        vist = input("Ha visto algun episodio:")
                        if vist.lower() == "si":
                            ep_vistos = input("Digame cuantos episodios ha visto(en numero):")
                            anadirepisodios_vistos(titulo, ep_vistos, temporada)
                        else:
                            continue
                else:
                    visualizacion = input("Digame si esta Viendo o ha visto(tipo: Viendo,Visto):")
                    database[1].execute(f"update contenido set visualizacion='{visualizacion}' where titulo='{titulo}'")
                    continue
            elif opcion_anadir_datos == 2:  # Añadir nueva plataforma
                codpl = generar_codigo_plataforma()
                nompl = input("Introduzca el nombre de la plataforma:").title()
                url = input("Introduzca el enlace de acceso a la plataforma:")
                database[1].execute(f"insert into plataformas values('{codpl}','{nompl}','{url}')")
                database[0].commit()
            elif opcion_anadir_datos == 3:  # Añadir nuevo genero
                nombre_genero = input("Introduzca el nombre del genero:").title()
                codg = generar_codigo_genero(nombre_genero)
                database[1].execute(f"insert into generos values('{codg}','{nombre_genero}')")
                database[0].commit()
            elif opcion_anadir_datos == 4:  # Añadir contenido plataforma
                tipo = input("Digame el tipo de contenido").title()
                titulo = obtener_titulo_de_titulos(tipo)
                cod_plat = obtener_plataforma_plataformas()
                insertar_contenido_plataforma(titulo, cod_plat)
            elif opcion_anadir_datos == 6:
                tipo = input("Digame el tipo de contenido").title()
                titulo = obtener_titulo_de_titulos(tipo)
                genero = input("Introduzca el genero:").title()
                introducir_contenido_genero(titulo, genero)
            elif opcion_anadir_datos == 7:
                tipo = input("Introduzca el tipo de contenido:").title()
                titulo = obtener_titulo_de_titulos(tipo)
                temporada = input("Inserte temporada en numero:")
                ep_totales = input("Introduzca los episodios totales en numero:")
                visualizacion = input("Introduzca si lo vio completamente o no:")
                estado = input("Introduzca estado(En emision,Finalizado):")
                if visualizacion.lower() == "no":
                    ep_vistos = input("Introduzca los episodios vistos en numero:")
                    insertar_temporada(titulo, temporada, ep_totales, ep_vistos, estado)
                else:
                    insertar_temporada_vista(titulo, temporada, ep_totales, estado)



        elif opcion_menu_1 == 2:  # Ver datos
            print(
                "1.Cuantos Episodios se han visto de un contenido especifico\n2.Saber cuantos episodios se han visto de animes/series\n3.En que plataforma veo contenido\n4.Cuanto contendio estoy viendo\n5.Cuanto he visto\n6.Generos a los que pertence un contenido")
            opcion_ver_datos = int(input())
            if opcion_ver_datos == 1:
                tipo = input("Dime el tipo de contenido:").title()
                titulo = obtener_titulo_de_titulos(tipo)
                episodios_saber(titulo)
            elif opcion_ver_datos == 2:
                tipo = input("Introduce el tipo de contenido")
                obtener_episodios_tipo_contenido(tipo)
            elif opcion_ver_datos == 3:
                titulo = input("Dime el titulo del contenido:")
                saber_plataforma_veo_contenido(titulo)
            elif opcion_ver_datos == 4:
                tipo = input("Indicame el tipo de contenido:")
                viendo = cuantos_veo_y_visto_contenido(tipo)[0]
                print(f"Estoy viendo {tipo} un total de {viendo} {tipo.lower()}s")
            elif opcion_ver_datos == 6:
                tipo = input("Digame el tipo de contenido que desea ver:")
                titulo = obtener_titulo_de_titulos(tipo)
                mostrar_generos_contendio(titulo)



        elif opcion_menu_1 == 4:  # Actualizar datos
            print("1.Contenido\n2.Episodios\n3.Plataformas")
            opcion_actualizar_datos = int(input())
            if opcion_actualizar_datos == 1:  # Actualizar datos del contenido
                print("1.Añadir descripcion\n2.Añadir visualizacion Peliculas u otro")
                op_actualizar_ep = int(input())
                if op_actualizar_ep == 1:
                    tipo = input("Digame el tipo de contenido del que desea añadir una descripcion:")
                    titulo = obtener_titulo_de_titulos(tipo)
                    descripcion = input("Introduce la descripcion a añadir")
                    anadir_descripcion(titulo, descripcion)
                elif op_actualizar_ep == 2:
                    tipo = input("Digame el tipo de contenido del que desea añadir una descripcion:")
                    titulo = obtener_titulo_de_titulos(tipo)
                    visualizacion = input("Introduzca la visualizacion:")
                    cambiar_visualizacion_contenido(titulo, visualizacion)

            elif opcion_actualizar_datos == 2:  # Actualizar datos de los episodios
                print("1.Episodios Vistos\n2.Episodios totales\n3.Visto un episodio")
                op_actualizar_ep = int(input())
                if op_actualizar_ep == 1:
                    tipo = input("Indiqueme el tipo de contenido:")
                    titulo = obtener_titulo_de_titulos(tipo)
                    ep_vistos = input("Introduzca en numero los episodios vistos:")
                    temporada = input("Digame en numero la temporada:")
                    anadirepisodios_vistos(titulo, ep_vistos, temporada)  # Añadimos nueva cantidad de episodios vistos
                elif op_actualizar_ep == 2:
                    titulo = input("Introduzca el titulo del anime/serie:")
                    ep_totales = input("Introduzca en numero los episodios vistos:")
                    temporada = input("Digame en numero la temporada:")
                    modificar_episodios_totales(titulo, ep_totales, temporada)  # Modificamos los episodios totales
                elif op_actualizar_ep == 3:
                    tipo = input("Digame el tipo de contenido:").title()
                    titulo = obtener_titulo_de_titulos(tipo)
                    temporada = input("Digame en numero la temporada:")
                    visto_un_episodio(titulo, temporada)  # Registra que de esa temporada se ha visto un episodio


if __name__ == '__main__':
    main()  # Ejecutamos la funcion principal
    cerrar_conexion(database)  # Cerramos la conexion con la base de datos pasandole la base de datos
