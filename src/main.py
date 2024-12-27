from accederBaseDatos import *

database = conectar_base()  # Obtenemos la conexion a la base de datos y un cursor el cual sera util en todas las funciones que hagamos


def mostrar_contenido(tipo):
    """
    Pasandole el tipo de contenido nos muestra tod-o lo que hay de ese contenido
    :param tipo: el tipo de contenido
    :return: los contenidos
    """
    contenidos = database[1].execute(
        f"select titulo from contenido where tipo='{tipo}';").fetchall()  # Guardamos esos contenidos
    num = 0
    diccionario_titulos = dict()  # Definimos un diccionario donde se guardaran los numeros
    for contenido in contenidos:
        num += 1
        diccionario_titulos[num] = contenido[0]
        print(f"{num}.{contenido[0]}")

    return diccionario_titulos


def obtener_titulo_de_titulos(tipo):
    """
    Obtiene el titulo que le indiquemos aprovechando la funcion mostrar_contenido
    :param tipo: el tipo de contenido lo necesitamos para la funcion mostrar_contenido
    :return: el titulo si tod salio bien si no vuelve a iniciar la funcion main
    """
    titulos = mostrar_contenido(tipo)
    opcion = int(input("Introduzca una opcion en numero:"))
    titulo = titulos.get(opcion, "nose")
    if titulo == "nose":
        print("Lo siento esa opcion no es valida")
        main()
    else:
        return titulo


def anadir_descripcion(titulo, descripcion):
    """
    Añadir descripcion al contenido
    :param titulo: el titulo del contenido
    :param descripcion: la descipcion a añadir
    """
    database[2].execute(f"update contenido set descripcion='{descripcion}' where titulo='{titulo}';")
    database[0].commit()


def generar_codigo_contenido(tipo):
    """
    Pasando el tipo de contenido a añadir creamos el numero que se le añade al codigo
    :param tipo: el tipo de contenido a añadir
    :return: (numero ultimo codc)+1 o 1 si no existen codigos con la letra para ese tipo definido
    """
    database[1].execute(
        f"select codc from contenido where tipo='{tipo}'")  # Ejecutamos la consulta para obtener los codigos
    letra = tipo[0].lower()  # Obtenemos la letra del tipo sacando el primer elemento como minuscula
    lista = database[1].fetchall()  # Obtenemos todos los codigos
    if not lista:  # Si la lista esta vacia
        return 1  # Devolvemos el primer numero por el que empiezan los codigos
    else:  # En caso contrario es decir que la lista contenga algo
        lista_ordenada = sorted(lista, key=lambda x: int(
            x[0][1:]))  # Ordenamos los valores de la lista por numeros de menor a mayor
        resultado = lista_ordenada[len(lista_ordenada) - 1][
            0]  # Obtenemos el ultimo indice de la lista pero como es bidimensional el dato estara siempre en el primer indice
        resultado = resultado.replace(letra, "")  # Quitamos la letra
        return int(resultado) + 1  # Devolvemos el resultado mas uno como numero


def generar_codigo_plataforma():
    """
    Generar el codigo numerico para plataformas
    :return: el codigo numerico
    """
    database[1].execute("select codpl from plataformas;")  # Obtener los codigos de las plataformas
    lista = database[1].fetchall()  # Guardarlos en una lista
    if not lista:
        return "pl1"
    else:
        lista_ordenada = sorted(lista, key=lambda x: int(x[0][2:]))  # Ordenar esa lista de menor a mayor numero
        resultado = lista_ordenada[len(lista_ordenada) - 1][0]  # Acceder al ultimo elemento de la lista
        resultado = int(resultado.replace("pl", ""))+1  # Quitarle los dos primeros caracters
        return  "pl" + str(resultado) # Devolver el resultado de eso más 1 como entero


def generar_codigo_genero(nomg):
    return nomg[0].capitalize()


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
    database[1].execute(
        f"select titulo,coalesce(episodios_vistos,0),episodios_totales from contenido,episodios where episodios.codc=contenido.codc and tipo='{tipo}'")
    datos = database[1].fetchall()
    articul = "De las" if tipo == "Serie" else "De los"
    articul2 = "Del" if tipo == "Anime" else "De la"
    print(f"{articul} {tipo.lower()}s se tiene la siguiente informacion:\n")
    for dato in datos:
        print(f"{articul2} {tipo.lower()} {dato[0]} se han visto {dato[1]} de {dato[2]} episodios\n")


def insertar_contenido_plataforma(titulo, nombreplataforma):
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
    for plataforma in plataformas:
        tipo = plataforma[2]
        tipo = tipo.lower()
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


def pasar_temporada_letra(temporada):
    """
    Pasa las temporadas a un formato letra tipo primera temporada y demás
    :param temporada: la temporada en numero
    :return: la temporada en letra
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
    episodios =  database[1].execute(
        f"select coalesce(episodios_vistos,0), episodios_totales,temporada from contenido JOIN episodios ON contenido.codc = episodios.codc where titulo='{titulo}';").fetchall()

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

    viendo =  database[1].execute(
        f"select count(codc) from contenido where tipo='{tipo}' and codc in (select codc from episodios where episodios_vistos<episodios_totales);").fetchone()
    database[1].execute(
        f"select count(codc) from contenido where select count(codc) from contenido where tipo='{tipo}' and codc in (select codc from episodios where episodios_vistos=episodios_totales);")
    visto = database[1].fetchone()
    return viendo[0], visto[0]


def introducir_contenido_genero(titulo, genero):
    codigo_cont = obtenercodigo_contenido(titulo)
    codigo_gen = generar_codigo_genero(genero)
    database[1].execute(f"insert into esde values('{codigo_cont}','{codigo_gen}')")
    database[0].commit()


def insertar_temporada(titulo, temporada, ep_totales, ep_vistos, estado):
    codc = obtenercodigo_contenido(titulo)
    database[1].execute(f"insert into episodios values('{codc}',{temporada},{ep_totales},{ep_vistos},'{estado}');")
    database[0].commit()


def insertar_temporada_vista(titulo, temporada, ep_totales, estado):
    codc = obtenercodigo_contenido(titulo)
    database[1].execute(f"insert into episodios values('{codc}',{temporada},{ep_totales},{ep_totales},'{estado}');")
    database[0].commit()


def cambiar_episoidos_si_visto(temporada, episodios_totales, codc):
    database[1].execute(
        f"update episodios set episodios_vistos={episodios_totales} where codc='{codc}' and temporada={temporada}")
    database[0].commit()


def main():
    op1 = 0
    while op1 != 5:
        print("1.Introducir Datos\n2.Ver datos\n3.Eliminar Dato\n4.Actualizar dato\n5.Salir")
        op1 = int(input("Seleccione una opción: "))
        if op1 == 1:
            print(
                "1.Contenido\n2.Plataformas\n3.Generos\n4.Contenido-Plataforma\n5.Insertar episodios contenido\n6.Insertar Contenido-Genero\n7.Añadir nueva temporada a una serie")
            op2 = int(input())
            if op2 == 1:
                titulo = input("Introduzca el titulo del contenido:")
                descripcion = input("Introduzca descripcion del contenido:")
                tipo = input("Introduzca el tipo de contenido").title()
                cod = tipo[0].lower()
                num = generar_codigo_contenido(tipo)
                codc = cod + str(num)
                database[1].execute(f"insert into contenido values('{codc}','{titulo}','{descripcion}',null,'{tipo}')")
                database[0].commit()
                if tipo == "Serie" or tipo == "Anime":
                    temporada = input("Digame en numero la temporada:")
                    episodios_totales = input("Dime cuantos episodios tiene el contenido:")
                    visualizacion = input("Dime la visualizacion (si esta visto o no):")
                    database[1].execute(
                        f"insert into episodios values('{codc}',{temporada},'{episodios_totales}',null)")
                    database[0].commit()
                    if visualizacion == "si":
                        cambiar_episoidos_si_visto(temporada, episodios_totales, codc)

                else:
                    continue
            elif op2 == 2:
                codpl = generar_codigo_plataforma()
                nompl = input("Introduzca el nombre de la plataforma:").title()
                url = input("Introduzca el enlace de acceso a la plataforma:")
                database[1].execute(f"insert into plataformas values('{codpl}','{nompl}','{url}')")
                database[0].commit()
            elif op2 == 3:
                nombre_genero = input("Introduzca el nombre del genero:").title()
                codg = generar_codigo_genero(nombre_genero)
                database[2].execute(f"insert into generos values('{codg}','{nombre_genero}')")
                database[0].commit()
            elif op2 == 4:
                titulo = input("Introduzca el titulo de la serie:")
                nombre_plat = input("Introduzca el nombre de la plataforma")
                insertar_contenido_plataforma(titulo, nombre_plat)

            elif op2 == 6:
                titulo = input("Introduzca el titulo:")
                genero = input("Introduzca el genero:").title()
                introducir_contenido_genero(titulo, genero)
            elif op2 == 7:
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



        elif op1 == 2:
            print(
                "1.Cuantos Episodios se han visto de un contenido especifico\n2.Saber cuantos episodios se han visto de animes/series\n3.En que plataforma veo contenido\n4.Cuanto contendio estoy viendo\n5.Cuanto he visto")
            op2 = int(input())
            if op2 == 1:
                tipo = input("Dime el tipo de contenido:").title()
                titulo = obtener_titulo_de_titulos(tipo)
                episodios_saber(titulo)
            elif op2 == 2:
                tipo = input("Introduce el tipo de contenido")
                obtener_episodios_tipo_contenido(tipo)
            elif op2 == 3:
                titulo = input("Dime el titulo del contenido:")
                saber_plataforma_veo_contenido(titulo)
            elif op2 == 4:
                tipo = input("Indicame el tipo de contenido:")
                viendo = cuantos_veo_y_visto_contenido(tipo)[0]
                print(f"Estoy viendo {tipo} un total de {viendo} {tipo.lower()}s")


        elif op1 == 4:
            print("1.Contenido\n2.Episodios\n3.Plataformas")
            op8 = int(input())
            if op8 == 1:
                print("1.Añadir descripcion")
                op9 = int(input())
                if op9 == 1:
                    tipo = input("Digame el tipo de contenido del que desea añadir una descripcion:")
                    titulo = obtener_titulo_de_titulos(tipo)
                    descripcion = input("Introduce la descripcion a añadir")
                    anadir_descripcion(titulo, descripcion)

            elif op8 == 2:
                print("1.Episodios Vistos\n2.Episodios totales\n3.Visto un episodio")
                op9 = int(input())
                if op9 == 1:
                    titulo = input("Introduzca el titulo del anime/serie:")
                    ep_vistos = input("Introduzca en numero los episodios vistos:")
                    temporada = input("Digame en numero la temporada:")
                    anadirepisodios_vistos(titulo, ep_vistos, temporada)
                elif op9 == 2:
                    titulo = input("Introduzca el titulo del anime/serie:")
                    ep_totales = input("Introduzca en numero los episodios vistos:")
                    temporada = input("Digame en numero la temporada:")
                    modificar_episodios_totales(titulo, ep_totales, temporada)
                elif op9 == 3:
                    tipo = input("Digame el tipo de contenido:").title()
                    titulo = obtener_titulo_de_titulos(tipo)
                    temporada = input("Digame en numero la temporada:")
                    visto_un_episodio(titulo, temporada)


if __name__ == '__main__':
    main()  # Ejecutamos la funcion principal
    cerrar_conexion(database)  # Cerramos la conexion con la base de datos pasandole la base de datos
