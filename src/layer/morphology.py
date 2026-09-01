import cv2
import numpy as np
import streamlit as st

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
        kernel_size = self.bounded_int('kernel_size', 3, 3, 19, odd=True)
        shape = self.ui_params.get('shape')
        if shape not in self.shapes:
            shape = 'rect'
            self.ui_params['shape'] = shape
        return cv2.getStructuringElement(self.shapes[shape],
                                         (kernel_size, kernel_size))

    def evaluate(self):
        iterations = self.bounded_int('n_iterations', 1, 1, 30)
        operation = self.ui_params.get('operation')
        if operation not in self.operations:
            operation = 'open'
            self.ui_params['operation'] = operation
        self.img_out = cv2.morphologyEx(
            self.img_in,
            op=self.operations[operation],
            kernel=self.get_structuring_element(),
            iterations=iterations
        )
        return self

    def interact(self):
        from matplotlib.figure import Figure

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

        fig = Figure()
        ax = fig.subplots()
        element = self.get_structuring_element()
        ax.imshow(element, cmap='gray', vmin=0, vmax=1)
        for row, column in np.ndindex(element.shape):
            ax.text(column, row, str(element[row, column]), ha='center', va='center')
        ax.set_title('Structuring Element')
        ax.axis('off')
        right.pyplot(fig)

        self.set_image(self.img_in)

        st.image(self.img_out)

        return self

    def __str__(self):
        return f'Morphology'
