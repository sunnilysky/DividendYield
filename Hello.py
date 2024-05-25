import streamlit as st
import requests
import pandas as pd
import datetime

@st.cache()
def load_data():
    today = datetime.date.today()
    
    # Check if today is Saturday (5) or Sunday (6)
    if today.weekday() == 5:  # Saturday
        today = today - datetime.timedelta(days=1)
    elif today.weekday() == 6:  # Sunday
        today = today - datetime.timedelta(days=2)

    date_str = today.strftime('%Y%m%d')
    url = f'https://www.twse.com.tw/rwd/zh/afterTrading/MI_INDEX?date={date_str}&type=17&response=json&_=1714387790744'
    print(url)
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
dividend_yield = (cash_dividend + stock_dividend)/closing_price * 100

col1, col2, col3, col4 = st.columns(4)
col1.text_input("收盤價", closing_price, disabled=True)
col2.text_input("現金股利", cash_dividend, disabled=True)
col3.text_input("股票股利", stock_dividend, disabled=True)
col4.text_input("殖利率", f'{dividend_yield:.2f} %', disabled=True)

st.text_input("提醒", '六日使用自動抓取禮拜五收盤價，股利數據尚無自動更新(目前是台中銀)', disabled=True)
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
