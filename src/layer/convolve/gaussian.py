import cv2
import numpy as np
import streamlit as st

from src.layer.convolve.convolve import Convolve


class GaussianFilter(Convolve):
    def __init__(self, image: np.ndarray):
        super().__init__()

        self.prepare_ui()

        self.set_image(image)

    def evaluate(self):
        self.img_out = self.img_in.copy()

        self.img_out = cv2.GaussianBlur(self.img_out,
                                        ksize=(self.ui_params['kernel_size'], self.ui_params['kernel_size']),
                                        sigmaX=0)

        return self

    def interact(self):
        super().interact()

        self.set_image(self.img_in)

        st.image(self.img_out)
        return self

    def get_img(self) -> np.ndarray:
        return self.img_out

    def __str__(self):
        return 'Gaussian Filter'
