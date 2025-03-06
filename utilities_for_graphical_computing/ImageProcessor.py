import numpy as np
from PIL import Image

class ImageProcessor:
    """
    Clase para manejar el procesamiento de imágenes representadas como arreglos de NumPy.
    """   
    
    @staticmethod
    def cargar_imagen_como_numpy(ruta: str) -> np.ndarray:
        """
        Carga una imagen desde la ruta especificada y la convierte en un arreglo numpy de forma (3,3,3).
        
        Parámetros:
            ruta (str): Ruta a la imagen.
        
        Retorna:
            np.ndarray: Arreglo de la imagen en formato RGB de forma (3,3,3).
        """
        # Abrir la imagen y asegurar que tenga 3 canales (RGB)
        imagen = Image.open(ruta).convert("RGB")
        # Convertir la imagen a arreglo numpy
        arreglo = np.array(imagen)
        return arreglo
    
    @staticmethod
    def normalizar_imagen(arr: np.ndarray) -> np.ndarray:
        """
        Normaliza un arreglo de imagen para que sus valores estén en el rango [0,1].
        
        Parámetros:
            arr (np.ndarray): Arreglo de imagen con valores en el rango [0,255].
        
        Retorna:
            np.ndarray: Arreglo de imagen normalizado con valores en el rango [0,1].
        """
        return arr / 255.0
    
    @staticmethod
    def desnormalizar_imagen(arr: np.ndarray) -> np.ndarray:
        """
        Desnormaliza un arreglo de imagen para que sus valores estén en el rango [0,255].
        
        Parámetros:
            arr (np.ndarray): Arreglo de imagen con valores en el rango [0,1].
        
        Retorna:
            np.ndarray: Arreglo de imagen desnormalizado con valores en el rango [0,255].
        """
        return (arr * 255).astype(np.uint8)

    @staticmethod
    def colorear_pixel(matriz, row, col, lista):
        """Colorea un píxel específico en una matriz de imagen."""
        matriz[row, col, :] = lista
        return matriz

    @staticmethod
    def invertir(imagen):
        """Invierte los colores de una imagen."""
        return 1 - imagen

    @staticmethod
    def extraer_capa_rgb(arr: np.ndarray, indice: int) -> np.ndarray:
        """
        Extrae una capa específica de un arreglo tridimensional y devuelve un nuevo arreglo
        con solo esa capa en la tercera dimensión, manteniendo las otras capas en cero.

        Parameters:
            arr (np.ndarray): Arreglo tridimensional de entrada con forma (M, N, 3).
            indice (int): Índice de la capa a extraer (debe estar entre 0 y 2).

        Returns:
            np.ndarray: Nuevo arreglo tridimensional con solo la capa especificada en la tercera dimensión.

        Raises:
            ValueError: Si el arreglo no tiene 3 capas en la tercera dimensión.
            ValueError: Si el índice no está entre 0 y 2.
        """
        # Verificar que el arreglo tenga 3 capas en la tercera dimensión
        if arr.shape[2] != 3:
            raise ValueError("El arreglo debe tener 3 capas en la tercera dimensión")
        # Verificar que el índice esté entre 0 y 2
        if not (0 <= indice <= 2):
            raise ValueError("El índice debe estar entre 0 y 2")
        # Crear una copia del arreglo original para no modificarlo directamente
        arr_modificado = np.zeros_like(arr)
        # Asignar la capa deseada a la copia
        arr_modificado[:, :, indice] = arr[:, :, indice]
        return arr_modificado
    
    @staticmethod
    def extraer_capa_cmyk(arr: np.ndarray, indice: int) -> np.ndarray:
        """
        Extrae una capa específica de un arreglo tridimensional para el formato CMYK y devuelve un nuevo arreglo
        con solo esa capa en la tercera dimensión, manteniendo las otras capas en cero.

        Parameters:
            arr (np.ndarray): Arreglo tridimensional de entrada con forma (M, N, 4) para el formato CMYK.
            indice (int): Índice de la capa a extraer (debe estar entre 0 y 3).

        Returns:
            np.ndarray: Nuevo arreglo tridimensional con solo la capa especificada en la tercera dimensión.

        Raises:
            ValueError: Si el arreglo no tiene 4 capas en la tercera dimensión.
            ValueError: Si el índice no está entre 0 y 3.
        """
        # Verificar que el arreglo tenga 4 capas en la tercera dimensión
        if arr.shape[-1] != 3:
            raise ValueError("El arreglo debe tener 3 capas en la tercera dimensión para RGB")
        # Verificar que el índice esté entre 0 y 3
        if not (0 <= indice <= 3):
            raise ValueError("El índice debe estar entre 0 y 3")
        # Crear una copia del arreglo original con ceros
        arr_modificado = np.zeros_like(arr)
        # Asignar la capa deseada a la copia
        if indice == 0: # cyan
            arr_modificado[:,:,1] = arr[:,:,1]
            arr_modificado[:,:,2] = arr[:,:,2]
            return arr_modificado
        elif indice == 1: # magenta
            arr_modificado[:,:,0] = arr[:,:,0]
            arr_modificado[:,:,2] = arr[:,:,2]
            return arr_modificado
        elif indice == 2: # yellow
            arr_modificado[:,:,0] = arr[:,:,0]
            arr_modificado[:,:,1] = arr[:,:,1]
            return arr_modificado
        elif indice == 3: # black
            return arr_modificado
            
    
    @staticmethod
    def rgb_a_cmyk(arr: np.ndarray) -> np.ndarray:
        """
        Convierte un arreglo con formato RGB (3 canales) a formato CMYK (4 canales).
        Se asume que el arreglo RGB está en el rango [0, 255]. La conversión se realiza
        normalizando los valores a [0,1] y usando la siguiente fórmula:
        
            K = 1 - max(R, G, B)
            Si K == 1:  C = M = Y = 0  (la imagen es negra)
            Si K < 1:
                C = (1 - R - K) / (1 - K)
                M = (1 - G - K) / (1 - K)
                Y = (1 - B - K) / (1 - K)
        
        Parameters:
            arr (np.ndarray): Arreglo RGB de entrada con forma (M, N, 3).
            
        Returns:
            np.ndarray: Arreglo CMYK resultante con forma (M, N, 4) en rango [0,1].
            
        Raises:
            ValueError: Si el arreglo no tiene 3 canales en la última dimensión.
        """
        if arr.shape[-1] != 3:
            raise ValueError("El arreglo debe tener 3 canales (RGB)")

        # Verificar si el arreglo ya está normalizado (asumiendo que los valores normalizados están en el rango [0, 1])
        if arr.max() > 1:
            # Normalizar el arreglo a rango [0,1]
            arr_norm = arr.astype(np.float32) / 255.0
        else:
            arr_norm = arr

        # Extraer canales R, G, B
        R = arr_norm[..., 0]
        G = arr_norm[..., 1]
        B = arr_norm[..., 2]

        # Calcular el canal K        
        K = 1 - np.max(arr_norm, axis=-1)
        
        # Evitar división por cero: si K==1 (píxel negro), se asigna 0 a C, M y Y.
        C = np.where(K == 1, 0, (1 - R - K) / (1 - K))
        M = np.where(K == 1, 0, (1 - G - K) / (1 - K))
        Y = np.where(K == 1, 0, (1 - B - K) / (1 - K))
        print(f"C:{C}, M:{M}, Y:{Y}, K:{K}")
        
        # Combinar los canales en un solo arreglo (M, N, 4)
        cmyk = np.stack((C, M, Y, K), axis=-1)
        return cmyk

    @staticmethod
    def cmyk_a_rgb(arr: np.ndarray) -> np.ndarray:
        """
        Convierte un arreglo con formato CMYK (4 canales) a formato RGB (3 canales).
        Se asume que el arreglo CMYK está en el rango [0,1]. La conversión se realiza
        usando la siguiente fórmula:
        
            R = (1 - C) * (1 - K)
            G = (1 - M) * (1 - K)
            B = (1 - Y) * (1 - K)
        
        Parameters:
            arr (np.ndarray): Arreglo CMYK de entrada con forma (M, N, 4).
            
        Returns:
            np.ndarray: Arreglo RGB resultante con forma (M, N, 3) en rango [0,1].
                        Si se requiere en [0,255], se puede escalar y convertir a uint8.
                        
        Raises:
            ValueError: Si el arreglo no tiene 4 canales en la última dimensión.
        """
        if arr.shape[-1] != 4:
            raise ValueError("El arreglo debe tener 4 canales (CMYK)")

        # Extraer canales C, M, Y, K
        C = arr[..., 0]
        M = arr[..., 1]
        Y = arr[..., 2]
        K = arr[..., 3]
        
        # Calcular los canales RGB
        R = (1 - C) * (1 - K)
        G = (1 - M) * (1 - K)
        B = (1 - Y) * (1 - K)
        
        # Combinar en un arreglo (M, N, 3)
        rgb = np.stack((R, G, B), axis=-1)
        
        # Opcional: convertir de [0,1] a [0,255] y a tipo uint8:
        # rgb_uint8 = (rgb * 255).astype(np.uint8)
        # return rgb_uint8
        
        return rgb
    
    @staticmethod
    def fusionar(arr: list[np.ndarray]) -> np.ndarray:
        """
        Suma las capas de un arreglo n-dimensional y devuelve un nuevo arreglo con estas capas solapadas.
        
        Parameters:
            arr (np.ndarray): Arreglo n-dimensional de entrada con forma (M, N, T).
            
        Returns:
            np.ndarray: Nuevo arreglo n-dimensional con las capas solapadas.
            
        Raises:
            ValueError: Si las capas no tienen el mismo número de filas y columnas.
        """
        # Verificar que todas las capas tengan el mismo número de filas y columnas
        if len(set([a.shape[:2] for a in arr])) != 1:
            raise ValueError("Las capas deben tener el mismo número de filas y columnas")
        
        arr_solapado = np.zeros_like(arr[0])
        for array in arr:
            arr_solapado += array
            
        return arr_solapado
    
    @staticmethod
    def fusionar_ecualizado(arr_list: list[tuple[np.ndarray, int]]) -> np.ndarray:
        """
        Suma las capas de un arreglo n-dimensional de acuerdo a un índice de ecualización y devuelve un nuevo arreglo con estas capas solapadas.
        
        Parameters:
            arr_list (list): Lista de tuplas donde cada tupla contiene un arreglo n-dimensional de entrada con forma (M, N, T) y un índice de ecualización.
            
        Returns:
            np.ndarray: Nuevo arreglo n-dimensional con las capas solapadas.
            
        Raises:
            ValueError: Si las capas no tienen el mismo número de filas y columnas.
        """
        # Verificar que todas las capas tengan el mismo número de filas y columnas
        if len(set([a.shape[:2] for a, _ in arr_list])) != 1:
            raise ValueError("Las capas deben tener el mismo número de filas y columnas")
        
        arr_solapado = np.zeros_like(arr_list[0][0])
        for array, indice in arr_list:
            arr_solapado += array * indice
            
        return arr_solapado
    
    @staticmethod
    def ajustar_imagen(img: np.ndarray, factor: float) -> np.ndarray:
        """
        Ajusta la imagen según un factor en el rango [-1, 1].
        
        Parámetros
        ----------
        img : np.ndarray
            Imagen de entrada en formato RGB con forma (Alto, Ancho, 3).
        factor : float
            Valor entre -1 y 1 que determina el tipo y la intensidad de la transformación:
              -  0   => no se aplica ninguna transformación.
              - menor a 0   => se aplica la transformación logarítmica (contraste).
              - mayor a 0   => se aplica la transformación exponencial (intensidad).

        Retorna
        -------
        np.ndarray
            La imagen resultante (con los mismos canales y dimensiones que la original).
        """
        if factor == 0:
            # Si el factor es 0, retornamos una copia de la imagen sin cambios
            return img.copy()
        elif factor < 0:
            # factor negativo => potenciar zonas oscuras (contraste)
            return ImageProcessor._contraste(img, factor)
        else:
            # factor positivo => potenciar zonas claras (intensidad)
            return ImageProcessor._intensidad(img, factor)

    @staticmethod
    def _contraste(img: np.ndarray, factor: float) -> np.ndarray:
        """
        Aplica una transformación logarítmica en base 10 y mezcla con la imagen original
        para realzar las zonas oscuras en detrimento de las claras.

        Parámetros
        ----------
        img : np.ndarray
            Imagen de entrada en formato RGB con forma (Alto, Ancho, 3).
        factor : float
            Factor negativo en el rango [-1, 0). Su valor absoluto determina
            la intensidad de la mezcla con la transformación logarítmica.

        Retorna
        -------
        np.ndarray
            Imagen resultante con el contraste realzado.
        """
        # Verificar si el arreglo ya está normalizado (asumiendo que los valores normalizados están en el rango [0, 1])
        if img.max() > 1:
            # Escalamos la imagen a [0, 1] en tipo float para evitar problemas con log
            img_norm = img.astype(np.float32) / 255.0
        else:
            img_norm = img.astype(np.float32)
        
        # Constante para normalizar la salida del log (base 10)
        # log10(1 + 1) = log10(2). Si usamos c = 1 / log10(2), 
        # aseguramos que el máximo sea ~1 en la transformada.
        c = 1.0 / np.log10(2.0) # TODO aprovar nuevos valores para c a fin de mejorar el efecto de contraste
        
        # Aplicamos la transformación logarítmica a cada canal
        # Evitamos log(0) usando (1 + valor), asumiendo img_norm en [0,1]
        log_img = c * np.log10(1.0 + img_norm)
        
        # Mezcla lineal entre la imagen original y la transformada
        # # factor_abs en [0,1] indica cuánto pesa la transformada
        # factor_abs = abs(factor)
        # blended = (1.0 - factor_abs) * img_norm + factor_abs * log_img
        
        return log_img

    @staticmethod
    def _intensidad(img: np.ndarray, factor: float) -> np.ndarray:
        """
        Aplica una transformación exponencial y mezcla con la imagen original
        para realzar las zonas claras en detrimento de las oscuras.

        Parámetros
        ----------
        img : np.ndarray
            Imagen de entrada en formato RGB con forma (Alto, Ancho, 3).
        factor : float
            Factor positivo en el rango (0, 1]. Su valor determina la intensidad
            de la mezcla con la transformación exponencial.

        Retorna
        -------
        np.ndarray
            Imagen resultante con mayor realce en las zonas claras.
        """
        # Verificar si el arreglo ya está normalizado (asumiendo que los valores normalizados están en el rango [0, 1])
        if img.max() > 1:
            # Escalamos la imagen a [0, 1]
            img_norm = img.astype(np.float32) / 255.0
        else:
            img_norm = img.astype(np.float32)
        
        # Definimos la transformada exponencial.
        # Aquí, (exp(x) - 1)/(e - 1) hace que el resultado esté en [0,1].
        exp_img = (np.exp(img_norm) - 1.0) / (np.e - 1.0) # TODO aplica la técnica de realce de contraste expresa en la presentación de clase
        
        # Mezcla lineal entre la imagen original y la transformada
        # factor_abs = abs(factor)  # en este caso factor > 0, pero se usa por consistencia
        # blended = (1.0 - factor_abs) * img_norm + factor_abs * exp_img
        
        return exp_img
    
    @staticmethod
    def mean_filter(img: np.ndarray, kernel_size: int = 3) -> np.ndarray:
        """
        Aplica un filtro de promedio a la imagen.

        Parámetros:
            img (np.ndarray): Imagen de entrada en formato RGB con forma (Alto, Ancho, 3).
            kernel_size (int): Tamaño del kernel cuadrado para el filtro de promedio. Debe ser un número impar.

        Retorna:
            np.ndarray: Imagen filtrada con el filtro de promedio aplicado.
        """
        if kernel_size % 2 == 0:
            raise ValueError("El tamaño del kernel debe ser un número impar")

        # Padding para mantener el tamaño de la imagen
        pad_size = kernel_size // 2
        img_padded = np.pad(img, ((pad_size, pad_size), (pad_size, pad_size), (0, 0)), mode='reflect')

        # Crear una imagen de salida vacía
        img_filtered = np.zeros_like(img)

        # Aplicar el filtro de promedio
        for i in range(img.shape[0]):
            for j in range(img.shape[1]):
                for k in range(img.shape[2]):
                    img_filtered[i, j, k] = np.mean(img_padded[i:i + kernel_size, j:j + kernel_size, k])

        return img_filtered

    @staticmethod
    def gris_promedio(img):
        """
        Convierte la imagen a escala de grises usando el promedio de los canales.
        Formula: gray = (R + G + B) / 3
        
        Parámetros:
        -----------
        img : numpy.ndarray
            Arreglo de la imagen con forma (H, W, 3).
        
        Retorna:
        --------
        numpy.ndarray
            Imagen en escala de grises con forma (H, W, 3).
        """
        # 1. Calcula el promedio por píxel (reduce el canal, axis=2)
        gray_2d = np.mean(img, axis=2)  # (H, W)

        # 2. Replica el resultado a 3 canales
        # Opción A: usando stack
        gray_3ch = np.stack((gray_2d, gray_2d, gray_2d), axis=-1)
        # Opción B: usando dstack
        # gray_3ch = np.dstack((gray_2d, gray_2d, gray_2d))
        # Opción C: usando np.repeat
        # gray_3ch = np.repeat(gray_2d[..., np.newaxis], 3, axis=2)

        return gray_3ch


    @staticmethod
    def gris_luminosidad(img):
        """
        Convierte la imagen a escala de grises usando el método de luminosidad.
        Fórmula estándar (RGB):
            gray = 0.299*R + 0.587*G + 0.114*B
        
        Parámetros:
        -----------
        img : numpy.ndarray
            Arreglo de la imagen con forma (alto, ancho, 3).
        
        Retorna:
        --------
        numpy.ndarray
            Imagen en escala de grises con forma (alto, ancho).
        """
        # Separamos canales
        R = img[:, :, 0]
        G = img[:, :, 1]
        B = img[:, :, 2]
        # Aplicamos la fórmula
        gray = 0.299 * R + 0.587 * G + 0.114 * B
        return np.stack((gray, gray, gray), axis=-1)

    @staticmethod
    def gris_tonalidad(img):
        """
        Convierte la imagen a escala de grises usando el método de tonalidad (midgray).
        Fórmula:
            gray = (max(R, G, B) + min(R, G, B)) / 2
        
        Parámetros:
        -----------
        img : numpy.ndarray
            Arreglo de la imagen con forma (alto, ancho, 3).
        
        Retorna:
        --------
        numpy.ndarray
            Imagen en escala de grises con forma (alto, ancho).
        """
        # Obtenemos el valor máximo y mínimo de cada pixel entre R, G, B
        max_val = np.max(img, axis=2)
        min_val = np.min(img, axis=2)
        # Calculamos la media de ambos
        gray = (max_val + min_val) / 2.0
        return np.stack((gray, gray, gray), axis=-1)