import cv2
import numpy as np
import streamlit as st

from src.layer.convolve.convolve import Convolve


class MedianFilter(Convolve):
    def __init__(self, image: np.ndarray):
        super().__init__()

        self.prepare_ui()

        self.set_image(image)

    def evaluate(self):
        self.img_out = self.img_in.copy()
        self.img_out = cv2.medianBlur(self.img_out, self.ui_params['kernel_size'])
        return self

    def interact(self):
        super().interact()

        self.set_image(self.img_in)

        st.image(self.img_out)
        return self

    def __str__(self):
        return 'Median Blur'
