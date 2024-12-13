import cv2
import numpy as np
import streamlit as st

from src.layer.layer import Layer


class LaplacianFilter(Layer):
    def __init__(self, image: np.ndarray):
        super().__init__()
        self.ui_params['kernel_size'] = 3

        self.prepare_ui()

        self.set_image(image)

    def evaluate(self):
        self.img_out = self.img_in.copy()

        self.img_out = cv2.Laplacian(self.img_out, cv2.CV_64F, ksize=self.ui_params['kernel_size'])

        self.img_out *= 255


        self.img_out = np.clip(self.img_out, 0, 255)
        self.img_out = self.img_out.astype(np.uint8)

        return self

    def interact(self):
        st.session_state.kernel_size = self.ui_params['kernel_size']
        st.slider('Kernel Size',
                  min_value=3,
                  max_value=19,
                  step=2,
                  on_change=self.changed,
                  key='kernel_size',
                  help='Size of the kernel'
                  )

        self.set_image(self.img_in)

        st.image(self.img_out, use_column_width='always')

        return self

    def get_img(self) -> np.ndarray:
        return self.img_out

    def __str__(self):
        return 'Laplacian Filter'
