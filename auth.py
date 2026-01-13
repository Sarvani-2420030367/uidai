import pandas as pd
import streamlit as st

def login():
    users = pd.read_csv("users.csv")

    st.subheader("🔐 UIDAI Secure Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = users[
            (users["username"] == username) &
            (users["password"] == password)
        ]

        if not user.empty:
            st.session_state["logged_in"] = True
            st.session_state["user"] = user.iloc[0].to_dict()
            st.success("Login successful")
            st.rerun()
        else:
            st.error("Invalid credentials")
