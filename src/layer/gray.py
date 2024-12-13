import cv2
import numpy as np
import streamlit as st

from src.layer.layer import Layer


class ToGrayscale(Layer):
    def __init__(self, image: np.ndarray):
        super().__init__()
        self.ui_params['kernel_size'] = 3

        self.prepare_ui()

        self.set_image(image)

    def evaluate(self):
        self.img_out = self.img_in.copy()

        if len(self.img_out.shape) == 3:
            self.img_out = cv2.cvtColor(self.img_out, cv2.COLOR_RGB2GRAY)

        return self

    def interact(self):
        self.set_image(self.img_in)

        st.image(self.img_out)

        return self

    def __str__(self):
        return 'Convert To Grayscale'
