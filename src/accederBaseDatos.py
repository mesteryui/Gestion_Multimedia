import psycopg
from psycopg import sql
from pathlib import Path
import sys
import xml.etree.ElementTree as ET

def leerXML():
    tree = ET.parse(Path.cwd().parent.joinpath("credentials.xml"))
    root = tree.getroot()
    return root


def conectar_base():
    """
    Conecta a la base de datos PostgreSQL y asegura la existencia de la base de datos y tablas.

    Returns:
        tuple: (conexión, cursor) o None en caso de error
    """
    credenciales = leerXML()

    try:
        # 1. Conexión inicial a postgres para verificar/crear la base de datos
        with psycopg.connect(
                dbname="postgres",
                user=credenciales.find("user").text,
                password=credenciales.find("password").text,
                host="localhost",
                port=5432
        ) as conn_postgres, conn_postgres.cursor() as cursor_postgres:

            db_name = "audiovisual"

            # Verificar si la base de datos existe
            cursor_postgres.execute(
                "SELECT 1 FROM pg_database WHERE datname = %s",
                (db_name,)
            )

            if not cursor_postgres.fetchone():
                cursor_postgres.execute(
                    sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name))
                )

        # 2. Conexión a la base de datos objetivo
        connection = psycopg.connect(
            dbname=db_name,
            user=credenciales.find("user").text,
            password=credenciales.find("password").text,
            host="localhost",
            port=5432
        )

        with connection.cursor() as cursor:
            # Verificar si existen tablas
            cursor.execute("""
                SELECT EXISTS (
                    SELECT 1 
                    FROM information_schema.tables 
                    WHERE table_schema = 'public'
                )
            """)

            # Si no hay tablas, ejecutar script SQL
            if not cursor.fetchone()[0]:
                sql_path = Path(__file__).parent.parent / "Crear_tablas.sql"

                with open(sql_path, "r") as f:
                    sql_script = f.read()

                # Ejecutar en una transacción
                with connection.transaction():
                    cursor.execute(sql_script)
                    cursor.commit()

                print("Tablas creadas exitosamente")

        return connection, connection.cursor()

    except Exception as e:
        print(f"Error de conexión: {e}", file=sys.stderr)
        return None


def cerrar_conexion(conexion):
    """Cierra la conexión a la base de datos"""
    if conexion and not conexion.closed:
        conexion.close()
        print("Conexión cerrada")
