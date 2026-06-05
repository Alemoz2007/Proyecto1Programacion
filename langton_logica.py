from random import randint


def generar_matriz(filas, columnas):
    """Genera una matriz vacía.
    Entradas y restricciones:
    -filas (int)
    -columnas (int)
    Salida: Matriz llena de ceros."""
    return [[0 for c in range(columnas)]
            for f in range(filas)]


def generar_matriz_aleatoria(filas, columnas, estados):
    """Genera una matriz con estados aleatorios.
    Entradas y restricciones:
    -filas (int)
    -columnas (int)
    -estados (int)
    Salida: Matriz aleatoria."""
    return [[randint(0, estados - 1) for c in range(columnas)] for f in range(filas)]

def generar_colores(cantidad):
    """Genera una lista de colores aleatorios.
    Entrada y restricciones:
    -cantidad (int)
    Salida: lista de tuplas RGB."""
    colores = [(0, 0, 0)]
    for i in range(cantidad - 1):
        colores.append((randint(0, 255), randint(0, 255), randint(0, 255)))
    return colores


def crear_hormiga(filas, columnas):
    """Crea una hormiga en el centro del tablero.
    Entrada y restricciones:
    -filas (int)
    -columnas (int)
    Salida: La hormiga"""
    return {"fila": filas // 2, "columna": columnas // 2, "direccion": 0}


def girar_hormiga(direccion, giro):
    """Gira la hormiga.
    Entrada y restricciones:
    -direccion (int)
    -giro (str)
    Salida: Cambio de dirrecion"""
    if giro == "R":
        return (direccion + 1) % 4
    return (direccion - 1) % 4


def avanzar_hormiga(hormiga, filas, columnas):
    """Avanza una posición la hormiga.
    Entrada y restrcciones:
    -hormiga (dict)
    -filas (int)
    -columnas (int)
    Salida: Ninguna"""
    if hormiga["direccion"] == 0:
        hormiga["fila"] -= 1
    elif hormiga["direccion"] == 1:
        hormiga["columna"] += 1
    elif hormiga["direccion"] == 2:
        hormiga["fila"] += 1
    else:
        hormiga["columna"] -= 1
    hormiga["fila"] %= filas
    hormiga["columna"] %= columnas


def siguiente(M, hormiga, regla):
    """Ejecuta una transición de la hormiga.
    Entradas:
    -M (list)
    -hormiga (dict)
    -regla (str)
    Salida: Ninguna"""
    fila = hormiga["fila"]
    columna = hormiga["columna"]
    estado_actual = M[fila][columna]
    giro = regla[estado_actual]
    hormiga["direccion"] = girar_hormiga(hormiga["direccion"],giro)
    M[fila][columna] = (estado_actual + 1) % len(regla)
    avanzar_hormiga(hormiga,len(M),len(M[0]))
