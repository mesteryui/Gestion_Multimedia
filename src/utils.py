def generar_numero_nuevo_codigo(lista, letra):
    numero_codigo = 1
    for elemento in lista:
        numero = int(elemento[0].replace(letra,""))
        if numero>numero_codigo:
            numero_codigo = numero
    return numero_codigo+1

if __name__ == '__main__':
    lista = [["a5"],["a1"],["a10"],["a3"],["a4"]]
    print(generar_numero_nuevo_codigo(lista,"a"))