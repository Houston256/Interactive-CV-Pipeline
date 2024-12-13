from abc import abstractmethod, ABC

import streamlit as st

from src.layer.layer import Layer


class Convolve(Layer, ABC):
    """
    Abstract class for convolutional layers.
    """
    def __init__(self):
        super().__init__()
        self.ui_params['kernel_size'] = 3

    @abstractmethod
    def evaluate(self):
        """
        Evaluate the layer.
        :return: self
        """
        raise NotImplementedError

    @abstractmethod
    def interact(self):
        """
        Show slider for kernel size.
        :return: self
        """
        st.session_state.kernel_size = self.ui_params['kernel_size']
        st.slider('Kernel Size',
                  min_value=3,
                  max_value=15,
                  step=2,
                  on_change=self.changed,
                  key='kernel_size',
                  )
        return self

    @abstractmethod
    def __str__(self):
        raise NotImplementedError
