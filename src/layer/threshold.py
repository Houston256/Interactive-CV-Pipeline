import cv2
import numpy as np
import streamlit as st

from src.layer.layer import Layer


class DoubleThreshold(Layer):
    def __init__(self, image: np.ndarray):
        super().__init__()

        # grayscale
        self.ui_params['intensity'] = (0, 255)
        self.ui_params['hue'] = (0, 360)
        self.ui_params['saturation'] = (0, 255)
        self.ui_params['value'] = (0, 255)
        self.ui_params['mask'] = False

        self.prepare_ui()

        self.set_image(image)

    def evaluate(self):
        # grayscale
        if self.img_in.ndim == 2:
            mask = cv2.inRange(self.img_in, *self.ui_params['intensity'])
        # color
        else:
            # convert to hsv
            hsv = cv2.cvtColor(self.img_in, cv2.COLOR_RGB2HSV)
            # construct lowebound and upperbound
            lbound = []
            ubound = []
            for k in ['hue', 'saturation', 'value']:
                lbound += [self.ui_params[k][0]]
                ubound += [self.ui_params[k][1]]
            lbound = np.array(lbound)
            ubound = np.array(ubound)
            # threshold
            mask = cv2.inRange(hsv, lbound, ubound)
        # apply mask to image
        if self.ui_params['mask']:
            if self.img_in.ndim == 3:
                # mask has to be 3 channel
                mask = cv2.merge(3 * [mask])
            # apply mask
            self.img_out = cv2.bitwise_and(self.img_in, mask)
        # only display mask
        else:
            self.img_out = mask
        return self

    def interact(self):
        self.prepare_ui()  # sliders streamlit removes sliders from session
        if self.img_in.ndim == 2:
            st.slider(
                label='Intensity',
                key='intensity',
                min_value=0,
                max_value=255,
                on_change=self.changed
            )
        else:
            st.slider(
                label='Hue',
                key='hue',
                min_value=0,
                max_value=360,
                on_change=self.changed
            )
            st.slider(
                label='Saturation',
                key='saturation',
                min_value=0,
                max_value=255,
                on_change=self.changed
            )
            st.slider(
                label='Value',
                key='value',
                min_value=0,
                max_value=255,
                on_change=self.changed
            )
        st.checkbox(
            'Display masked image',
            key='mask',
            on_change=self.changed
        )

        st.image(self.img_out)
        return self

    def __str__(self) -> str:
        return "Double Threshold"
