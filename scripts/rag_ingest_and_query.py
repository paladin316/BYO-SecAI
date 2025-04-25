import os
import sys
import traceback
from datetime import datetime
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

VECTOR_DIR = 'vector_index'
DEFAULT_LOG_DIR = 'logs'

EMBED_MODEL = HuggingFaceEmbeddings(model_name='all-MiniLM-L6-v2')

def query_rag(query, logfile, top_k=3):  # Added top_k
    log(f"Query received: {query}", logfile)
    try:
        if not os.path.exists(VECTOR_DIR):
            print("[!] No vector index found. Please ingest data first.")
            return None

        db = FAISS.load_local(VECTOR_DIR, EMBED_MODEL, allow_dangerous_deserialization=True)
        print(f"🔧 DEBUG: vector_index exists: {os.path.exists(VECTOR_DIR)}")
        print("🔧 DEBUG #4: FAISS index loaded")

        results = db.similarity_search_with_score(query, k=top_k)  # Get similar docs
        if results:  # Check if there are results
            for i, (doc, score) in enumerate(results):
                print(f"--- Document {i+1} (Score: {score:.4f}) ---")  # Include score
                print(doc.page_content)
                print(f"Source: {doc.metadata['source']}")  # Print source
                print("🔧 DEBUG #6: Output result")
                print()
        else:
            print("No matching documents found.")

        return results  # Optionally return results for further processing

    except Exception as e:
        log(f"[ERROR] Query failed: {e}", logfile)
        print(f"[!] Query failed: {e}")
        traceback.print_exc()
        return None

if __name__ == '__main__':
    query = None
    logfile = None

    try:
        if "--query" in sys.argv:
            query_index = sys.argv.index("--query") + 1
            if query_index < len(sys.argv) and sys.argv[query_index] != "":
                query = sys.argv[query_index]
            elif query_index < len(sys.argv) and sys.argv[query_index] == "":
                query = ""
            else:
                print("Error: --query argument requires a value.")
                sys.exit(1)

        if "--logfile" in sys.argv:
            logfile_index = sys.argv.index("--logfile") + 1
            if logfile_index < len(sys.argv) and sys.argv[logfile_index] != "":
                logfile = sys.argv[logfile_index]
            else:
                print("Error: --logfile argument requires a value.")
                sys.exit(1)

    except ValueError:
        print("Error: Invalid command-line arguments.")
        sys.exit(1)

    if not logfile:
        os.makedirs(DEFAULT_LOG_DIR, exist_ok=True)
        now_str = datetime.now().strftime('%Y%m%d_%H%M%S')
        logfile = os.path.join(DEFAULT_LOG_DIR, f"ingestion_{now_str}.txt")

    def log(msg, logfile):
        with open(logfile, 'a', encoding='utf-8') as logf:
            logf.write(f"[{datetime.now().isoformat()}] {msg}\n")

    try:
        if query is not None:  # Check if query is provided
            if query == "":  # Check if query is empty
                while True:
                    user_query = input("Enter your query (or type 'exit' to quit): ")
                    if user_query.lower() == 'exit':
                        break
                    query_rag(user_query, logfile)  # Call query_rag with logfile
            else:
                query_rag(query, logfile)  # Call query_rag with logfile
        else:
            print("Usage: python rag_ingest_and_query.py --query <query> [--logfile <logfile>]")
            sys.exit(1)

    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()
        sys.exit(1)