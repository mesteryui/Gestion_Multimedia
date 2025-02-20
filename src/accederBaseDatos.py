import psycopg
import xml.etree.ElementTree as ET

def leerXML():
    tree = ET.parse('archivo.xml')
    root = tree.getroot()
    return root

def conectar_base():
    """
    Conectarse a la base de datos
    Returns:
        La conexion a la base de datos, el cursor para poder hacer consultas y por si acaso el cursor de cliente
    """
    credenciales = leerXML()
    try:
        connection = psycopg.connect(database = "audiovisual",
                        user = credenciales.find("user"),
                        host= 'localhost',
                        password = credenciales.find("password"),
                        port = 5432)
        cursor = connection.cursor()
        return connection,cursor
    except sqlite3.OperationalError:
        return "La base de datos no fue abierta correctamente"


def cerrar_conexion(datab):
    conex = datab[0]
    conex.close()
