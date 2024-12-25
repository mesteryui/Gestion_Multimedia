# Gestion contenido audiovisual

>[!WARNING]
>Informo he tenido unos problemas a la hora de gestionar lo relacionado a la cuenta de Github
>debido a eso aparece una cuenta que tengo por los estudios
>Informo que las dos cuentas corresponden a mi

Aviso que las pruebas la estoy haciendo con la base de datos que ya tengo y que además hay algunas cosas que no he corregido
debido a eso el programa puede no estar adaptado al script que estoy creando

## Tecnologias utilizadas:
- [PostgreSQL](https://www.postgresql.org/): Sistema de base de datos utilizado
- [Python](https://www.python.org/): Lenguaje de programacion utilizado
- [psycopg](https://pypi.org/project/psycopg/): Sistema para conectar la base de datos con el programa y hacer operaciones

## Credenciales
Las credenciales se almacenan en un XML llamado `credentials.xml` con la siguiente estructura:
```xml
<credentials>
    <user>nombre_usuario</user>
    <host>localhost</host>
    <password>contraseña</password>
    <database>nombre_base_datos</database>
</credentials>
```