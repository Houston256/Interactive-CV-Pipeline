import streamlit as st

from src.sequential.sequential import Sequential
from src.utils.helpers import cache_config

if __name__ == "__main__":
    cache_config()

    if 'seq' not in st.session_state:
        st.session_state['seq'] = Sequential()

    st.session_state.seq.interact()
