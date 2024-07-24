# RAG Chatbot Project

This project is a Retrieval-Augmented Generation (RAG) chatbot that leverages FastAPI for the backend and Streamlit for the frontend. The chatbot is designed to provide intelligent responses by combining retrieval-based information and generative AI techniques.

## Project Structure

- `main.py`: This file contains the FastAPI code for the chatbot backend.
- `client.py`: This file contains the Streamlit code for the chatbot frontend.

https://www.loom.com/share/2b18ffad54dc40fab374a5806543cd00?sid=ab399368-a0dd-449f-8ec3-7a10babfb91b

## Prerequisites

Before running the project, make sure you have the following installed:

- Python 3.8 or higher
- FastAPI
- Uvicorn
- Streamlit
- Requests
- LangChain
- FAISS
- Any other dependencies specified in the `requirements.txt` file

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/hritikpal671/RAG-using-FastAPI-.git
   cd rag-chatbot
   ```

2. **Create a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate   # On Windows, use `venv\Scripts\activate`
   ```

3. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

### Backend (FastAPI)

1. **Navigate to the backend directory:**
   ```bash
   cd backend
   ```

2. **Run the FastAPI server:**
   ```bash
   uvicorn main:app --reload
   ```

   The backend server will start and be accessible at `http://127.0.0.1:8000`.

### Frontend (Streamlit)

1. **Navigate to the frontend directory:**
   ```bash
   cd frontend
   ```

2. **Run the Streamlit application:**
   ```bash
   streamlit run client.py
   ```

   The frontend will be accessible at `http://localhost:8501`.

## Usage

1. Open your browser and go to `http://localhost:8501` to access the Streamlit UI.
2. Interact with the chatbot by typing your queries in the provided input box.
3. The chatbot will use the RAG approach to provide responses based on the input query.

## Project Details

### main.py

- **Description:** This file defines the FastAPI application which serves the backend for the chatbot.
- **Key Components:**
  - Endpoint to handle user queries.
  - Integration with LangChain and FAISS for retrieval-augmented generation.

### client.py

- **Description:** This file defines the Streamlit application which serves the frontend for the chatbot.
- **Key Components:**
  - Streamlit UI for user interaction.
  - HTTP requests to the FastAPI backend for obtaining chatbot responses.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
