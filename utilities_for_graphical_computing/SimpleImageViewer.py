import matplotlib.pyplot as plt

class SimpleImageViewer:
    """
    Clase sencilla para mostrar múltiples imágenes (arreglos NumPy) en una sola figura.
    """
    
    def __init__(self, images_dict: dict):
        """Inicializa la clase con un diccionario de imágenes."""
        self.images_dict = images_dict
    
    def show(self):
        """Muestra todas las imágenes en figuras con subplots de dos filas y dos columnas."""
        n_images = len(self.images_dict)
        images_per_figure = 4
        scale = 5

        # Crear tantas figuras como sea necesario
        for i in range(0, n_images, images_per_figure):
            fig, axes = plt.subplots(2, 2, figsize=(scale * 2, scale * 2))
            fig.subplots_adjust(hspace=0.5, wspace=0.5)
            
            # Asegurarse de que axes sea una matriz 2D
            axes = axes.flatten()
            
            for ax, (title, image_array) in zip(axes, list(self.images_dict.items())[i:i + images_per_figure]):
                ax.imshow(image_array)
                ax.set_title(title)
                ax.axis('off')
            
            # Ocultar ejes no utilizados
            for ax in axes[len(list(self.images_dict.items())[i:i + images_per_figure]):]:
                ax.axis('off')
        
        plt.show()
