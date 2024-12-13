import cv2
import numpy as np
import seaborn as sns
import streamlit as st
from matplotlib import pyplot as plt

from src.layer.layer import Layer


class Morphology(Layer):
    def __init__(self, image: np.ndarray):
        super().__init__()
        self.ui_params['kernel_size'] = 3
        self.ui_params['n_iterations'] = 1

        self.ui_params['shape'] = 'rect'
        self.shapes = {
            'rect': cv2.MORPH_RECT,
            'ellipse': cv2.MORPH_ELLIPSE,
            'cross': cv2.MORPH_CROSS,
        }

        self.ui_params['operation'] = 'open'
        self.operations = {
            'erode': cv2.MORPH_ERODE,
            'dilate': cv2.MORPH_DILATE,
            'open': cv2.MORPH_OPEN,
            'close': cv2.MORPH_CLOSE,
            'gradient': cv2.MORPH_GRADIENT,
            'top hat': cv2.MORPH_TOPHAT,
            'black hat': cv2.MORPH_BLACKHAT,
        }

        self.prepare_ui()

        self.set_image(image)

    def get_structuring_element(self):
        return cv2.getStructuringElement(self.shapes[self.ui_params['shape']],
                                         (self.ui_params['kernel_size'], self.ui_params['kernel_size']))

    def evaluate(self):
        self.img_out = cv2.morphologyEx(
            self.img_in,
            op=self.operations[self.ui_params['operation']],
            kernel=self.get_structuring_element(),
            iterations=self.ui_params['n_iterations']
        )
        return self

    def interact(self):
        if self.img_in.ndim == 3:
            st.info('Morphology operations will be applied to each channel separately.')

        left, right = st.columns(2)

        left.selectbox(
            label='Morphology Operation',
            options=list(self.operations.keys()),
            key='operation',
            on_change=self.changed
        )

        left.selectbox(
            label='Structuring Element Shape',
            options=list(self.shapes.keys()),
            key='shape',
            on_change=self.changed
        )

        left.slider(
            label='Kernel Size',
            min_value=3,
            max_value=19,
            step=2,
            on_change=self.changed,
            key='kernel_size',
            help='Size of the structuring element'
        )

        left.number_input(
            label='Number of Iterations',
            min_value=1,
            max_value=30,
            key='n_iterations',
            on_change=self.changed
        )

        fig, ax = plt.subplots()
        sns.heatmap(self.get_structuring_element(), ax=ax, annot=True, cbar=False, square=True)
        ax.set_title('Structuring Element')
        ax.axis('off')
        right.write(fig)

        self.set_image(self.img_in)

        st.image(self.img_out)

        return self

    def __str__(self):
        return f'Morphology'
