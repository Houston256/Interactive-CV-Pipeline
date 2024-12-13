import cv2
import numpy as np
import streamlit as st

from src.layer.layer import Layer
from src.utils.helpers import draw_histogram


class BoxFilter(Layer):
    def __init__(self, image: np.ndarray):
        """
        Initialize EqualizeHist object with an image and default UI parameters.
        :param image: initialize with this
        """
        super().__init__()
        self.ui_params['kernel_size'] = 3

        self.prepare_ui()

        self.set_image(image)

    def evaluate(self):
        self.img_out = self.img_in.copy()

        kernel = np.ones((self.ui_params['kernel_size'], self.ui_params['kernel_size']), np.float32) / (
                    self.ui_params['kernel_size'] ** 2)

        self.img_out = cv2.filter2D(self.img_out, -1, kernel)

        return self

    def interact(self):
        st.session_state.kernel_size = self.ui_params['kernel_size']
        st.slider('Kernel Size',
                  min_value=3,
                  max_value=15,
                  step=2,
                  on_change=self.changed,
                  key='kernel_size',
                  help='Size of the kernel for Box filter'
                  )

        self.set_image(self.img_in)

        st.image(self.img_out)

        with st.expander('Image Histogram'):
            draw_histogram(self.img_out)
        return self

    def get_img(self) -> np.ndarray:
        return self.img_out

    def __str__(self):
        return 'Box Filter'
