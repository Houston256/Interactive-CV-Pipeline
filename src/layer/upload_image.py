import io

import numpy as np
import streamlit as st
from PIL import Image, ImageOps, UnidentifiedImageError

from src.layer.layer import Layer

# Pillow only raises above 2x this value. The real check is in _decode.
Image.MAX_IMAGE_PIXELS = 40_000_000


def _allowed_formats(extensions) -> list:
    """Map the configured extensions to the Pillow format names they decode to."""
    registered = Image.registered_extensions()
    return sorted({registered[e] for t in extensions if (e := '.' + t.lower()) in registered})


def _decode(data: bytes, conf: dict) -> np.ndarray | None:
    """
    Turn uploaded bytes into a bounded uint8 RGB or grayscale array.

    Returns None and shows an error if the file is not an acceptable image.
    """
    if len(data) > conf['max_size_mb'] * 1024 * 1024:
        st.error(f"File is too large. Limit is {conf['max_size_mb']} MB.")
        return None

    allowed = _allowed_formats(conf['types'])
    try:
        # formats= limits which Pillow plugins get to parse the header. Without
        # it every registered plugin's _open() is tried in turn.
        # open() reads the header only, no pixels are decoded yet.
        img = Image.open(io.BytesIO(data), formats=allowed)

        if img.format not in allowed:
            st.error(f"Unsupported image format: {img.format}. Allowed: {', '.join(allowed)}.")
            return None

        if getattr(img, 'n_frames', 1) > 1:
            st.error('Multi-frame images are not supported.')
            return None

        width, height = img.size
        if max(width, height) > conf['max_side_px'] or width * height > conf['max_megapixels'] * 1_000_000:
            st.error(
                f'Image is too large ({width}x{height}). '
                f"Limit is {conf['max_side_px']} px per side and {conf['max_megapixels']} MP."
            )
            return None

        # Decodes JPEG at reduced scale. No-op for other formats.
        img.draft('RGB', (conf['target_side_px'], conf['target_side_px']))

        img = ImageOps.exif_transpose(img)
        # Layers expect 2D grayscale or 3-channel RGB uint8.
        if img.mode not in ('L', 'RGB'):
            img = img.convert('RGB')
        img.thumbnail((conf['target_side_px'], conf['target_side_px']), Image.Resampling.LANCZOS)

        return np.asarray(img)
    except (UnidentifiedImageError, Image.DecompressionBombError, OSError, ValueError, MemoryError):
        st.error('Could not read that file as an image.')
        return None


class UploadImage(Layer):
    def interact(self):
        uploaded = st.file_uploader("Choose an image",
                                    type=st.session_state.conf['image']['types'],
                                    accept_multiple_files=False,
                                    key='image_upload')
        # don't do anything if no image is selected
        if uploaded is not None:
            decoded = _decode(uploaded.getvalue(), st.session_state.conf['image'])
            if decoded is not None:
                self.img_out = decoded
        if self.img_out is not None:
            st.image(self.img_out)
        return self

    def evaluate(self):
        self.img_out = self.img_in.copy()
        return self

    def __str__(self):
        return 'Upload Image'
