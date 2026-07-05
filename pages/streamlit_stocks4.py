import streamlit as st
import altair as alt
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import date
from Data import Data
stocks = Data('resources/tech10_2.csv')

def line_with_annotation(df):
    
    df = df.reset_index()
    #print(df)
    line = alt.Chart(df).mark_line()\
              .encode(x=df.columns[0], y=df.columns[1])
    last_point = df.iloc[-1:]#Series doesn't work here[[-1]]yes[-1]no
    point = alt.Chart(last_point)\
               .mark_circle(size=100, color="red")\
               .encode(x=df.columns[0], y=df.columns[1])
    text = alt.Chart(last_point)\
              .mark_text(align="left", dx=-10, dy=10,
                         fontSize=15, color="red")\
              .encode(x=df.columns[0], y=df.columns[1], 
                      text=alt.Text(f"{df.columns[1]}", format=".2f"))\
              #if you have another mark_text here, the first is replaced
    chart = line + point + text
    st.altair_chart(chart, use_container_width=True)

def line_with_annotation2(df):
    df = df.reset_index()

    x_col = df.columns[0]

    df_long = df.melt(
        id_vars=x_col,
        var_name="series",
        value_name="value"
    )

    line = alt.Chart(df_long).mark_line().encode(
        x=x_col,
        y="value",
        color="series"
    )

    last_points = df_long.groupby("series").tail(1)

    point = alt.Chart(last_points).mark_circle(size=150,color="red").encode(
        x=x_col,
        y="value",
        #color="series"
    )

    text = alt.Chart(last_points).mark_text(
        align="left",
        dx=5,
        dy=-5,
        color="red"
    ).encode(
        x=x_col,
        y="value",
        text=alt.Text("value:Q", format=".2f"),
        #color="series"
    )

    st.altair_chart(line + point + text, use_container_width=True)


st.markdown(
    """
    <style>
        @media (max-width:926px) {
            div[data-testid="stHorizontalBlock"] {
                flex-direction: column !important;
            }
        }
    </style>
    """, unsafe_allow_html=True
    )
st.set_page_config(layout='wide')

st.title('Top Tech Stocks Analysis')

# stocks.df = pd.read_csv('pages/tech10_2.csv', 
#   index_col = 'date',
#   parse_dates = True
#   )
#print(stocks.df)
sec1, spacing, sec2 = st.columns([4,0.4,4])

with sec1:
    st.write('### Input Data')
    col1, col2= sec1.columns(2)

    time_range = {'min_value': stocks.df.index[0], 'max_value': stocks.df.index[-1], 'format': 'MM-DD-YYYY'}

    with col1:
        start_date = col1.date_input('Start Date', value=date(2025,5,1), **time_range)

    with col2:
        end_date = col2.date_input('End Date', value=date(2026,5,1), **time_range)

    
    available_tickers = stocks.columns
    selected_tickers = st.multiselect(
        "Select stock tickers for analysis:",
        options=available_tickers,
        default=['SPY','AAPL', 'GOOGL','NVDA','AMD']
    )
    #print(type(selected_tickers), selected_tickers)


    st.write(stocks.df.loc[start_date:end_date].head())
    
    st.write(f'### Stocks Daily Return')

    # stocks_daily_return = stocks.df.loc[start_date:end_date, select_column].pct_change().dropna()

    st.line_chart(stocks.get_daily_return(start_date = start_date, end_date= end_date,columns=selected_tickers))

    st.write(f'### Stocks Cumulative Returns')
    line_with_annotation2(stocks.get_cumulative_return(start_date = start_date, end_date= end_date,columns=selected_tickers))
    st.write(f'#### {selected_tickers} cumulative returns: {stocks.get_cumulative_return(start_date = start_date, end_date= end_date,columns=selected_tickers).iloc[-1].values}')


    st.write(f'### Stocks Daily Return Volatility')
    fig = px.box(stocks.get_daily_return(start_date = start_date, end_date= end_date,columns=selected_tickers))
    st.plotly_chart(fig, theme='streamlit')

with sec2:

    st.write(f'### Sharpe Ratio')
    st.bar_chart(stocks.sharpe_ratio(start_date = start_date, end_date= end_date,columns=selected_tickers))
    st.latex(r"\text{Sharpe Ratio} = \frac{R_p - R_f}{\sigma_p}")
    st.markdown("""
    **Where:**
    - \(R_p\) = Portfolio return
    - \(R_f\) = Risk-free rate
    - \(\sigma_p\) = Standard deviation (volatility) of returns
    """)

    st.write(f'### Sortino ratio')
    st.bar_chart(stocks.sortino_ratio(start_date = start_date, end_date= end_date,columns=selected_tickers))
    st.latex(r"\text{Sortino Ratio} = \frac{R_p - R_f}{\sigma_d}")
    st.markdown("""
    **Where:**
    - \(R_p\) = Portfolio return
    - \(R_f\) = Risk-free rate
    - \(\sigma_d\) = Downside deviation
    """)

    st.write(f'### Beta Value')
    st.bar_chart(stocks.get_beta())
    st.latex(r"""\beta = \frac{\operatorname{Cov}(R_{stock}, R_{market})}{\operatorname{Var}(R_{market})}""")
