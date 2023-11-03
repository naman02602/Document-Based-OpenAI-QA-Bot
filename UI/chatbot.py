import streamlit as st
import requests  # Import the requests library
import os

FASTAPI_SERVICE_URL = os.getenv("FASTAPI_SERVICE_URL")  # Replace with your FastAPI service URL


def ask_question(question, selected_pdfs, token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(
        f"{FASTAPI_SERVICE_URL}/ask",
        json={"question": question, "pdfs": selected_pdfs},
        headers=headers,
    )
    if response.status_code == 200:
        return response.json()["answer"]
    else:
        st.error("An error occurred while fetching the answer.")
        return None


def show():
    st.title("Chat with our Bot")

    # Step 1: Add Multiselect Widget
    pdf_options = [
        "form1-e.pdf",
        "form1-k.pdf",
        "form1-n.pdf",
        "form1-sa.pdf",
        "form1-z.pdf",
    ]  # Replace with actual PDF names
    selected_pdfs = st.multiselect(
        "Select PDFs:", options=pdf_options, default=pdf_options
    )

    # Initialize chat history if it doesn't exist
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []

    user_input = st.text_input("Ask me anything...")

    # st.markdown(
    #     f"<div style='background-color: lightblue; padding: 10px; border-radius: 10px;'>You: {user_input}</div>",
    #     unsafe_allow_html=True,
    # )
    st.markdown(
        f"<div style='background-color: lightblue; padding: 10px; border-radius: 10px; color: black; font-weight: bold;'>You: {user_input}</div>",
        unsafe_allow_html=True,
    )
    if user_input:
        if st.button("Submit"):
            if not selected_pdfs:
                selected_pdfs = pdf_options

            # Call the function to send a request to your FastAPI service
            answer = ask_question(user_input, selected_pdfs, st.session_state["token"])
            if answer:
                # Update chat history
                st.session_state["chat_history"].extend(
                    [
                        {"sender": "User", "message": user_input},
                        {"sender": "Bot", "message": answer},
                    ]
                )
            # Error handling is done inside ask_question function
        else:
            st.warning("Please enter a question")
        user_input = ""
    # st.markdown(
    #     f"<div style='background-color: lightblue; padding: 10px; border-radius: 10px;'>Bot: {answer}</div>",
    #     unsafe_allow_html=True,
    # )
    # Display chat history
    for message in st.session_state["chat_history"]:
        st.write(f"{message['sender']}: {message['message']}")

    st.write("Chat History will appear here")

    def generate_chat_text(chat_history):
        # Convert each message in the chat history to a string and join them with line breaks
        chat_text = "\n".join(
            [f"{message['sender']}: {message['message']}" for message in chat_history]
        )
        return chat_text

    # Generate the chat text from the chat history
    chat_text = generate_chat_text(st.session_state["chat_history"])

    # Create a download button for the chat history
    st.download_button(
        label="Download Chat History",
        data=chat_text,
        file_name="chat_history.txt",
        mime="text/plain",
    )
