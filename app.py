import streamlit as st

# st.title("Meow home")

st.markdown("""
<style>
div.stButton > button {
    width: 400px;
    height: 250px;
    background-image: url("https://raw.githubusercontent.com/lis497/stock-analysis-dashboard/main/images/stock.png");
    background-size: cover;
    border: none;
    color: transparent;  /* Hide the button text */
}
</style>
""", unsafe_allow_html=True)

if st.button("Navigate"):
    st.switch_page("pages/streamlit_stocks4.py")