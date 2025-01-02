import os.path
import sqlite3
from pathlib import Path


def crear_base_datos():
    base = Path(os.getcwd()).parent.joinpath("main.db")
    tablas = str(Path(os.getcwd()).parent.joinpath("Crear_tablas.sql"))
    if not os.path.exists(base):
        base_datos = conectar_base()
        with open(base,"w") as archivo:
            archivo.write("")
            base_datos[1].execute("PRAGMA foreign_keys = ON;")
            base_datos[1].execute(f".read {tablas}")
            base_datos[0].commit()

def conectar_base():
    """
    Conectarse a la base de datos
    Returns:
        La conexion a la base de datos, el cursor para poder hacer consultas y por si acaso el cursor de cliente
    """
    crear_base_datos()
    try:
        conexion = sqlite3.connect(Path(os.getcwd()).parent.joinpath("main.db"))
        cursor = conexion.cursor()
        return conexion,cursor
    except sqlite3.OperationalError:
        return "La base de datos no fue abierta correctamente"


def cerrar_conexion(datab):
    conex = datab[0]
    curs = datab[1]
    conex.close(), curs.close()
