"""
Module that defines the Sequential class, which is a class that
represents a sequence of image processing layers.
"""
import numpy as np
import streamlit as st

from src.layer.upload_image import UploadImage
from src.layer_factory.layer_factory import LayerFactory


class Sequential:
    """
    The Sequential class is used to manage a sequence of image processing layers.
    """

    def __init__(self):
        """
        Initialize the Sequential object with default parameters and an UploadImage layer.
        """
        self.remove_last_active = False
        self.layers = [UploadImage()]
        self.layer_idx_default = 0
        self.factory = LayerFactory()

    def add_layer(self, layer):
        """
        Add a new layer to the sequence. The new layer is initialized with the output image of the previous layers.
        """
        if self.get_img() is None:
            st.sidebar.error('Pipeline yields None. Did you forget to upload an image?')
            return self
        layer = layer(self.get_img())
        self.layers.append(layer)
        st.session_state.layer_idx = len(self.layers) - 1
        self.change_layer().set_remove_last()
        return self

    def evaluate(self) -> np.ndarray:
        """
        Evaluate the sequence of layers and return the output image of the last layer.
        """
        if len(self.layers) == 1:
            return self.get_img()
        for i in range(1, len(self.layers)):
            prev_img = self.layers[i - 1].get_img()
            self.layers[i].set_image(prev_img)
        return self.get_img()

    def prepare_ui(self):
        """
        Prepare the UI for the Sequential object by setting the default UI parameters.
        """
        self.layer_idx_default = st.session_state.layer_idx
        return self

    def get_img(self) -> np.ndarray:
        """
        Return the output image of the last layer in the sequence.
        """
        return self.layers[-1].get_img()

    def set_remove_last(self):
        """
        Set the remove_last_active attribute based on the number of layers in the sequence.
        """
        self.remove_last_active = len(self.layers) > 1
        return self

    def change_layer(self):
        """
        Update the UI parameters when user switches between layers.
        """
        self.layer_idx_default = st.session_state.layer_idx
        self.layers[st.session_state.layer_idx].prepare_ui()
        self.prepare_ui()
        return self

    def remove_last(self):
        """
        Remove the last layer in the sequence.
        """
        if len(self.layers) == 1:
            st.sidebar.error('Cannot remove Upload Image layer.')
            return self

        self.layers.pop()

        self.layer_idx_default = min(self.layer_idx_default, len(self.layers) - 1)
        st.session_state.layer_idx = self.layer_idx_default
        self.set_remove_last().change_layer().prepare_ui()
        return self

    def interact(self):
        """
        Create the UI for the Sequential object.
        """
        st.sidebar.title('Image Processing Pipeline')

        st.title(str(self.layers[self.layer_idx_default]))

        st.sidebar.radio(
            label="Layers",
            options=range(len(self.layers)),
            format_func=lambda x: str(self.layers[x]),
            on_change=self.change_layer,
            key='layer_idx',
        )

        self.evaluate()

        col_add, col_remove = st.sidebar.columns(2)

        pop = col_add.popover('Add Layer')

        selected_layer = pop.selectbox(
            label="Select layer to add",
            options=self.factory.get_layer_names(),
            key='layer_select',
        )
        layer = self.factory.get_layer(selected_layer)

        pop.button('Add',
                   on_click=self.add_layer,
                   args=[layer])

        col_remove.button('Remove Last',
                          on_click=self.remove_last,
                          disabled=not self.remove_last_active,
                          help='Cannot remove Upload Image layer.' if not self.remove_last_active else None
                          )

        self.evaluate()

        self.layers[st.session_state.layer_idx].interact()
