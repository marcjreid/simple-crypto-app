import streamlit as st
from apps import home, crossover, candlestick

PAGES = {
    "Home": home,
    "Rising Currencies": crossover,
    "Currency Charts": candlestick
}

st.sidebar.title('Navigation')

selection = st.sidebar.radio("Go to", list(PAGES.keys()))

page = PAGES[selection]

page.app()