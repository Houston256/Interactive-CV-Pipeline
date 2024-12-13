from streamlit.testing.v1 import AppTest

from src.layer_factory.layer_factory import LayerFactory
from tests.helpers import *


def test_ui(rgb_image, rgb_image_binary, gray_image, gray_image_binary):
    factory = LayerFactory()
    at = AppTest.from_file('../src/main.py')
    at.session_state['layer_idx'] = 0
    at.run()
    seq = at.session_state['seq']
    assert at.session_state is not None
    assert len(at.button) == 2
    assert at.title[0].body == 'Upload Image'
    assert at.title[1].body == 'Image Processing Pipeline'
    add_btn = at.button[0]
    assert add_btn.label == 'Add'
    seq.layers[-1].set_image(rgb_image)
    assert seq.get_img() is not None
