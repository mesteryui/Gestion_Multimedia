import psycopg
from psycopg import sql
import xml.etree.ElementTree as ET
from pathlib import Path
def leerXML():
    tree = ET.parse(Path.cwd().parent.joinpath("credentials.xml"))
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
        connection = psycopg.connect(database = "postgres",
                        user = credenciales.find("user"),
                        host= 'localhost',
                        password = credenciales.find("password"),
                        port = 5432)
        db_name = "audiovisual"
        cursor = connection.cursor()
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (db_name,))
        exists = cursor.fetchone()
        if not exists:
            # Crear la base de datos
            cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name)))

        return connection,cursor
    except psycopg.Error:
        return "La base de datos no fue abierta correctamente"


def cerrar_conexion(datab):
    conex = datab[0]
    conex.close()
