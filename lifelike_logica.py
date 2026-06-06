# Autómata Life-Like - Lógica
# Sergio Aarón Cambronero Fonseca
# Taller de Programación - Prof. Mauricio Avilés

import random


# Función: generar_matriz_aleatoria
# Crea una matriz con valores 0 o 1 de forma aleatoria
# Entradas: filas, columnas 
# Salidas: matriz
# Restricciones: filas y columnas deben ser positivos
def generar_matriz_aleatoria(filas, columnas):
    matriz = [
        [random.randint(0, 1) for _ in range(columnas)]
        for _ in range(filas)
    ]
    return matriz


# Función: generar_matriz_vacia
# Crea una matriz con todos los valores en cero
# Entradas: filas, columnas 
# Salidas: matriz 
# Restricciones: filas y columnas deben ser positivos
def generar_matriz_vacia(filas, columnas):
    matriz = [
        [0 for _ in range(columnas)]
        for _ in range(filas)
    ]
    return matriz


# Función: obtener_vecinos
# Retorna los estados de las 8 células vecinas (vecindario de Moore)
# Usa bordes toroidales: los bordes se conectan entre sí
# Entradas: matriz, fila, col
# Salidas: vecinos con los 8 estados vecinos
# Restricciones: fila y col deben estar dentro de los límites
def obtener_vecinos(matriz, fila, col):
    num_filas = len(matriz)
    num_cols = len(matriz[0])
    vecinos = []

    for df in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if df == 0 and dc == 0:
                continue
            vecino_fila = (fila + df) % num_filas
            vecino_col = (col + dc) % num_cols
            vecinos.append(matriz[vecino_fila][vecino_col])

    return vecinos


# Función: transicion_celula
# Determina el nuevo estado de una célula según las reglas Bx/Sy
# Entradas: estado, vecinos, nacimiento, supervivencia
# Salidas: nuevo_estado
# Restricciones: estado debe ser 0 o 1; vecinos debe tener 8 elementos
def transicion_celula(estado, vecinos, nacimiento, supervivencia):
    vivos = sum(vecinos)

    if estado == 0:
        if vivos in nacimiento:
            return 1
        else:
            return 0
    else:
        if vivos in supervivencia:
            return 1
        else:
            return 0


# Función: transicion
# Aplica las reglas a toda la matriz y retorna el nuevo estado
# Entradas: matriz, nacimiento, supervivencia
# Salidas: nueva_matriz
# Restricciones: la matriz debe ser rectangular
def transicion(matriz, nacimiento, supervivencia):
    filas = len(matriz)
    columnas = len(matriz[0])
    nueva_matriz = generar_matriz_vacia(filas, columnas)

    for f in range(filas):
        for c in range(columnas):
            estado_actual = matriz[f][c]
            vecinos = obtener_vecinos(matriz, f, c)
            nuevo_estado = transicion_celula(estado_actual, vecinos, nacimiento, supervivencia)
            nueva_matriz[f][c] = nuevo_estado

    return nueva_matriz


# Función: parsear_reglas
# Convierte una cadena "Bx/Sy" a listas de números
# Ejemplo: "B3/S23" -> nacimiento=[3], supervivencia=[2,3]
# Entradas: regla_str
# Salidas: tupla
# Restricciones: formato debe ser Bx/Sy con dígitos del 0 al 8
def parsear_reglas(regla_str):
    regla_str = regla_str.upper().strip()
    partes = regla_str.split("/")
    nacimiento = [int(d) for d in partes[0][1:]]
    supervivencia = [int(d) for d in partes[1][1:]]
    return nacimiento, supervivencia
