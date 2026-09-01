import tomllib

import numpy as np
import streamlit as st


def cache_config():
    if 'conf' not in st.session_state:
        with open('config.toml', 'rb') as config_file:
            st.session_state['conf'] = tomllib.load(config_file)


def draw_histogram(image: np.ndarray):
    # Figure() not plt.subplots(); pyplot never frees the figures it creates.
    from matplotlib.figure import Figure

    fig = Figure()
    ax = fig.subplots()
    ax.hist(image.ravel(), bins=100)
    st.pyplot(fig)
