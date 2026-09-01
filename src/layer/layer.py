from abc import ABC, abstractmethod
from math import isfinite

import numpy as np
import streamlit as st


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

    def bounded_int(self, key: str, default: int, minimum: int, maximum: int, *, odd: bool = False) -> int:
        value = self.ui_params.get(key)
        if type(value) is not int or not minimum <= value <= maximum or (odd and value % 2 == 0):
            value = default
            self.ui_params[key] = value
        return value

    def bounded_float(self, key: str, default: float, minimum: float, maximum: float) -> float:
        value = self.ui_params.get(key)
        if (
            isinstance(value, bool)
            or not isinstance(value, (int, float))
            or not isfinite(value)
            or not minimum <= value <= maximum
        ):
            value = default
            self.ui_params[key] = value
        return float(value)

    def bounded_range(self, key: str, default: tuple, minimum: float, maximum: float) -> tuple:
        value = self.ui_params.get(key)
        valid = isinstance(value, (list, tuple)) and len(value) == 2
        if valid:
            low, high = value
            valid = all(
                not isinstance(item, bool) and isinstance(item, (int, float)) and isfinite(item)
                for item in (low, high)
            ) and minimum <= low <= high <= maximum
        if not valid:
            value = default
            self.ui_params[key] = value
        return tuple(value)

    def bounded_bool(self, key: str, default: bool) -> bool:
        value = self.ui_params.get(key)
        if type(value) is not bool:
            value = default
            self.ui_params[key] = value
        return value

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
        input_column, output_column = st.columns(2)
        input_column.caption('Input')
        input_column.image(self.img_in)
        output_column.caption('Output')
        output_column.image(self.img_out)

    @abstractmethod
    def __str__(self) -> str:
        """
        Name of Layer used for UI
        """
        raise NotImplementedError
