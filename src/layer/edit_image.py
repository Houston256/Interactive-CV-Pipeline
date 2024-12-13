"""
This module contains the EditImage class, which is a subclass of the Layer class.
It allows the user to adjust the brightness, contrast, and gamma of an image.
"""
import cv2
import streamlit as st
from skimage.exposure import adjust_gamma

from src.layer.layer import Layer
from src.utils.helpers import draw_histogram


class EditImage(Layer):
    """
    EditImage class allows the user to adjust the brightness, contrast, and gamma of an image.
    """

    def __init__(self, image):
        super().__init__()

        self.ui_params['contrast'] = 1.0
        self.ui_params['brightness'] = 0
        self.ui_params['gamma'] = 1.0

        self.prepare_ui()
        self.set_image(image)

    def evaluate(self):
        self.img_out = cv2.convertScaleAbs(self.img_in,
                                           alpha=self.ui_params['contrast'],
                                           beta=self.ui_params['brightness'])

        self.img_out = adjust_gamma(self.img_out, gamma=self.ui_params['gamma'])
        return self

    def interact(self):
        st.slider('Contrast',
                  min_value=0.0,
                  max_value=2.0,
                  # value=self.ui_params_def['contrast'],
                  step=0.1,
                  on_change=self.changed,
                  key='contrast')

        st.slider('Brightness',
                  min_value=0,
                  max_value=100,
                  step=1,
                  on_change=self.changed,
                  key='brightness')

        st.slider('Gamma',
                  min_value=0.,
                  max_value=2.0,
                  step=0.01,
                  on_change=self.changed,
                  key='gamma')

        self.set_image(self.img_in)

        st.image(self.img_out)

        with st.expander('Image Histogram'):
            draw_histogram(self.img_out)

        return self

    def __str__(self):
        return 'Edit Image'
