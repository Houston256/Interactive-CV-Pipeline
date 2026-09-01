from importlib import import_module


class LayerFactory:
    """This class is used to create instances of the different image processing layers."""
    def __init__(self):
        self.layers = {
            'Edit Image': ('src.layer.edit_image', 'EditImage'),
            'Equalize Histogram': ('src.layer.equalize_hist', 'EqualizeHist'),
            'Find Contours': ('src.layer.contours', 'FindContours'),
            'Morphology': ('src.layer.morphology', 'Morphology'),
            'Double Threshold': ('src.layer.threshold', 'DoubleThreshold'),
            'Box Filter': ('src.layer.convolve.box', 'BoxFilter'),
            'Gaussian Filter': ('src.layer.convolve.gaussian', 'GaussianFilter'),
            'Median Filter': ('src.layer.convolve.median', 'MedianFilter'),
            'Laplacian Filter': ('src.layer.edge.laplace', 'LaplacianFilter'),
            'To Grayscale': ('src.layer.gray', 'ToGrayscale'),
            'Canny Edge Detector': ('src.layer.edge.canny', 'Canny'),
            'Prewitt Edge Detector': ('src.layer.edge.prewitt', 'Prewitt'),
        }

    def get_layer(self, layer_name: str):
        """
        Get the layer class corresponding to the given layer name.
        :param layer_name: name of layer
        :return: Layer class
        """
        module_name, class_name = self.layers[layer_name]
        return getattr(import_module(module_name), class_name)

    def get_layer_names(self):
        """
        Get the names of all available layers.
        :return: layer names: str
        """
        return list(self.layers.keys())
