import streamlit as st
import requests
import pandas as pd

@st.cache_resource(ttl=60s)
def load_data():
  url = 'https://www.twse.com.tw/rwd/zh/afterTrading/MI_INDEX?date=20240429&type=17&response=json&_=1714387790744'
  r = requests.get(url)
  data = r.json()['tables'][8]
  df = pd.DataFrame(data['data'], columns=data['fields'])
  return df

# Load the data
df = load_data()


col1, col2 = st.columns(2)
stock = col1.selectbox("證券名稱", df['證券名稱'], index=2)
stock_number = df.loc[df['證券名稱'] == stock, '證券代號'].values[0]
col2.text_input("證券代號", stock_number, disabled=True)

closing_price = float(df.loc[df['證券名稱'] == stock, '收盤價'].values[0])
cash_dividend = 0.4
stock_dividend = 0.56

col1, col2, col3 = st.columns(3)
col1.text_input("收盤價", closing_price, disabled=True)
col2.text_input("現金股利", cash_dividend, disabled=True)
col3.text_input("股票股利", stock_dividend, disabled=True)

have_stock_number = st.number_input("持有張數", step=1)

col1, col2 = st.columns(2)
total_cash = int(have_stock_number * cash_dividend * 1000)
total_stock = int(have_stock_number * stock_dividend * 100)
col1.text_input("現金股利(總額)", total_cash, disabled=True)
col2.text_input("股票股利(總額)", total_stock, disabled=True)



col1, col2 = st.columns(2)
total_cash_transfer = int((total_stock * closing_price) + total_cash)
total_stock_transfer = int((total_cash / closing_price) + total_stock)
col1.text_input("換算台幣", total_cash_transfer, disabled=True)
col2.text_input("換算股票", total_stock_transfer, disabled=True)
