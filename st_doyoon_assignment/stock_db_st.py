from dotenv import load_dotenv
import os
import pandas as pd
from sqlalchemy import create_engine
import streamlit as st

load_dotenv()

DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', 3306)),
    'user': os.getenv('DB_USER', 'analyst'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'stocks')
}

engine = create_engine(f'mysql+pymysql://{DB_CONFIG["user"]}:{DB_CONFIG["password"]}@{DB_CONFIG["host"]}:{DB_CONFIG["port"]}/{DB_CONFIG["database"]}')

def get_stocks():
    with engine.connect() as conn:
        return pd.read_sql("SELECT * FROM tb_stock", conn)

def get_data(stock_id):
    with engine.connect() as conn:
        query = "SELECT * FROM tb_price WHERE stock_id = %s ORDER BY created_at DESC LIMIT 100"
        return pd.read_sql(query, conn, params=(stock_id,))

stocks = get_stocks()

def stock_selector(stocks):
    main_selection = st.selectbox("Stocks", stocks)
    return main_selection

stock = stock_selector(stocks['name'])

def get_id(stock):
    with engine.connect() as conn:
        query = "SELECT id FROM tb_stock WHERE name = %s"
        result = pd.read_sql(query, conn, params=(stock,))
        if not result.empty:
            return result['id'].iloc[0]
        return None

stock_id = get_id(stock)

data = get_data(stock_id)

st.dataframe(data)