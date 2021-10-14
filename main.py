from functions.amazon_scraper import search_produto
import streamlit as st


add_selectbox = st.sidebar.selectbox(
    "Avaliação",
    (chr(0x2606), 2*chr(0x2606), 3*chr(0x2606), 4*chr(0x2606), 5*chr(0x2606))
)

with st.form(key="entrada"):
    text_input = st.text_input(label='Buscar o produto')
    submit_button = st.form_submit_button(label='Buscar')

    if submit_button:
        if text_input != "":
            
