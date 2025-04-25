# BYO-SecAI RAG Module – rag_ingest_and_query.py (HuggingFace + Safe Deserialization)
import os
import glob
import pandas as pd
from pathlib import Path
from datetime import datetime
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS

SUPPORTED_EXTS = ['.pdf', '.md', '.csv', '.txt', '.log']
VECTOR_DIR = 'vector_index'
DEFAULT_LOG_DIR = 'logs'

EMBED_MODEL = HuggingFaceEmbeddings(model_name='all-MiniLM-L6-v2')

def load_documents(folder, logfile):
    documents = []
    log(f"Scanning folder: {folder}", logfile)
    for ext in SUPPORTED_EXTS:
        for filepath in glob.glob(f'{folder}/**/*{ext}', recursive=True):
            path = Path(filepath)
            log(f"Loading {filepath}", logfile)
            if ext == '.csv':
                try:
                    df = pd.read_csv(filepath, encoding='utf-8', engine='python')
                    for i, row in df.iterrows():
                        doc = Document(page_content=str(row.to_dict()), metadata={"source": str(path)})
                        documents.append(doc)
                except Exception as e:
                    log(f"[ERROR] CSV {filepath}: {e}", logfile)
                try:
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        if content.strip():
                            documents.append(Document(page_content=content, metadata={"source": str(path)}))
                except Exception as e:
                    log(f"[ERROR] {filepath}: {e}", logfile)
    log(f"Loaded {len(documents)} documents total", logfile)
    return documents

def create_index(input_dir, logfile):
    log("Starting ingestion", logfile)
    docs = load_documents(input_dir, logfile)
    log(f"Loaded {len(docs)} raw documents", logfile)

    splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=32)
    splits = splitter.split_documents(docs)
    texts = [s.page_content for s in splits if s.page_content.strip()]
    log(f"Split into {len(texts)} text chunks", logfile)

    if not texts:
        log("[ABORT] No valid content to embed.", logfile)
        print("[!] No valid content to embed. Please check your files.")
        return

    db = FAISS.from_texts(texts, embedding=EMBED_MODEL)
    db.save_local(VECTOR_DIR)
    log(f"Vector index created and saved to {VECTOR_DIR}/", logfile)
    print(f"[✔] Vector index saved to {VECTOR_DIR}/")

def query_rag(query, logfile, top_k=3):
    log(f"Query received: {query}", logfile)
    try:
        db = FAISS.load_local(VECTOR_DIR, EMBED_MODEL, allow_dangerous_deserialization=True)
        print(f"🔧 DEBUG: vector_index exists: {os.path.exists(VECTOR_DIR)}")
        print("🔧 DEBUG #4: FAISS index loaded")

        results = db.similarity_search_with_score(query, k=top_k)  # Get similar docs
        for i, (doc, score) in enumerate(results):
            print(f"--- Document {i+1} (Score: {score:.4f}) ---")  # Include score
            print(doc.page_content)
            print(f"Source: {doc.metadata['source']}")  # Print source
            print("🔧 DEBUG #6: Output result")
            print()

        return results  # Optionally return results for further processing

    except Exception as e:
        log(f"[ERROR] Query failed: {e}", logfile)
        print(f"[!] Query failed: {e}")
        return None  # Or raise the exception, depending on your error handling policy


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--query-mode', action='store_true', help='Interactive mode using your ingested documents')
    parser.add_argument('--ingest', help="Folder to ingest files from")
    parser.add_argument('--query', help="Query the vector index")
    parser.add_argument('--logfile', help="Log output to this file (default: logs/ingestion_LOGDATE.txt)")
    args = parser.parse_args()
    print("🔧 DEBUG #1: CLI args parsed")

    if not args.logfile:
        os.makedirs(DEFAULT_LOG_DIR, exist_ok=True)
        now_str = datetime.now().strftime('%Y%m%d_%H%M%S')
        logfile = os.path.join(DEFAULT_LOG_DIR, f"ingestion_{now_str}.txt")
    else:
        logfile = args.logfile

    def log(msg, logfile):
        with open(logfile, 'a', encoding='utf-8') as logf:
            logf.write(f"[{datetime.now().isoformat()}] {msg}\n")

    if args.ingest:
        create_index(args.ingest, logfile)
    elif args.query:
        query_rag(args.query, logfile)
    else:
        print("Usage: python rag_ingest_and_query.py --ingest data/ OR --query 'example question'")