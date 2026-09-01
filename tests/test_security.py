import asyncio
from io import BytesIO

import numpy as np
from PIL import Image

import src.layer.contours as contours_module
from src.layer.convolve.box import BoxFilter
from src.layer.convolve.gaussian import GaussianFilter
from src.layer.convolve.median import MedianFilter
from src.layer.edge.canny import Canny
from src.layer.edge.laplace import LaplacianFilter
from src.layer.edit_image import EditImage
from src.layer.equalize_hist import EqualizeHist
from src.layer.morphology import Morphology
from src.layer.threshold import DoubleThreshold
from src.layer.upload_image import _decode
from src.server import SECURITY_HEADERS, SecurityMiddleware


IMAGE_CONF = {
    'types': ['bmp', 'jpeg', 'jpg', 'png'],
    'max_size_mb': 1,
    'max_megapixels': 1,
    'max_side_px': 1024,
    'target_side_px': 256,
}


def encode_image(image: Image.Image, image_format: str = 'PNG') -> bytes:
    output = BytesIO()
    image.save(output, format=image_format)
    return output.getvalue()


def test_decode_rejects_oversized_file_before_parsing(monkeypatch):
    errors = []
    monkeypatch.setattr('src.layer.upload_image.st.error', errors.append)

    result = _decode(b'x' * (1024 * 1024 + 1), IMAGE_CONF)

    assert result is None
    assert errors == ['File is too large. Limit is 1 MB.']


def test_decode_uses_content_format_allowlist(monkeypatch):
    errors = []
    monkeypatch.setattr('src.layer.upload_image.st.error', errors.append)
    gif = encode_image(Image.new('RGB', (8, 8)), 'GIF')

    assert _decode(gif, IMAGE_CONF) is None
    assert errors == ['Could not read that file as an image.']


def test_decode_rejects_dimensions_before_full_decode(monkeypatch):
    errors = []
    monkeypatch.setattr('src.layer.upload_image.st.error', errors.append)
    conf = {**IMAGE_CONF, 'max_side_px': 16}
    png = encode_image(Image.new('RGB', (32, 8)))

    assert _decode(png, conf) is None
    assert errors[0].startswith('Image is too large (32x8).')


def test_decode_normalizes_mode_and_bounds_output():
    png = encode_image(Image.new('RGBA', (512, 128), (1, 2, 3, 4)))

    result = _decode(png, IMAGE_CONF)

    assert result.dtype == np.uint8
    assert result.shape == (64, 256, 3)


def test_contours_bound_working_image_before_allocation(monkeypatch):
    seen_shapes = []

    def fake_find_contours(image):
        seen_shapes.append(image.shape)
        return []

    monkeypatch.setattr(contours_module, 'find_contours', fake_find_contours)
    image = np.indices((2048, 1024)).sum(axis=0).astype(np.uint8)

    layer = contours_module.FindContours(image)

    assert seen_shapes == [(512, 256)]
    assert layer.contour_scale == (4.0, 4.0)


def test_unknown_selectbox_values_fall_back():
    gray_image = np.arange(100, dtype=np.uint8).reshape(10, 10)
    equalize = EqualizeHist(gray_image)
    equalize.ui_params['option_idx'] = 'attacker-controlled'
    equalize.evaluate()

    morphology = Morphology(gray_image)
    morphology.ui_params['operation'] = 'attacker-controlled'
    morphology.ui_params['shape'] = 'attacker-controlled'
    morphology.evaluate()

    assert equalize.ui_params['option_idx'] == 0
    assert morphology.ui_params['operation'] == 'open'
    assert morphology.ui_params['shape'] == 'rect'


def test_client_controlled_numeric_values_are_bounded():
    gray_image = np.arange(100, dtype=np.uint8).reshape(10, 10)

    kernels = [
        (BoxFilter(gray_image), 1_000_001),
        (GaussianFilter(gray_image), 4),
        (MedianFilter(gray_image), -1),
        (LaplacianFilter(gray_image), True),
        (EqualizeHist(gray_image), float('inf')),
    ]
    for layer, value in kernels:
        layer.ui_params['kernel_size'] = value
        layer.evaluate()
        assert layer.ui_params['kernel_size'] == 3

    morphology = Morphology(gray_image)
    morphology.ui_params.update(kernel_size=2, n_iterations=1_000_000)
    morphology.evaluate()
    assert morphology.ui_params['kernel_size'] == 3
    assert morphology.ui_params['n_iterations'] == 1

    canny = Canny(gray_image)
    canny.ui_params.update(sigma=float('nan'), threshold=(0.8, 0.2))
    canny.evaluate()
    assert canny.ui_params['sigma'] == 1.0
    assert canny.ui_params['threshold'] == (0.1, 0.2)

    edit = EditImage(gray_image)
    edit.ui_params.update(contrast=float('inf'), brightness=True, gamma=-1)
    edit.evaluate()
    assert edit.ui_params == {'contrast': 1.0, 'brightness': 0, 'gamma': 1.0}

    threshold = DoubleThreshold(gray_image)
    threshold.ui_params.update(intensity='invalid', mask=1)
    threshold.evaluate()
    assert threshold.ui_params['intensity'] == (0, 255)
    assert threshold.ui_params['mask'] is False


def test_security_middleware_blocks_metrics():
    messages = []

    async def unreachable_app(scope, receive, send):
        raise AssertionError('Metrics request reached the Streamlit app')

    async def receive():
        return {'type': 'http.request', 'body': b'', 'more_body': False}

    async def send(message):
        messages.append(message)

    scope = {'type': 'http', 'method': 'GET', 'path': '/_stcore/metrics'}
    asyncio.run(SecurityMiddleware(unreachable_app)(scope, receive, send))

    assert messages[0]['status'] == 404


def test_security_middleware_adds_headers():
    messages = []

    async def app(scope, receive, send):
        await send({'type': 'http.response.start', 'status': 200, 'headers': []})
        await send({'type': 'http.response.body', 'body': b'ok'})

    async def receive():
        return {'type': 'http.request', 'body': b'', 'more_body': False}

    async def send(message):
        messages.append(message)

    scope = {'type': 'http', 'method': 'GET', 'path': '/'}
    asyncio.run(SecurityMiddleware(app)(scope, receive, send))

    assert set(SECURITY_HEADERS).issubset(set(messages[0]['headers']))
