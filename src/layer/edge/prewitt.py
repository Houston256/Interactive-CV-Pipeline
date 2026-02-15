import numpy as np
import streamlit as st
from skimage.filters import prewitt

from src.layer.layer import Layer


class Prewitt(Layer):
    def __init__(self, image: np.ndarray):
        super().__init__()

        self.prepare_ui()

        self.set_image(image)

    def evaluate(self):
        self.img_out = np.empty_like(self.img_in)

        self.img_out = prewitt(
            image=self.img_in,
        )

        self.img_out *= 255
        self.img_out = self.img_out.astype(np.uint8)
        return self

    def interact(self):
        self.set_image(self.img_in)

        st.image(self.img_out, width="stretch")

        return self

    def __str__(self):
        return 'Prewitt Edge Detector'
