import streamlit as st

st.set_page_config(
    page_title='Security Awareness Quiz',
    page_icon='🔐'
)

st.title('Security Awareness Quiz')

name = st.text_input('Enter your name')

if st.button('Start Quiz'):

    if name.strip():
        st.success(f'Welcome, {name}!')
    else:
        st.error('Please enter your name before starting the quiz.')