import streamlit as st
import requests  # Import the requests library
import os
import logging
from logging_config import logger

logger = logging.getLogger(__name__)

# Define the URL of your FastAPI service
FASTAPI_SERVICE_URL = os.getenv("FASTAPI_SERVICE_URL") 


def show():
    st.title("Login Page")

    st.write(
        "In order to use this QA chatbot, make sure that your FastAPI Server is running."
    )
    st.write("Click on Health Check to test")

    if st.button("Health Check"):
        # Your health check code here
        try:
            # Send a GET request to the /health endpoint
            response = requests.get(f"{FASTAPI_SERVICE_URL}/health")

            # Check the response status code
            if response.status_code == 200:
                health_data = response.json()
                logger.info("APIs are up and running.")
                st.success(
                    f"Server status: {health_data['status']} - {health_data['message']}"
                )
            else:
                logger.error("APIs are not running. Check your server")
                st.error(
                    f"Unexpected response: {response.status_code} - {response.text}"
                )
        except requests.RequestException as e:
            logger.error("APIs are not running. Check your server")
            st.error(f"Servers are not up and running")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if username and password:
        if st.button("Login"):
            # Prepare the request data
            login_data = {"username": username, "password": password}
            logger.info(f"Login attempt by user: {username}")
            # Send a POST request to the /login endpoint
            response = requests.post(f"{FASTAPI_SERVICE_URL}/login", data=login_data)

            # Check the response status code
            if response.status_code == 200:
                # Login was successful
                token_data = response.json()
                st.write("Login successful! Redirecting...")
                logger.info(f"Login successful for user: {username}")
                st.session_state["token"] = token_data[
                    "access_token"
                ]  # Save the token in the session state
                st.session_state["page"] = "Home"  # Set the current page to Home
                st.experimental_rerun()

            else:
                # Login failed
                logger.warning(f"Invalid login attempt by user: {username}")
                st.error("Invalid credentials. Please try again.")
    else:
        st.warning("Username and Password must be entered to login")
