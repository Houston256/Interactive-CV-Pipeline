import numpy as np
from streamlit.testing.v1 import AppTest

from src.layer_factory.layer_factory import LayerFactory
from tests.helpers import *


def test_set_image(rgb_image, rgb_image_binary, gray_image, gray_image_binary):
    at = AppTest.from_file('../src/main.py').run()
    assert at.session_state is not None
    factory = LayerFactory()
    for layer_name in factory.get_layer_names():
        layer = factory.get_layer(layer_name)(image=rgb_image)
        for image in [rgb_image, rgb_image_binary, gray_image, gray_image_binary]:
            img_cpy = image.copy()
            layer.set_image(image)
            new_layer = factory.get_layer(layer_name)(image=image)
            assert all(l is not None for l in [layer, new_layer]), f'Failed for {layer_name}'
            assert np.array_equal(layer.evaluate().img_in, img_cpy), f'Failed for {layer_name}'
