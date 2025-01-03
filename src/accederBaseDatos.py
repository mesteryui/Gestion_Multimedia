from xml.etree.ElementTree import ElementTree

import psycopg
import xml.etree.ElementTree as ET


def obtener_raiz() -> ElementTree:
    arbol = ET.parse("credentials.xml")
    return arbol.getroot()


def conectar_base():
    """
    Conectarse a la base de datos
    Returns:
        La conexion a la base de datos, el cursor para poder hacer consultas y por si acaso el cursor de cliente
    """
    raiz = obtener_raiz()
    try:
        conexion = psycopg.connect(
            host=raiz.find("host").text,
            dbname=raiz.find("database").text,
            user=raiz.find("user").text,
            password=raiz.find("password").text
        )
        client_cursor = psycopg.ClientCursor(conexion)
        cursor = conexion.cursor()
        return conexion, cursor, client_cursor
    except psycopg.Error as e:
        print("Error al insertar datos:", e)
        return e


def cerrar_conexion(datab):
    conex = datab[0]
    curs = datab[1]
    conex.close(), curs.close()
