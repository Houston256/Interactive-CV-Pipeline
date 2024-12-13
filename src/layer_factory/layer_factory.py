from src.layer.contours import FindContours
from src.layer.convolve.box import BoxFilter
from src.layer.convolve.gaussian import GaussianFilter
from src.layer.convolve.median import MedianFilter
from src.layer.edge.canny import Canny
from src.layer.edge.laplace import LaplacianFilter
from src.layer.edge.prewitt import Prewitt
from src.layer.edit_image import EditImage
from src.layer.equalize_hist import EqualizeHist
from src.layer.gray import ToGrayscale
from src.layer.morphology import Morphology
from src.layer.threshold import DoubleThreshold


class LayerFactory:
    """This class is used to create instances of the different image processing layers."""
    def __init__(self):
        self.layers = {
            'Edit Image': EditImage,
            'Equalize Histogram': EqualizeHist,
            'Find Contours': FindContours,
            'Morphology': Morphology,
            'Double Threshold': DoubleThreshold,
            'Box Filter': BoxFilter,
            'Gaussian Filter': GaussianFilter,
            'Median Filter': MedianFilter,
            'Laplacian Filter': LaplacianFilter,
            'To Grayscale': ToGrayscale,
            'Canny Edge Detector': Canny,
            'Prewitt Edge Detector': Prewitt,
        }

    def get_layer(self, layer_name: str):
        """
        Get the layer class corresponding to the given layer name.
        :param layer_name: name of layer
        :return: Layer class
        """
        return self.layers[layer_name]

    def get_layer_names(self):
        """
        Get the names of all available layers.
        :return: layer names: str
        """
        return list(self.layers.keys())
