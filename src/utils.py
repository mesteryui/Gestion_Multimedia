def generar_numero_nuevo_codigo(lista, letra:str) -> int:
    """
    Obtener el numero del codigo para un nuevo elemento, por ejemplo contenido, plataformas
    Args:
        lista: le pasamos la lista de codigos ya existentes
        letra: los caracteres que hay por en medio en estos codigos

    Returns:
        El numero mayor mas 1, asumiendo que el mayor si no hay nada en la lista es 0
    """
    numero_codigo = 0
    for elemento in lista:
        numero = int(elemento[0].replace(letra,""))
        if numero>numero_codigo:
            numero_codigo = numero
    return numero_codigo+1

def generar_codigo_genero(nomg) -> str:
    return nomg[0:2].upper()  # Devolvemos las dos primeras letras del genero en mayusculas

if __name__ == '__main__':
    lista = [["a5"],["a1"],["a10"],["a3"],["a4"]]
    print(generar_numero_nuevo_codigo(lista,"a"))