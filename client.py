import requests
import streamlit as st

def get_pdf_response(session_id, question):
    response = requests.post(
        f"http://localhost:8000/chat/",
        data={'question': question},  # Send as form data
        cookies={'session_id': session_id}
    )
    return response.json()

def upload_pdf(file):
    files = {'file': file}
    response = requests.post("http://localhost:8000/upload/", files=files)
    return response.json()['session_id']

if __name__ == "__main__":
    st.title("Chat with PDF")

    uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")
    if uploaded_file is not None:
        session_id = upload_pdf(uploaded_file)
        st.success("File uploaded successfully!")

        question = st.text_input("Ask your question:")
        if question:
            response = get_pdf_response(session_id, question)
            if 'error' in response:
                st.error(response['error'])  # Display error message
            else:
                st.write(f"**Chatbot:** {response['response']}")  # Display the answer  