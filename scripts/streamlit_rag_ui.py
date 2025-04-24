import os
os.environ["STREAMLIT_DISABLE_WATCHDOG_WARNINGS"] = "true"
os.environ["STREAMLIT_WATCH_MODE"] = "false"

import sys
import hashlib
import streamlit as st
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader, TextLoader, CSVLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings

def verify_index_integrity(folder="vector_index"):
    if not os.path.exists(folder):
        return False
    for root, dirs, files in os.walk(folder):
        for file in files:
            path = os.path.join(root, file)
            with open(path, 'rb') as f:
                h = hashlib.sha256()
                for chunk in iter(lambda: f.read(4096), b''):
                    h.update(chunk)
                checksum = h.hexdigest()
                st.write(f"🔐 Verified {file}: {checksum}")
    return True

def load_docs(file_paths):
    docs = []
    for path in file_paths:
        if path.endswith(".pdf"):
            loader = PyPDFLoader(path)
        elif path.endswith(".csv"):
            loader = CSVLoader(file_path=path)
        else:
            loader = TextLoader(path)
        docs.extend(loader.load())
    return docs

def embed_and_store(docs):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    texts = text_splitter.split_documents(docs)
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    db = FAISS.from_documents(texts, embedding=embeddings)
    db.save_local("vector_index")
    return db

def load_db():
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    if verify_index_integrity():
        return FAISS.load_local("vector_index", embeddings, allow_dangerous_deserialization=True)
    else:
        st.error("❌ Failed to verify vector index integrity.")
        return None

def query_db(db, query):
    return db.similarity_search(query, k=4)

def main_app():
    st.title("🧠 BYO-SecAI RAG Streamlit UI")
    uploaded_files = st.file_uploader("Upload PDFs, CSVs, or text files", type=["pdf", "csv", "txt", "log", "md"], accept_multiple_files=True)

    if uploaded_files and st.button("Ingest Files"):
        os.makedirs("data", exist_ok=True)
        file_paths = []
        for uploaded_file in uploaded_files:
            file_path = os.path.join("data", uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            file_paths.append(file_path)
        docs = load_docs(file_paths)
        embed_and_store(docs)
        st.success("✅ Files ingested and vector index created!")

    if os.path.exists("vector_index"):
        query = st.text_input("Ask something about your documents:")
        if query:
            db = load_db()
            if db:
                results = query_db(db, query)
                for i, res in enumerate(results):
                    st.write(f"### Match {i+1}")
                    st.write(res.page_content)

def safe_exit_on_error(func):
    try:
        func()
    except Exception as e:
        st.error(f"❌ Streamlit error: {e}")
        sys.exit(1)

safe_exit_on_error(main_app)