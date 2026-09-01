from heapq import nlargest

import cv2
import numpy as np
import streamlit as st
from skimage.measure import find_contours

from src.layer.layer import Layer

# Max contours drawn. A noise image produces hundreds of thousands.
MAX_CONTOURS = 2000
# Bound the marching-squares working set before contours are allocated.
MAX_CONTOUR_SIDE_PX = 512


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

        height, width = self.img_out.shape
        if max(height, width) > MAX_CONTOUR_SIDE_PX:
            ratio = MAX_CONTOUR_SIDE_PX / max(height, width)
            contour_image = cv2.resize(
                self.img_out,
                (max(1, round(width * ratio)), max(1, round(height * ratio))),
                interpolation=cv2.INTER_NEAREST,
            )
        else:
            contour_image = self.img_out

        contour_height, contour_width = contour_image.shape
        self.contour_scale = (height / contour_height, width / contour_width)
        self.contours = find_contours(contour_image)
        return self

    def interact(self):
        from matplotlib.collections import LineCollection
        from matplotlib.figure import Figure

        self.set_image(self.img_in)

        if self.img_in.ndim == 3:
            st.info('Input image implicitly converted to grayscale.')

        sample = self.img_in.reshape(-1)[::max(1, self.img_in.size // 65536)]
        if len(np.unique(sample)) > 2:
            st.info('Input image implicitly converted to binary.')

        contours = self.contours
        if len(contours) > MAX_CONTOURS:
            st.info(f'Found {len(contours)} contours, drawing the {MAX_CONTOURS} largest.')
            contours = nlargest(MAX_CONTOURS, contours, key=len)

        # https://scikit-image.org/docs/stable/auto_examples/edges/plot_contours.html#sphx-glr-auto-examples-edges-plot-contours-py
        fig = Figure()
        ax = fig.subplots()
        ax.imshow(self.img_out, cmap='gray')
        # One collection, not one artist per contour.
        scale_y, scale_x = self.contour_scale
        segments = [c[:, ::-1] * (scale_x, scale_y) for c in contours]
        ax.add_collection(LineCollection(segments, linewidths=2))

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
