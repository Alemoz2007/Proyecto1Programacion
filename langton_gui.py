import pygame
import easygui
import pickle
import langton_logica as lan

TICK = 60

def guardar_simulacion(archivo, matriz, hormiga, regla, filas, columnas, tam):
    """Guarda una simulación.
    Entradas y restricciones:
    -archivo (str)
    -matriz (list)
    -hormiga (dict)
    -regla (str)
    -filas (int)
    -columnas (int)
    -tam (int)
    Salida: Ninguna"""
    datos = {"matriz": matriz, "hormiga": hormiga, "regla": regla, "filas": filas, "columnas": columnas, "tam": tam}
    with open(archivo, "wb") as f:
        pickle.dump(datos, f)

def cargar_simulacion(archivo):
    """Carga una simulación.
    Entrada:
    -archivo (str)
    Salida: La simulacion"""
    with open(archivo, "rb") as f:
        datos = pickle.load(f)
    return datos

def validar_regla(regla):
    """Verifica que la regla solo contenga L y R."""
    if len(regla) == 0:
        return False
    for letra in regla:
        if letra not in ("L", "R"):
            return False
    return True

def leer_configuracion():
    """Lee la configuración inicial."""
    while True:
        campos = ["Filas", "Columnas", "Tamaño de celda", "Regla"]
        datos = easygui.multenterbox("Ingrese la configuración", "Hormiga de Langton", campos)
        if datos is None:
            raise SystemExit
        try:
            filas = int(datos[0])
            columnas = int(datos[1])
            tam = int(datos[2])
            regla = datos[3].upper()
            if filas <= 0:
                raise ValueError
            if columnas <= 0:
                raise ValueError
            if tam <= 0:
                raise ValueError
            if not validar_regla(regla):
                raise ValueError
            return filas, columnas, tam, regla
        except:
            easygui.msgbox("Datos inválidos.")


def dibujar_tablero(window, M, colores, filas, columnas, tam):
    """Dibuja el tablero."""
    for fila in range(filas):
        for columna in range(columnas):
            pygame.draw.rect(window, colores[M[fila][columna]],(columna * tam, fila * tam, tam, tam))
            pygame.draw.rect(window, (40, 40, 40), (columna * tam, fila * tam, tam, tam), 1)

def dibujar_hormiga(window, hormiga, tam):
    """Dibuja la hormiga."""
    pygame.draw.rect(window, (255, 0, 0), (hormiga["columna"] * tam, hormiga["fila"] * tam, tam, tam))

def main():

    easygui.msgbox(
        """
CONTROLES

ESPACIO -> Pausar

Click izquierdo -> Cambiar estado

R -> Reinicio aleatorio

B -> Reinicio vacío

G -> Guardar simulación

C -> Cargar simulación
        """,
        "Hormiga de Langton"
    )

    filas, columnas, tam, regla = leer_configuracion()
    pygame.init()
    clock = pygame.time.Clock()
    M = lan.generar_matriz(filas, columnas)
    hormiga = lan.crear_hormiga(filas, columnas)
    colores = lan.generar_colores(len(regla))
    ancho = columnas * tam
    alto = filas * tam
    window = pygame.display.set_mode((ancho, alto))
    pygame.display.set_caption(
        "Hormiga de Langton"
    )
    pausa = False
    loop = True
    while loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pausa = not pausa
                elif event.key == pygame.K_r:
                    M = lan.generar_matriz_aleatoria(filas, columnas, len(regla))
                    hormiga = lan.crear_hormiga(filas, columnas)
                elif event.key == pygame.K_b:
                    M = lan.generar_matriz(filas, columnas)
                    hormiga = lan.crear_hormiga(filas, columnas)
                elif event.key == pygame.K_g:
                    archivo = easygui.filesavebox(default="simulacion.pkl")
                    if archivo:
                        guardar_simulacion(archivo, M, hormiga, regla, filas, columnas, tam)
                elif event.key == pygame.K_c:
                    archivo = easygui.fileopenbox()
                    if archivo:
                        datos = cargar_simulacion(archivo)
                        M = datos["matriz"]
                        hormiga = datos["hormiga"]
                        regla = datos["regla"]
                        filas = datos["filas"]
                        columnas = datos["columnas"]
                        tam = datos["tam"]
                        colores = lan.generar_colores(len(regla))
                        ancho = columnas * tam
                        alto = filas * tam
                        window = pygame.display.set_mode((ancho, alto))
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                fila = y // tam
                columna = x // tam
                if (0 <= fila < filas and 0 <= columna < columnas):
                    M[fila][columna] = (M[fila][columna] + 1) % len(regla)
        if not pausa:
            lan.siguiente(M, hormiga, regla)
        window.fill((0, 0, 0))
        dibujar_tablero(window, M, colores, filas, columnas, tam)
        dibujar_hormiga(window, hormiga, tam)
        pygame.display.update()
        clock.tick(TICK)
    pygame.quit()

if __name__ == "__main__":
    main()
