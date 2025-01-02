import sqlite3
from pathlib import Path


def conectar_base():
    """
    Conectarse a la base de datos
    Returns:
        La conexion a la base de datos, el cursor para poder hacer consultas y por si acaso el cursor de cliente
    """
    try:
        connection = sqlite3.connect(Path.cwd().parent.joinpath("main.db"))
        cursor = connection.cursor()
        return connection,cursor
    except sqlite3.OperationalError:
        return "La base de datos no fue abierta correctamente"


def cerrar_conexion(datab):
    conex = datab[0]
    curs = datab[1]
    conex.close(),curs.close()
