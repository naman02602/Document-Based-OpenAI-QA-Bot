import streamlit as st
import requests


def show():
    st.title("Signup Page")

    username = st.text_input("Username")
    fullname = st.text_input("Full Name")
    password = st.text_input("Password", type="password")

    if st.button("Signup"):
        # Define the URL of your FastAPI signup endpoint
        url = "http://localhost:8000/signup"  # Adjust the URL as needed

        # Prepare the signup data
        signup_data = {"username": username, "fullname": fullname, "password": password}

        # Send a POST request to the FastAPI signup endpoint
        response = requests.post(url, json=signup_data)

        if response.status_code == 200:
            st.success(f"User {username} created successfully!")
        else:
            st.error(f"An error occurred: {response.json()}")
