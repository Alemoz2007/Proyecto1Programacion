# Autómata Life-Like - GUI
# Sergio Aarón Cambronero Fonseca
# Taller de Programación - Prof. Mauricio Avilés

import pygame
import pickle
import easygui
import lifelike_logica as ll

COLOR_FONDO = (0, 0, 0)
COLOR_VIVA = (0, 255, 200)
COLOR_GRID = (30, 30, 30)
TITULO_VENTANA = "Autómata Life-Like"
FPS = 10


# Función: dibujar_matriz
# Dibuja el estado de la matriz en la ventana de pygame
# Entradas: ventana (pygame.Surface), matriz, tam_celda
# Salidas: ninguna
# Restricciones: tam_celda debe ser positivo
def dibujar_matriz(ventana, matriz, tam_celda):
    filas = len(matriz)
    columnas = len(matriz[0])

    for f in range(filas):
        for c in range(columnas):
            x = c * tam_celda
            y = f * tam_celda

            if matriz[f][c] == 1:
                color = COLOR_VIVA
            else:
                color = COLOR_FONDO

            # Primero se dibuja el fondo de la celda en gris (el grid)
            pygame.draw.rect(ventana, COLOR_GRID, (x, y, tam_celda, tam_celda))
            # Luego el relleno de color con 1px de margen, para que el grid se vea
            pygame.draw.rect(ventana, color, (x + 1, y + 1, tam_celda - 1, tam_celda - 1))


# Función: guardar_estado
# Guarda el estado completo del autómata en un archivo pickle
# Entradas: matriz, filas, columnas, tam_celda, nacimiento, supervivencia
# Salidas: ninguna
# Restricciones: el usuario debe tener permisos de escritura
def guardar_estado(matriz, filas, columnas, tam_celda, nacimiento, supervivencia):
    ruta = easygui.filesavebox(
        msg="Guardar estado del autómata",
        title="Guardar",
        default="estado_lifelike.pkl",
        filetypes=["*.pkl"]
    )

    if ruta is None:
        print("Guardado cancelado.")
        return

    datos = {
        "matriz": matriz,
        "filas": filas,
        "columnas": columnas,
        "tam_celda": tam_celda,
        "nacimiento": nacimiento,
        "supervivencia": supervivencia
    }

    with open(ruta, "wb") as archivo:
        pickle.dump(datos, archivo)

    print(f"Estado guardado en: {ruta}")


# Función: cargar_estado
# Carga el estado del autómata desde un archivo pickle
# Entradas: ninguna
# Salidas: tupla con (matriz, filas, columnas, tam_celda, nacimiento, supervivencia) o None si el usuario cancela
# Restricciones: el archivo debe haber sido guardado con guardar_estado
def cargar_estado():
    ruta = easygui.fileopenbox(
        msg="Cargar estado del autómata",
        title="Cargar",
        filetypes=["*.pkl"]
    )

    if ruta is None:
        print("Carga cancelada.")
        return None

    with open(ruta, "rb") as archivo:
        datos = pickle.load(archivo)

    print(f"Estado cargado desde: {ruta}")
    return (
        datos["matriz"],
        datos["filas"],
        datos["columnas"],
        datos["tam_celda"],
        datos["nacimiento"],
        datos["supervivencia"]
    )


# Función: solicitar_parametros
# Muestra diálogos para pedir los parámetros iniciales al usuario
# Entradas: ninguna
# Salidas: tupla (filas, columnas, tam_celda, nacimiento, supervivencia)
# Restricciones: el usuario debe ingresar valores válidos
def solicitar_parametros():
    filas_str = easygui.enterbox(
        msg="¿Cuántas filas debe tener la cuadrícula?",
        title="Parámetros - Life-Like",
        default="50"
    )
    filas = int(filas_str) if filas_str else 50

    columnas_str = easygui.enterbox(
        msg="¿Cuántas columnas debe tener la cuadrícula?",
        title="Parámetros - Life-Like",
        default="80"
    )
    columnas = int(columnas_str) if columnas_str else 80

    tam_str = easygui.enterbox(
        msg="¿Cuál es el tamaño (en píxeles) de cada célula?",
        title="Parámetros - Life-Like",
        default="10"
    )
    tam_celda = int(tam_str) if tam_str else 10

    regla_str = easygui.enterbox(
        msg=(
            "Ingrese las reglas en formato Bx/Sy\n\n"
            "Ejemplos:\n"
            "  B3/S23        -> Juego de la Vida de Conway\n"
            "  B3/S012345678 -> Life Without Death\n"
            "  B1357/S1357   -> Replicator\n"
            "  B35678/S5678  -> Diamoeba\n"
            "  B34/S34       -> 34 Life\n"
            "  B4678/S35678  -> Anneal"
        ),
        title="Parámetros - Life-Like",
        default="B3/S23"
    )
    if not regla_str:
        regla_str = "B3/S23"

    nacimiento, supervivencia = ll.parsear_reglas(regla_str)
    return filas, columnas, tam_celda, nacimiento, supervivencia


# Función: main
# Bucle principal del programa: eventos, actualización y dibujo
# Entradas: ninguna
# Salidas: ninguna
# Restricciones: ninguna
def main():
    pygame.init()

    filas, columnas, tam_celda, nacimiento, supervivencia = solicitar_parametros()

    ancho_ventana = columnas * tam_celda
    alto_ventana = filas * tam_celda

    ventana = pygame.display.set_mode((ancho_ventana, alto_ventana))
    pygame.display.set_caption(TITULO_VENTANA)

    matriz = ll.generar_matriz_aleatoria(filas, columnas)
    reloj = pygame.time.Clock()
    corriendo = True
    activo = True

    while activo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                activo = False

            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    corriendo = not corriendo
                    print("Simulación", "corriendo." if corriendo else "pausada.")

                elif evento.key == pygame.K_r:
                    matriz = ll.generar_matriz_aleatoria(filas, columnas)
                    print("Matriz reiniciada (aleatoria).")

                elif evento.key == pygame.K_b:
                    matriz = ll.generar_matriz_vacia(filas, columnas)
                    print("Matriz reiniciada (vacía).")

                elif evento.key == pygame.K_g:
                    guardar_estado(matriz, filas, columnas, tam_celda, nacimiento, supervivencia)

                elif evento.key == pygame.K_c:
                    resultado = cargar_estado()
                    if resultado is not None:
                        matriz, filas, columnas, tam_celda, nacimiento, supervivencia = resultado
                        ancho_ventana = columnas * tam_celda
                        alto_ventana = filas * tam_celda
                        ventana = pygame.display.set_mode((ancho_ventana, alto_ventana))

            elif evento.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                col_click = mouse_x // tam_celda
                fila_click = mouse_y // tam_celda

                if 0 <= fila_click < filas and 0 <= col_click < columnas:
                    estado_actual = matriz[fila_click][col_click]
                    matriz[fila_click][col_click] = (estado_actual + 1) % 2
                    print(f"Célula ({fila_click}, {col_click}) -> {matriz[fila_click][col_click]}")

        if corriendo:
            matriz = ll.transicion(matriz, nacimiento, supervivencia)

        ventana.fill(COLOR_FONDO)
        dibujar_matriz(ventana, matriz, tam_celda)
        pygame.display.flip()
        reloj.tick(FPS)

    pygame.quit()
    print("Life-Like cerrado.")


# Función: iniciar
# Punto de entrada del módulo, llamable desde main.py
# Entradas: ninguna
# Salidas: ninguna
# Restricciones: ninguna
def iniciar():
    print("Iniciando Life-Like...")
    print("Controles: ESPACIO=pausa  R=aleatorio  B=vacío  G=guardar  C=cargar  CLIC=toggle célula")
    main()


if __name__ == "__main__":
    iniciar()
