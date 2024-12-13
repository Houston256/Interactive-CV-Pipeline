from src.layer_factory.layer_factory import LayerFactory
from src.sequential.sequential import Sequential
from tests.helpers import *


def test_sequential_pipeline(rgb_image):
    seq = Sequential()

    factory = LayerFactory()
    layer_names = factory.get_layer_names()
    seq.layers[-1].set_image(rgb_image)
    seq.evaluate()
    for layer_name in layer_names:
        seq.add_layer(factory.get_layer(layer_name))

    result = seq.evaluate()

    assert isinstance(result, type(rgb_image))

    for i in range(len(layer_names)):
        seq.remove_last()
        result = seq.evaluate()
        assert len(seq.layers) == len(layer_names) - i
        assert isinstance(result, type(rgb_image))

    assert len(seq.layers) == 1
