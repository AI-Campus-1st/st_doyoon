import streamlit as st

def Button(name, value):
    if name not in st.session_state:
        st.session_state[name] = None

    if st.button(name):
        st.session_state[name] = value

    