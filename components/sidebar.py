import streamlit as st

def render():
    with st.sidebar:
        st.title('사이드바 항목')

        if st.button('홈'):
            st.session_state['page'] = 0

        if st.button('About'):
            st.session_state['page'] = 1

    page = 0
    return page
