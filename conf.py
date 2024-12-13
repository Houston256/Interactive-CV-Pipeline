import tomllib

import streamlit as st


@st.cache_resource
def load_toml():
    return tomllib.load("config.toml")
