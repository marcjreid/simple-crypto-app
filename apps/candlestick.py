import streamlit as st
import datetime as dt
import pandas_datareader as pdr
import pandas_ta as ta
import pandas as pd
import numpy as np
import plotly.offline as pyo
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from .crossover import *

def app():
    st.title("Candlestick and MACD Chart")
    stickers = symbol_gen()

    currency = st.selectbox(
        "Choose a cryptocurrency to look at candlestick data", tuple(stickers)
        )

    def graph_gen(sticker):
        end = dt.datetime.now()
        start = end - dt.timedelta(days=61)
        df = pdr.DataReader(sticker, 'yahoo', start, end)
        df = pd.concat([df, df.ta.macd(close='Close', fast=12, slow=26, signal=9, append=True)])
        # Force lowercase (optional)
        df.columns = [x.lower() for x in df.columns]

        # Construct a 2 x 1 Plotly figure
        fig = make_subplots(rows=2, cols=1)
        # price Line
        fig.append_trace(
            go.Scatter(
                x=df.index,
                y=df['open'],
                line=dict(color='#228B22', width=1),
                name='open',
                # showlegend=False,
                legendgroup='1',
            ), row=1, col=1
        )
        # Candlestick chart for pricing
        fig.append_trace(
            go.Candlestick(
                x=df.index,
                open=df['open'],
                high=df['high'],
                low=df['low'],
                close=df['close'],
                #increasing_line_color='#ff9900',
                #decreasing_line_color='black',
                showlegend=False
            ), row=1, col=1
        )
        # Fast Signal (%k)
        fig.append_trace(
            go.Scatter(
                x=df.index,
                y=df['macd_12_26_9'],
                line=dict(color='#ff9900', width=2),
                name='macd',
                # showlegend=False,
                legendgroup='2',
            ), row=2, col=1
        )
        # Slow signal (%d)
        fig.append_trace(
            go.Scatter(
                x=df.index,
                y=df['macds_12_26_9'],
                line=dict(color='#000000', width=2),
                # showlegend=False,
                legendgroup='2',
                name='signal'
            ), row=2, col=1
        )
        # Colorize the histogram values
        colors = np.where(df['macdh_12_26_9'] < 0, '#000', '#ff9900')
        # Plot the histogram
        fig.append_trace(
            go.Bar(
                x=df.index,
                y=df['macdh_12_26_9'],
                name='histogram',
                marker_color=colors,
            ), row=2, col=1
        )
        # Make it pretty
        layout = go.Layout(
            title_text = sticker + " 61 Day Chart",
            width=1200,
            height=800,
            plot_bgcolor='#efefef',
            # Font Families
            font_family='Monospace',
            font_color='#000000',
            font_size=20,
            xaxis=dict(
                rangeslider=dict(
                    visible=False
                )
            )
        )
        # Update options and show plot
        fig.update_layout(layout)
        st.write(fig)

    graph_gen(currency)