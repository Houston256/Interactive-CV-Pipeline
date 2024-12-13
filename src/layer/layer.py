from abc import ABC, abstractmethod

import numpy as np
import streamlit as st
from streamlit_image_comparison import image_comparison


class Layer(ABC):
    def __init__(self):
        self.is_changed = True
        self.img_in = None
        self.img_out = None
        self.ui_params = {}

    def changed(self):
        """
        Set the flag to indicate that the layer has changed
        example: when a slider is moved, the layer needs to be recomputed.
        if nothing changes, there is no need to recompute.
        """
        self.is_changed = True

        for k in self.ui_params:
            if k not in st.session_state.keys():
                continue
            self.ui_params[k] = st.session_state[k]

    def get_img(self) -> np.ndarray:
        return self.img_out

    @abstractmethod
    def evaluate(self):
        """
        Recomputes self.img_out from self.img_in
        """
        raise NotImplementedError

    def set_image(self, image: np.ndarray):
        """
        Recomputes calls evaluate if needed
        """
        if image is None:
            raise UserWarning("Setting image as None")

        if self.img_in is None or not np.array_equal(image, self.img_in):
            self.img_in = image.copy()
            self.is_changed = True

        if self.is_changed:
            self.evaluate()
            self.is_changed = False

        return self

    def prepare_ui(self):
        """
        Call before first render

        You should set the default values of selectors/sliders here.
        """
        for k in self.ui_params:
            st.session_state[k] = self.ui_params[k]
        return self

    @abstractmethod
    def interact(self):
        """
        Renders the layer's UI
        
        For your own sanity,
        DON'T CHANGE PARAMETERS OF SLIDERS DURING THEIR LIFETIME,
        their cache would be invalidated and the sliders become janky.
        """
        raise NotImplementedError

    def show_difference(self):
        """
        Show the difference between input and output image
        """
        if self.img_out is None or self.img_in is None:
            st.error('Input or Output image is None')
            return
        image_comparison(self.img_in, self.img_out, label1='Input', label2='Output')

    @abstractmethod
    def __str__(self) -> str:
        """
        Name of Layer used for UI
        """
        raise NotImplementedError
