import numpy as np
import streamlit as st
import toml
from matplotlib import pyplot as plt


def cache_config():
    if 'conf' not in st.session_state:
        st.session_state['conf'] = toml.load("config.toml")


def draw_histogram(image: np.ndarray):
    arr = image.ravel()
    fig, ax = plt.subplots()
    ax.hist(arr, bins=100)
    st.pyplot(fig)
