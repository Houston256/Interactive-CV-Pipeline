import numpy as np
import pytest


def generate_random_image(size, value_range, channels=1, binary=False) -> np.ndarray:
    """
    Generate a random image with the specified size, value range, and number of channels.
    :param binary: if True, generate a binary image with values 0 and 255
    :param size: int or tuple of int with the size of the image
    :param value_range: tuple with the minimum and maximum values for the image
    :param channels: number of channels for the image (1 or 3)
    :return: random np.ndarray representing the image
    """
    # BINARY
    if binary:
        return np.random.choice([0, 255], size)
    min_val, max_val = value_range
    # RGB
    if channels == 3:
        return np.stack([generate_random_image(size, value_range) for _ in range(channels)], axis=-1)
    # GRAYSCALE
    else:
        return np.random.randint(min_val, max_val + 1, size, dtype=np.uint8)


# Define image fixtures that will be used across all tests
# should be more efficient than generating new image everytime
SIZE = 100


@pytest.fixture(scope="session")
def rgb_image():
    return generate_random_image((SIZE, SIZE), (0, 255), channels=3)


@pytest.fixture(scope="session")
def rgb_image_binary():
    return generate_random_image((SIZE, SIZE), (0, 1), channels=3)


@pytest.fixture(scope="session")
def gray_image():
    return generate_random_image((SIZE, SIZE), (0, 255))


@pytest.fixture(scope="session")
def gray_image_binary():
    return generate_random_image((SIZE, SIZE), (0, 1))
