from functions.amazon_scraper import search_produto
import streamlit as st

st.sidebar.select_slider()

with st.form(key="entrada"):
    text_input = st.text_input(label='Buscar o produto')
    submit_button = st.form_submit_button(label='Buscar')

    if submit_button:
        if text_input != "":
            data = search_produto(text_input)
