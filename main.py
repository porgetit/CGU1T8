import ImageProcessing as ip
import numpy as np
import matplotlib.pyplot as plt

def matriz3x3Personalizada():
    """Función que genera y retorna una matriz 3x3 con valores personalizados.
    """
    matriz = np.zeros((3,3,3))
    matriz = ip.ImageProcessor.colorear_pixel(matriz, 0, 0, [0,1,1]) # cyan
    matriz = ip.ImageProcessor.colorear_pixel(matriz, 0, 1, [1,1,1]) # blanco
    matriz = ip.ImageProcessor.colorear_pixel(matriz, 0, 2, [1,0,0]) # rojo
    matriz = ip.ImageProcessor.colorear_pixel(matriz, 1, 0, [1,0,1]) # magenta
    matriz = ip.ImageProcessor.colorear_pixel(matriz, 1, 1, [0.5, 0.5, 0.5]) # gris
    matriz = ip.ImageProcessor.colorear_pixel(matriz, 1, 2, [0, 1, 0]) # verde
    matriz = ip.ImageProcessor.colorear_pixel(matriz, 2, 0, [1, 1, 0]) # amarillo
    matriz = ip.ImageProcessor.colorear_pixel(matriz, 2, 2, [0, 0, 1]) # azul
    return matriz

def matriz6x11PantallaTelevision():
    """Función que genera y retorna una matriz 6x11 con valores personalizados emulando una antigua pantalla de televisión.
    """
    matriz = np.zeros((8,11,3))
    matriz = ip.ImageProcessor.colorear_pixel(matriz, slice(0,6), 0, [1,1,0]) # barra amarilla
    matriz = ip.ImageProcessor.colorear_pixel(matriz, slice(0,6), slice(1,3), [0,1,1]) # barra cyan
    matriz = ip.ImageProcessor.colorear_pixel(matriz, slice(0,6), slice(3,5), [0,1,0]) # barra verde
    matriz = ip.ImageProcessor.colorear_pixel(matriz, slice(0,6), slice(5,7), [1,0,1]) # barra magenta
    matriz = ip.ImageProcessor.colorear_pixel(matriz, slice(0,6), slice(7,9), [1,0,0]) # barra roja
    matriz = ip.ImageProcessor.colorear_pixel(matriz, slice(0,6), slice(9,11), [0,0,1]) # barra azul
    for i in range(8):  
        matriz = ip.ImageProcessor.colorear_pixel(matriz, slice(6,8), i, [(7-i)/7, (7-i)/7, (7-i)/7]) # barra escala de grises 
    return matriz * 0.6



if __name__ == "__main__":
    
    matriz3x3 = matriz3x3Personalizada()
    matriz6x11 = matriz6x11PantallaTelevision()
    paris = ip.ImageProcessor.cargar_imagen_como_numpy("paris.jpg")
    paris = ip.ImageProcessor.normalizar_imagen(paris)
    paris_invertida = ip.ImageProcessor.invertir(paris)
    paris_roja = ip.ImageProcessor.extraer_capa_rgb(paris, 0)
    paris_verda = ip.ImageProcessor.extraer_capa_rgb(paris, 1)
    paris_azul = ip.ImageProcessor.extraer_capa_rgb(paris, 2)
    paris_cyan = ip.ImageProcessor.extraer_capa_cmyk(paris, 0)
    paris_magenta = ip.ImageProcessor.extraer_capa_cmyk(paris, 1)
    paris_yellow = ip.ImageProcessor.extraer_capa_cmyk(paris, 2)
    paris_black = ip.ImageProcessor.extraer_capa_cmyk(paris, 3)
    paris_original_rgb = ip.ImageProcessor.fusionar([paris_roja, paris_verda, paris_azul])
    paris_original_cmyk = ip.ImageProcessor.fusionar_ecualizado([(paris_cyan, 0.266), (paris_magenta, 0.266), (paris_yellow, 0.266), (paris_black, 0.202)])
    paris_alto_contraste = ip.ImageProcessor.desnormalizar_imagen(ip.ImageProcessor.ajustar_imagen(paris, -0.8))
    paris_alta_intensidad = ip.ImageProcessor.desnormalizar_imagen(ip.ImageProcessor.ajustar_imagen(paris, 0.8))
    paris_mean = ip.ImageProcessor.mean_filter(paris, 3)
    paris_gray_mean = ip.ImageProcessor.gris_promedio(paris)
    paris_gray_lum = ip.ImageProcessor.gris_luminosidad(paris)
    paris_gray_ton = ip.ImageProcessor.gris_tonalidad(paris)

    
        
    images = {
        "Matriz 3x3 personalizada": matriz3x3,
        "Pantalla de TV": matriz6x11,
        "Paris - Invertida": paris_invertida,
        "Paris - Capa Roja": paris_roja,
        "Paris - Capa Cyan": paris_cyan,
        "Paris - Capa Magenta": paris_magenta,
        "Paris - Capa Yellow": paris_yellow,
        "Paris - Capa Black": paris_black,
        "Paris - Original RGB": paris_original_rgb,
        "Paris - Original CMYK": paris_original_cmyk,
        "Paris - Alto Contraste": paris_alto_contraste,
        "Paris - Alta Intensidad": paris_alta_intensidad,
        "Paris - Mean Filter": paris_mean,
        "Paris - Grises (Mean)": paris_gray_mean,
        "Paris - Grises (Luminosity)": paris_gray_lum,
        "Paris - Grises (Tonalidad)": paris_gray_ton,        
    }
    
    viewer = ip.SimpleImageViewer(images)
    viewer.show()