import numpy as np
import streamlit as st
from PIL import Image

from src.layer.layer import Layer


class UploadImage(Layer):
    def interact(self):
        uploaded = st.file_uploader("Choose an image",
                                    type=st.session_state.conf['image']['types'],
                                    key='image_upload')
        # don't do anything if no image is selected
        if uploaded is not None:
            self.img_out = np.asarray(Image.open(uploaded))
        if self.img_out is not None:
            st.image(self.img_out)
        return self

    def evaluate(self):
        self.img_out = self.img_in.copy()
        return self

    def __str__(self):
        return 'Upload Image'
