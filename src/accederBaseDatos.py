import psycopg2
import xml.etree.ElementTree as ET

def obtener_raiz():
    arbol = ET.parse("credentials.xml")
    return arbol.getroot()

def conectar_base():
    raiz = obtener_raiz()
    try:
        conexion = psycopg2.connect(
            host=raiz.find("host").text,
            database=raiz.find("database").text,
            user=raiz.find("user").text,
            password=raiz.find("password").text
        )
        cursor = conexion.cursor()
        return conexion,cursor
    except psycopg2.Error as e:
        print("Error al insertar datos:", e)
        return e

def cerrar_conexion(datab):
    conex = datab[0]
    curs = datab[1]
    if conex:
        return conex.close(),curs.close()
