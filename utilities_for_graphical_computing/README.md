# IS623-ImageTools

Una librería sencilla para el procesamiento y visualización de imágenes, desarrollada para el curso **IS623 - Computación Gráfica** impartido por el Profesor Francisco Alejandro Medina Aguirre en la Universidad Tecnológica de Pereira (UTP), Colombia. Esta librería se encuentra en estado Alpha y es mantenida por **Kevin Esguerra Cardona**.

---

## Características

- **Procesamiento de Imágenes:**  
  Funciones para cargar imágenes, normalizarlas, desnormalizarlas, invertir colores, ajustar contraste e intensidad, entre otras transformaciones.

- **Conversión de Formatos:**  
  Métodos para convertir imágenes de RGB a CMYK y viceversa, así como para extraer capas específicas de cada formato.

- **Filtros y Operaciones:**  
  Aplicación de filtros como el filtro de promedio y operaciones de fusión de imágenes.

- **Escala de Grises:**  
  Conversión a escala de grises utilizando diferentes métodos: promedio, luminosidad y tonalidad.

- **Visualización:**  
  La clase `SimpleImageViewer` permite mostrar múltiples imágenes en una única figura utilizando subplots.

---

## Requisitos

- **Python:** Versión 3.8 o superior  
- **Librerías:**  
  - NumPy  
  - Pillow  
  - Matplotlib

---

## Instalación

1. **Clonar el repositorio:**

   ```bash
   git clone https://ruta-del-repositorio/IS623-ImageTools.git
   cd IS623-ImageTools
   ```

2. **Instalar la librería y sus dependencias:**

   - **Instalación normal:**

     ```bash
     pip install .
     ```

   - **Instalación en modo desarrollo:**

     ```bash
     pip install -e .
     ```

---

## Uso

### Procesamiento de Imágenes

La clase `ImageProcessor` contiene métodos estáticos para realizar diversas operaciones sobre imágenes. Por ejemplo:

```python
from ImageProcessor import ImageProcessor

# Cargar una imagen y convertirla en un arreglo NumPy
imagen_array = ImageProcessor.cargar_imagen_como_numpy("ruta/a/la/imagen.jpg")

# Normalizar la imagen (valores en el rango [0,1])
imagen_normalizada = ImageProcessor.normalizar_imagen(imagen_array)

# Invertir los colores de la imagen
imagen_invertida = ImageProcessor.invertir(imagen_normalizada)

# Convertir la imagen de RGB a CMYK
imagen_cmyk = ImageProcessor.rgb_a_cmyk(imagen_array)
```

### Visualización de Imágenes

La clase `SimpleImageViewer` permite mostrar varias imágenes en una figura, organizándolas en subplots de forma sencilla:

```python
from SimpleImageViewer import SimpleImageViewer

# Diccionario de imágenes con títulos descriptivos
imagenes = {
    "Original": imagen_array,
    "Normalizada": imagen_normalizada,
    "Invertida": imagen_invertida,
    "CMYK": imagen_cmyk  # Nota: Para visualizar correctamente, se recomienda convertir a RGB si es necesario.
}

# Crear el visor y mostrar las imágenes
visor = SimpleImageViewer(imagenes)
visor.show()
```

---

## Documentación de Funcionalidades

### Funciones Clave en `ImageProcessor`

- **Carga y Conversión:**
  - `cargar_imagen_como_numpy`: Carga una imagen y la convierte en un arreglo NumPy.
  
- **Normalización:**
  - `normalizar_imagen`: Escala los valores de la imagen a un rango [0,1].
  - `desnormalizar_imagen`: Convierte una imagen normalizada de vuelta a [0,255].

- **Manipulación de Píxeles:**
  - `colorear_pixel`: Modifica el color de un píxel específico.

- **Transformaciones de Color:**
  - `invertir`: Invierte los colores de la imagen.
  - `extraer_capa_rgb` y `extraer_capa_cmyk`: Extraen una capa específica de la imagen.
  - `rgb_a_cmyk` y `cmyk_a_rgb`: Convierten entre formatos de color RGB y CMYK.

- **Fusión y Filtros:**
  - `fusionar` y `fusionar_ecualizado`: Permiten fusionar múltiples arreglos de imagen.
  - `mean_filter`: Aplica un filtro de promedio a la imagen.

- **Ajustes de Imagen:**
  - `ajustar_imagen`: Modifica la imagen según un factor para ajustar contraste e intensidad.
  - Métodos privados `_contraste` y `_intensidad` para realizar transformaciones específicas.

- **Escala de Grises:**
  - `gris_promedio`: Conversión a escala de grises usando el promedio de los canales.
  - `gris_luminosidad`: Conversión a escala de grises utilizando la fórmula de luminosidad.
  - `gris_tonalidad`: Conversión a escala de grises mediante el método de tonalidad.

### Visualización con `SimpleImageViewer`

Esta clase facilita la visualización de varias imágenes (arreglos NumPy) en una sola figura, distribuyéndolas en subplots de dos filas y dos columnas. Es ideal para comparar diferentes transformaciones o resultados del procesamiento.

---

## Contribuciones

Si deseas contribuir al desarrollo de **IS623-ImageTools**, por favor:

- Abre un *issue* para reportar errores o sugerir mejoras.
- Envía un *pull request* con tus propuestas de cambio.

Todas las contribuciones son bienvenidas para mejorar esta herramienta.

---

## Licencia

Este proyecto se distribuye bajo la **Licencia MIT**. Consulta el archivo de licencia para más detalles.

---

## Créditos

- **Profesor:** Francisco Alejandro Medina Aguirre  
- **Desarrollador:** Kevin Esguerra Cardona  
- **Universidad:** Universidad Tecnológica de Pereira (UTP)

---

Disfruta procesando y visualizando imágenes con **IS623-ImageTools**. ¡Esperamos tus aportes y comentarios!