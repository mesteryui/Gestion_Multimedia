def generar_numero_nuevo_codigo(lista, letra:str) -> int:
    """
    Obtener el numero del codigo para un nuevo elemento, por ejemplo contenido, plataformas
    Args:
        lista: le pasamos la lista de codigos ya existentes
        letra: los caracteres que hay por en medio en estos codigos

    Returns:
        El numero mayor mas 1, asumiendo que el mayor si no hay nada en la lista es 0
    """
    numero_codigo = 0 # Asumimos que el numero mayor es 0 de esta manera al devolver el numero siempre dara como queremos
    for elemento in lista:
        numero = int(elemento[0].replace(letra,"")) # Obtenemos el numero del codigo casteando como entero el resultado de quitar las letras
        if numero>numero_codigo: # Comprobamos si el numero es mayor al numero del codigo
            numero_codigo = numero # Reasignamos a numero si se cumple si no no hacemos nada
    return numero_codigo+1 # Devolvemos el numero_codigo + 1

def generar_codigo_genero(nomg) -> str:
    return nomg[0:2].upper()  # Devolvemos las dos primeras letras del genero en mayusculas

if __name__ == '__main__':
    lis = [["a5"], ["a1"], ["a10"], ["a3"], ["a4"]]
    print(generar_numero_nuevo_codigo(lis, "a"))