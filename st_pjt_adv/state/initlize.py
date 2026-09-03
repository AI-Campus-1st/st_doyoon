import streamlit as st

def initlize():
    if 'page' not in st.session_state:
        st.session_state['page'] = 0
