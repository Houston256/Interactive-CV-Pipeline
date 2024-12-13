import numpy as np
from streamlit.testing.v1 import AppTest

from src.layer.layer import Layer
from src.layer_factory.layer_factory import LayerFactory
from tests.helpers import *


def test_return_type(rgb_image):
    at = AppTest.from_file('../src/main.py').run()
    assert at.session_state is not None
    factory = LayerFactory()
    for layer_name in factory.get_layer_names():
        layer = factory.get_layer(layer_name)(image=rgb_image)
        assert isinstance(layer.interact(), Layer)
        assert isinstance(layer.evaluate(), Layer)
        assert isinstance(str(layer), str)
        assert isinstance(layer.get_img(), np.ndarray)
