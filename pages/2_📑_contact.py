import streamlit as st

st.set_page_config(
    page_title="Contacts Page",
    page_icon="📑",
)

if st.session_state['user_login'] == True:
    st.title("Contacts")
    st.header("Welcome to contact page")
else:
    st.title("Please Log in First")

# st.write(f"you typed {st.session_state['my_input']}")

