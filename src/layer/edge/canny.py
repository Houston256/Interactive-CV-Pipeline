import cv2
import numpy as np
import streamlit as st
from skimage.feature import canny

from src.layer.layer import Layer


class Canny(Layer):
    def __init__(self, image: np.ndarray):
        super().__init__()
        self.ui_params['sigma'] = 1.
        self.ui_params['threshold'] = (.1, .2)

        self.prepare_ui()

        self.set_image(image)

    def evaluate(self):
        if self.img_in.ndim == 3:
            self.img_out = cv2.cvtColor(self.img_in, cv2.COLOR_RGB2GRAY)
        else:
            self.img_out = self.img_in.copy()

        self.img_out = canny(
            image=self.img_out,
            sigma=self.ui_params['sigma'],
            low_threshold=self.ui_params['threshold'][0],
            high_threshold=self.ui_params['threshold'][1]
        )
        self.img_out = self.img_out.astype(np.uint8) * 255
        return self

    def interact(self):
        if self.img_in.ndim == 3:
            st.info('Input image implicitly converted to grayscale.')

        st.slider(
            label='Threshold',
            key='threshold',
            min_value=0.,
            max_value=1.,
            step=0.01,
            help='Good values to start with are 0.1-0.2',
            on_change=self.changed,
        )

        st.slider(
            label='Sigma',
            min_value=0.,
            max_value=100.,
            step=0.05,
            on_change=self.changed,
            key='sigma',
            help='Standard deviation of the Gaussian filter',
        )

        self.set_image(self.img_in)

        st.image(self.img_out, use_column_width='always')

        return self

    def __str__(self):
        return 'Canny Edge Detector'
