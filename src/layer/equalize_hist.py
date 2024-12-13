"""
This module contains the EqualizeHist class which is used for histogram equalization of images.
"""
import cv2
import numpy as np
import streamlit as st

from src.layer.layer import Layer
from src.utils.helpers import draw_histogram


class EqualizeHist(Layer):
    """
    The EqualizeHist class inherits from the Layer class and is used for histogram equalization of images.
    It provides two types of histogram equalization: standard and Contrast Limited Adaptive Histogram Equalization (CLAHE).

    https://docs.opencv.org/4.x/d5/daf/tutorial_py_histogram_equalization.html
    """

    def __init__(self, image: np.ndarray):
        """
        Initialize EqualizeHist object with an image and default UI parameters.
        :param image: initialize with this
        """
        super().__init__()
        self.ui_params['kernel_size'] = 3
        self.ui_params['option_idx'] = 0

        self.options = [
            'Contrast Limited Adaptive Histogram Equalization (CLAHE)',
            'Histogram Equalization',
        ]

        self.prepare_ui()

        self.set_image(image)

    def evaluate(self):
        """
        Apply the selected histogram equalization method to the image.
        """
        key = self.ui_params['option_idx']
        key = self.options[key]

        self.img_out = self.img_in.copy()

        clahe = cv2.createCLAHE(clipLimit=2.0,
                                tileGridSize=tuple(2 * [self.ui_params['kernel_size']]))
        # grayscale image
        if self.img_in.ndim == 2:
            if key == 'Histogram Equalization':
                self.img_out = cv2.equalizeHist(self.img_out)
            else:
                clahe.apply(self.img_out, self.img_out)
        # color image
        else:
            # image needs to be converted to YCrCb colorspace. If applied to RGB, the result is not as expected.
            # https://stackoverflow.com/questions/15007304/histogram-equalization-not-working-on-color-image-opencv
            # https://stackoverflow.com/questions/31998428/opencv-python-equalizehist-colored-image
            cv2.cvtColor(self.img_out, cv2.COLOR_RGB2YCR_CB, dst=self.img_out)
            # here, we only apply the histogram equalization to the first channel
            if key == 'Histogram Equalization':
                self.img_out[:, :, 0] = cv2.equalizeHist(self.img_out[:, :, 0])
            else:
                self.img_out[:, :, 0] = clahe.apply(self.img_out[:, :, 0])

            # convert back to RGB
            cv2.cvtColor(self.img_out, cv2.COLOR_YCR_CB2RGB, dst=self.img_out)

        return self

    def interact(self):
        st.selectbox('Select HE type',
                     options=range(len(self.options)),
                     format_func=lambda x: self.options[x],
                     on_change=self.changed,
                     key='option_idx', )

        if self.ui_params['option_idx'] == 0:
            st.session_state.kernel_size = self.ui_params['kernel_size']
            st.slider('Kernel Size',
                      min_value=3,
                      max_value=15,
                      step=2,
                      on_change=self.changed,
                      key='kernel_size',
                      help='Size of the kernel for CLAHE'
                      )

        self.set_image(self.img_in)

        st.image(self.img_out)

        with st.expander('Image Histogram'):
            draw_histogram(self.img_out)

        return self

    def __str__(self):
        return 'Equalize Histogram'
