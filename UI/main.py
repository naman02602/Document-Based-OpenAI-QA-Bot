# # main.py
import streamlit as st
from signup import show as show_signup
from login import show as show_login
from home import show as show_home
from chatbot import show as show_chatbot
import logging
from logging_config import logger

logger = logging.getLogger(__name__)

def main():
    # Initialize session state variables
    if "page" not in st.session_state:
        st.session_state["page"] = "Login"  # Set initial page to Login

    # Sidebar for navigation
    st.sidebar.title("Navigation")

    # Check if user is logged in
    if "token" in st.session_state:
        # User is logged in
        page_selection = st.sidebar.radio("Go to", ["Home", "Logout"])
    else:
        # User is not logged in
        page_selection = st.sidebar.radio("Go to", ["Login", "Signup"])

    # Update session state based on sidebar selection
    st.session_state["page"] = page_selection

    # Display pages based on session state
    if st.session_state["page"] == "Signup":
        show_signup()
    elif st.session_state["page"] == "Login":
        show_login()
    elif st.session_state["page"] == "Home":
        show_chatbot()
    elif st.session_state["page"] == "Logout":
        st.session_state.pop("token", None)  # Remove token from session state
        st.session_state["page"] = "Login"  # Set page to Login
        logger.warning("User logged out")
        st.experimental_rerun()  # Rerun the script to update the UI


if __name__ == "__main__":
    main()
