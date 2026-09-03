import streamlit as st
import pandas as pd
import time
# 상태 초기화
# if 'counter' not in st.session_state:
#     st.session_state['counter'] = 0

# if st.button('Increment'):
#     st.session_state['counter'] += 1

# if st.button('초기화'):
#     st.session_state['counter'] = 0

# counter = st.session_state['counter']
# st.write(f'카운터: {counter}')

start_time = time.time()

@st.cache_data
def load_data(parameter: int):
    df = pd.read_csv('2019-Oct-small.csv')
    return df


v = st.number_input('파라미터 입력 - 캐시 깨짐', 0, 100)
st.slider('볼륨', 0, 10, step=1)
st.text_input('아이디')

data = load_data(v)
st.dataframe(data.head())

elapsed = time.time() - start_time

st.write(f'소요시간: {elapsed}')

st.write('캐시 데이터 적용')
st.write('파라미터를 주면 캐싱이 구분됨')
