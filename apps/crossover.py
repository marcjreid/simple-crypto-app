import streamlit as st
import numpy as np
import pandas as pd
import yfinance as yf
from bs4 import BeautifulSoup
import requests


def symbol_gen():
        response = requests.get("https://finance.yahoo.com/cryptocurrencies")
        soup = BeautifulSoup(response.content,'lxml')
        symbols = []
        for item in soup.select('.simpTblRow'):
            symbols.append(item.select('[aria-label=Symbol]')[0].get_text())
        return symbols


def app():
    st.title("Crossover Checker")
    st.write("Looking at Crossover is a basic trading strategy.")
    st.write("When their is crossover in the 7 and 25 day moving average it is a signal a potential change in trend.")
    st.write("This app lists the currencies that show this signal in the last 2 hours.")


    def convert_df(df):
        df = df.iloc[-31:]
        df.index.names = ['E']
        df.rename(columns={'Close':'c'}, inplace=True)
        df = df[['c']]
        return df  

    def applytechnicals(df):
        df['SMA_7'] = df['c'].rolling(7).mean()
        df['SMA_25'] = df['c'].rolling(25).mean()
        df.dropna(inplace=True)
        return df

    def query(symbol):
        df = yf.download(tickers=symbol, period = '2h', interval = '1m')
        df = convert_df(df)
        df = applytechnicals(df)
        df['position'] = np.where(df['SMA_7'] > df['SMA_25'], 1, 0)
        return df

    symbols = symbol_gen()
    crossing_symbols = []

    def check():
        for symbol in symbols:
            if len(query(symbol)['position']) > 1:
                if query(symbol)['position'][-1] and query(symbol)['position'].diff()[-1]:
                    crossing_symbols.append(symbol)

    if crossing_symbols == []:
        st.write("There are no currently cryptocurrencies with Simple Moving Average Crossovers")
        st.write("these were the commodities checked.")
        st.write(symbols)
    else:
        st.write(crossing_symbols)

    st.button('Get Live SMA Cross', on_click=check())