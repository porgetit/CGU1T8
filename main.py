from utilities_for_graphical_computing import Imagen, SimpleImageViewer
import numpy as np


def colorear_region(imagen: Imagen, rows, cols, color: list[int]) -> Imagen:
    """
    Colorea una región de la imagen especificada por filas y columnas.
    Los parámetros 'rows' y 'cols' pueden ser índices individuales o slices.
    
    Parámetros:
        imagen (Imagen): Instancia de Imagen.
        rows (int o slice): Índice o rango de filas a colorear.
        cols (int o slice): Índice o rango de columnas a colorear.
        color (list[int]): Lista de valores de color (la longitud debe coincidir con el número de canales).
    
    Retorna:
        Imagen: La misma instancia con la región coloreada.
    """
    # Convertir rows a lista de índices
    if isinstance(rows, slice):
        rows = list(range(*rows.indices(imagen.datos.shape[0])))
    elif isinstance(rows, int):
        rows = [rows]
    # Convertir cols a lista de índices
    if isinstance(cols, slice):
        cols = list(range(*cols.indices(imagen.datos.shape[1])))
    elif isinstance(cols, int):
        cols = [cols]
    for r in rows:
        for c in cols:
            imagen.colorear_pixel(r, c, color)
    return imagen


def matriz3x3Personalizada():
    """
    Genera y retorna una matriz 3x3 con valores personalizados.
    
    Retorna:
        np.ndarray: Arreglo de imagen resultante.
    """
    imagen = Imagen(np.zeros((3, 3, 3), dtype=float))
    imagen.colorear_pixel(0, 0, [0, 1, 1])    # cyan
    imagen.colorear_pixel(0, 1, [1, 1, 1])    # blanco
    imagen.colorear_pixel(0, 2, [1, 0, 0])    # rojo
    imagen.colorear_pixel(1, 0, [1, 0, 1])    # magenta
    imagen.colorear_pixel(1, 1, [0.5, 0.5, 0.5])  # gris
    imagen.colorear_pixel(1, 2, [0, 1, 0])    # verde
    imagen.colorear_pixel(2, 0, [1, 1, 0])    # amarillo
    imagen.colorear_pixel(2, 2, [0, 0, 1])    # azul
    return imagen.datos


def matriz6x11PantallaTelevision():
    """
    Genera y retorna una matriz 6x11 con valores personalizados emulando una antigua pantalla de televisión.
    
    Retorna:
        np.ndarray: Arreglo de imagen resultante.
    """
    imagen = Imagen(np.zeros((8, 11, 3), dtype=float))
    # Asignar barras de color utilizando la función auxiliar para colorear regiones
    colorear_region(imagen, slice(0, 6), 0, [1, 1, 0])        # barra amarilla
    colorear_region(imagen, slice(0, 6), slice(1, 3), [0, 1, 1])  # barra cyan
    colorear_region(imagen, slice(0, 6), slice(3, 5), [0, 1, 0])  # barra verde
    colorear_region(imagen, slice(0, 6), slice(5, 7), [1, 0, 1])  # barra magenta
    colorear_region(imagen, slice(0, 6), slice(7, 9), [1, 0, 0])  # barra roja
    colorear_region(imagen, slice(0, 6), slice(9, 11), [0, 0, 1]) # barra azul
    # Asignar la barra de escala de grises
    for i in range(8):
        colorear_region(imagen, slice(6, 8), i, [(7 - i) / 7] * 3)
    return imagen.datos * 0.6


if __name__ == "__main__":
    # Crear imágenes personalizadas
    matriz3x3 = matriz3x3Personalizada()
    matriz6x11 = matriz6x11PantallaTelevision()

    # Cargar y procesar la imagen "paris.jpg"
    paris = Imagen.desde_archivo("paris.jpg").normalizar()

    # Crear copias para cada operación, de modo que no se modifique la imagen original
    paris_invertida = Imagen(paris.datos.copy()).invertir().datos
    paris_roja = Imagen(paris.datos.copy()).extraer_capa_rgb(0)
    paris_verda = Imagen(paris.datos.copy()).extraer_capa_rgb(1)
    paris_azul = Imagen(paris.datos.copy()).extraer_capa_rgb(2)
    paris_cyan = Imagen(paris.datos.copy()).extraer_capa_cmyk(0)
    paris_magenta = Imagen(paris.datos.copy()).extraer_capa_cmyk(1)
    paris_yellow = Imagen(paris.datos.copy()).extraer_capa_cmyk(2)
    paris_black = Imagen(paris.datos.copy()).extraer_capa_cmyk(3)

    paris_original_rgb = Imagen.fusionar([paris_roja, paris_verda, paris_azul]).datos
    paris_original_cmyk = Imagen.fusionar_ecualizado([
        (paris_cyan, 0.266),
        (paris_magenta, 0.266),
        (paris_yellow, 0.266),
        (paris_black, 0.202)
    ]).datos

    paris_alto_contraste = Imagen(paris.datos.copy()).ajustar(-0.8).desnormalizar().datos
    paris_alta_intensidad = Imagen(paris.datos.copy()).ajustar(0.8).desnormalizar().datos
    paris_mean = Imagen(paris.datos.copy()).mean_filter(3).datos
    paris_gray_mean = Imagen(paris.datos.copy()).gris_promedio().datos
    paris_gray_lum = Imagen(paris.datos.copy()).gris_luminosidad().datos
    paris_gray_ton = Imagen(paris.datos.copy()).gris_tonalidad().datos

    # Preparar diccionario de imágenes para visualizar
    images = {
        "Matriz 3x3 personalizada": matriz3x3,
        "Pantalla de TV": matriz6x11,
        "Paris - Invertida": paris_invertida,
        "Paris - Capa Roja": paris_roja.datos,
        "Paris - Capa Cyan": paris_cyan.datos,
        "Paris - Capa Magenta": paris_magenta.datos,
        "Paris - Capa Yellow": paris_yellow.datos,
        "Paris - Capa Black": paris_black.datos,
        "Paris - Original RGB": paris_original_rgb,
        "Paris - Original CMYK": paris_original_cmyk,
        "Paris - Alto Contraste": paris_alto_contraste,
        "Paris - Alta Intensidad": paris_alta_intensidad,
        "Paris - Mean Filter": paris_mean,
        "Paris - Grises (Mean)": paris_gray_mean,
        "Paris - Grises (Luminosity)": paris_gray_lum,
        "Paris - Grises (Tonalidad)": paris_gray_ton,
    }

    viewer = SimpleImageViewer(images)
    viewer.show()
