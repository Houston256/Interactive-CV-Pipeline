import cv2
import numpy as np
import streamlit as st
from matplotlib import pyplot as plt
from skimage.measure import find_contours

from src.layer.layer import Layer


class FindContours(Layer):
    """
    A pass-through layer that finds contours in a binary image.
    Passthrough means, that the input image is returned mostly as is. (except for the conversion to grayscale and binary)
    """

    def __init__(self, image: np.ndarray):
        super().__init__()

        self.prepare_ui()

        self.contours = None

        self.set_image(image)

    def evaluate(self):
        self.img_out = self.img_in.copy()
        # handle color image
        if self.img_out.ndim == 3:
            self.img_out = cv2.cvtColor(self.img_out, cv2.COLOR_RGB2GRAY)
        # make binary
        self.img_out = ((self.img_out > self.img_out.mean()) * 255).astype(np.uint8)

        # find contours
        self.contours = find_contours(self.img_out)
        return self

    def interact(self):
        self.set_image(self.img_in)

        if self.img_in.ndim == 3:
            st.info('Input image implicitly converted to grayscale.')

        if len(np.unique(self.img_in)) > 2:
            st.info('Input image implicitly converted to binary.')

        # https://scikit-image.org/docs/stable/auto_examples/edges/plot_contours.html#sphx-glr-auto-examples-edges-plot-contours-py
        fig, ax = plt.subplots()
        ax.imshow(self.img_out, cmap=plt.cm.gray)
        for contour in self.contours:
            ax.plot(contour[:, 1], contour[:, 0], linewidth=2)

        ax.axis('image')
        ax.set_xticks([])
        ax.set_yticks([])
        st.pyplot(fig)
        return self

    def __str__(self) -> str:
        return "Find Contours"

    @classmethod
    def class_str(cls):
        return 'Find Contours'
