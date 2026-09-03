import random
from sqlalchemy import create_engine, Table, Column, Integer, Float, String, MetaData, text
from datetime import datetime
import streamlit as st
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from streamlit_autorefresh import st_autorefresh
from dotenv import load_dotenv
import os

# 2번문제로 인해 바뀌어야할 부분은 주석으로 표시해 만들었습니다.

load_dotenv()

DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', 3306)),
    'user': os.getenv('DB_USER', 'analyst'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'stocks')
}

host = DB_CONFIG['host']
port = DB_CONFIG['port']
user = DB_CONFIG['user']
password = DB_CONFIG['password']
database = DB_CONFIG['database']

stocks = ["A", "B", "C", "D", "E"]
ids = [1, 2, 3, 4, 5]

# SQLite 데이터베이스 연결
#engine = create_engine(f'mysql+pymysql://{user}:{password}@{host}:{port}/tb_stock')
engine = create_engine('sqlite:///stocks.db')
metadata = MetaData()

# interval set
st_autorefresh(interval=1000)

# 테이블 정의
stocks_table = Table('stocks', metadata,
                     Column('id', Integer, primary_key=True),
                     Column('timestamp', String),
                     Column('price', Float),
                     Column('volume', Integer),
                     Column('stock_id', Integer))

stocks_name = Table('stocks_name', metadata,
                     Column('id', Integer, primary_key=True),
                     Column('name', String))

# 테이블 생성
metadata.create_all(engine)

def add_fake_stock_name_data():
    with engine.connect() as conn:
        # query = "SELECT COUNT(*) FROM tb_stock"
        query = "SELECT COUNT(*) FROM stocks_name"
        try:
            result = conn.execute(text(query))
            count = result.scalar()
        except Exception as e:
            print(f"Error executing query: {e}")
            count = 0
        if count == 5:
            return 5 
        for stock in stocks:
            conn.execute(stocks_name.insert().values(
                name=stock
            ))
        conn.commit()

res = add_fake_stock_name_data()

def add_fake_stock_data():
    with engine.connect() as conn:
        # 가상의 주식 데이터 생성
        price = random.uniform(100, 200)  # 주식 가격
        volume = random.randint(1000, 5000)  # 거래량
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        stock_id = random.randint(1, 5)

        # 데이터 삽입
        conn.execute(stocks_table.insert().values(
            timestamp=timestamp,
            price=price,
            volume=volume,
            stock_id=stock_id
        ))
        conn.commit()
    return price, volume

price, volume = add_fake_stock_data()

def load_data():
    with engine.connect() as conn:
        # query = "SELECT * FROM tb_price ORDER BY created_at DESC LIMIT 100"
        query = "SELECT * FROM stocks ORDER BY timestamp DESC LIMIT 100"
        return pd.read_sql(query, conn)
    
data = load_data()

st.title("Real-Time Stock Dashboard")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Latest Price", value=f"${price:.2f}")
with col2:
    st.metric(label="Latest Volume", value=f"{volume}")
with col3:
    price_change = price - data['price'].iloc[1]
    volume_change = volume - data['volume'].iloc[1] 
    st.metric(label="Price Change", value=f"${price_change:.2f}", delta=f"${price_change:.2f}")
    st.metric(label="Volume Change", value=f"{volume_change}", delta=f"{volume_change}")

fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Stock Price & Volume", ""),
                    row_heights=[0.7, 0.3])

fig.add_trace(
    go.Scatter(x=data['timestamp'], y=data['price'], mode='lines', name='Price', line=dict(color='blue', width=2)),
    row=1, col=1
)
fig.add_trace(
    go.Bar(x=data['timestamp'], y=data['volume'], name='Volume', marker=dict(color='orange')),
    row=2, col=1
)

fig.update_layout(title="Stock Price & Volume",
                  showlegend = False, 
                  yaxis_title="Price",
                  yaxis2_title="Volume",
                  height=700)

st.plotly_chart(fig)

with st.expander("View Raw Data"):
    st.dataframe(data)

st.divider()

st.write("## Select a stock to view its detailed price and volume information.")

@st.fragment
def stock_selector(stocks):
    main_selection = st.selectbox("Stocks", stocks)
    return main_selection

selected_stock = stock_selector(stocks)
selected_stock_data = data[data['stock_id'] == ids[stocks.index(selected_stock)]]

fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Stock Price & Volume", ""),
                    row_heights=[0.7, 0.3])

fig.add_trace(
    go.Scatter(x=selected_stock_data['timestamp'], y=selected_stock_data['price'], mode='lines', name='Price', line=dict(color='blue', width=2)),
    row=1, col=1
)
fig.add_trace(
    go.Bar(x=selected_stock_data['timestamp'], y=selected_stock_data['volume'], name='Volume', marker=dict(color='orange')),
    row=2, col=1
)

fig.update_layout(title="Stock Price & Volume",
                  showlegend = False, 
                  yaxis_title="Price",
                  yaxis2_title="Volume",
                  height=700)

st.plotly_chart(fig)   