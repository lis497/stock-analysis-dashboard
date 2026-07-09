import streamlit as st
import plotly.graph_objects as go

st.title("📈 Stock Profit Donut Chart")

# Example values
shares = st.number_input("Number of Shares", value=100)
buy_price = st.number_input("Buy Price", value=120.0)
current_price = st.number_input("Current Price", value=145.0)

investment = shares * buy_price
current_value = shares * current_price
profit = current_value - investment
profit_percent = (profit / investment) * 100 if investment > 0 else 0

# Colors based on profit/loss
profit_color = "green" if profit >= 0 else "red"

fig = go.Figure(
    go.Pie(
        #labels=["Investment", "Profit"],
        values=[5,7,5,8,8,3],
        hole=0.65,
        marker=dict(colors=["lightgray", profit_color]),
        textinfo="label+percent"
    )
)

fig.update_layout(
    annotations=[
        dict(
            text=f"${profit:,.2f}<br>{profit_percent:.2f}%",
            x=0.5,
            y=0.5,
            font_size=22,
            showarrow=False
        )
    ],
    showlegend=True
)

st.plotly_chart(fig, use_container_width=True)

st.metric("Investment", f"${investment:,.2f}")
st.metric("Current Value", f"${current_value:,.2f}")
st.metric("Profit", f"${profit:,.2f}", f"{profit_percent:.2f}%")
