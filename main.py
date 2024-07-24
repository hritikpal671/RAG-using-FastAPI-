from fastapi import FastAPI, File, UploadFile, Form, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import google.generativeai as genai
from langchain_google_genai import GoogleGenerativeAI
from langchain.docstore.document import Document
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.vectorstores.faiss import FAISS
import PyPDF2
from io import BytesIO  
from langchain.chains.question_answering import load_qa_chain

# Initialize FastAPI
app = FastAPI()

# Allow CORS 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

load_dotenv()  

# Configure Google Generative AI
api = genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")
llm = GoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.3, google_api_key=api)

# In-memory storage 
chat_sessions = {}

def parse_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()
    return text

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    content = await file.read()
    pdf_file = BytesIO(content) 
    document_text = parse_pdf(pdf_file)  
    document = Document(page_content=document_text)
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=api)
    session_id = os.urandom(16).hex()  
    session_id_str = session_id.encode('utf-8').decode('utf-8')  

    chat_sessions[session_id_str] = { 
        'document_text': document_text,
        'vectorstore': FAISS.from_documents([document], embeddings)
    }

    response = JSONResponse(content={"session_id": session_id_str, "message": "Document content loaded. You can now ask questions based on this document."})
    response.set_cookie(key="session_id", value=session_id_str)
    return response

# Your custom functions
def retrieve_relevant_chunks(question, session_id):
    vectorstore = chat_sessions[session_id]['vectorstore']
    docs = vectorstore.similarity_search(question, k=5) 
    return docs

# Load QA chain with Gemini-1.5-flash
qa_chain = load_qa_chain(llm, chain_type="stuff")  

def generate_answer(question, session_id):
    relevant_chunks = retrieve_relevant_chunks(question, session_id)
    if relevant_chunks:
        response = qa_chain.run(input_documents=relevant_chunks, question=question)
        return response
    else:
        return "The answer to this question is not found in the provided PDF."

@app.post("/chat/")
async def chat(request: Request, question: str = Form(...)):
    session_id = request.cookies.get("session_id")
    if session_id is None or session_id not in chat_sessions:
        return JSONResponse(content={"error": "Invalid session ID"}, status_code=400)
    
    answer = generate_answer(question, session_id)  # Pass session_id to generate_answer
    response = JSONResponse(content={"response": answer})
    response.set_cookie(key="session_id", value=session_id)
    return response

# To run the FastAPI app, use 'uvicorn main:app --reload' 