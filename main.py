import streamlit as st

add_selectbox = st.sidebar.selectbox(
    "Avaliação",
    (chr(0x2606), 2*chr(0x2606), 3*chr(0x2606), 4*chr(0x2606), 5*chr(0x2606))
)

preco = st.sidebar.slider('Faixa de preço', 0, 130, 25)