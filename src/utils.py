def generar_numero_nuevo_codigo(lista, letra):
    numero_codigo = 1
    for list in lista:
        numero = int(list.replace(letra,""))
        if numero>numero_codigo:
            numero_codigo = numero