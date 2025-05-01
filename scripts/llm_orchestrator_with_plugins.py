#!/usr/bin/env python3
import os
import sys
import yaml
import logging
import concurrent.futures
import json
import datetime

# Ensure project root cwd
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, os.pardir))
os.chdir(PROJECT_ROOT)
sys.path.insert(0, PROJECT_ROOT)

# Setup directories
EVIDENCE_DIR = os.path.join(PROJECT_ROOT, 'evidence')
os.makedirs(EVIDENCE_DIR, exist_ok=True)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    filename=os.path.join(PROJECT_ROOT, 'plugin.log'),
    format='%(asctime)s %(levelname)s %(message)s'
)

# Load config
config_path = os.path.join(PROJECT_ROOT, 'config.yaml')
if not os.path.exists(config_path):
    logging.error(f"Missing config file at {config_path}")
    raise FileNotFoundError(f"config.yaml not found at {config_path}")
with open(config_path, 'r') as cf:
    CONFIG = yaml.safe_load(cf)
PLUGIN_TOGGLES = CONFIG.get('plugins', {})

# === Plugin Integration with Async, Toggles, Metadata ===
PLUGIN_DIR = os.path.join(PROJECT_ROOT, 'plugins')

def discover_plugins():
    plugins = []
    for filename in os.listdir(PLUGIN_DIR):
        if filename.endswith('.py') and filename != '__init__.py':
            name = filename[:-3]
            if PLUGIN_TOGGLES.get(name, True):
                plugins.append(name)
    return plugins


def load_plugin(plugin_name):
    path = os.path.join(PLUGIN_DIR, f"{plugin_name}.py")
    spec = __import__('importlib').util.spec_from_file_location(plugin_name, path)
    module = __import__('importlib').util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run_plugins(ioc: str):
    results = {}
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_map = {
            executor.submit(load_plugin(name).run, ioc): name
            for name in discover_plugins()
        }
        for future in concurrent.futures.as_completed(future_map):
            name = future_map[future]
            try:
                res = future.result()
                module = load_plugin(name)
                meta = module.meta() if hasattr(module, 'meta') else {}
                res['meta'] = meta
                results[name] = res
                logging.info(f"Plugin {name} succeeded for IOC {ioc}")
            except Exception as e:
                err = {'source': name, 'ioc': ioc, 'error': str(e)}
                results[name] = err
                logging.error(f"Plugin {name} error: {e}")
    return results

# === LLM & RAG Configuration ===
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from langchain_core.prompts import PromptTemplate
from langchain_ollama import OllamaLLM
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

OLLAMA_BASE_URL = "http://localhost:11434"

# Configure available Ollama models
mistral_llm     = OllamaLLM(model="mistral:latest", base_url=OLLAMA_BASE_URL, num_predict=1000)
phi_llm         = OllamaLLM(model="phi:latest", base_url=OLLAMA_BASE_URL, num_predict=1000)
gemma_llm       = OllamaLLM(model="gemma:latest", base_url=OLLAMA_BASE_URL, num_predict=1000)
codellama_llm   = OllamaLLM(model="codellama:latest", base_url=OLLAMA_BASE_URL, num_predict=1000)
llama2_llm      = OllamaLLM(model="llama2:latest", base_url=OLLAMA_BASE_URL, num_predict=1000)
llama3_llm      = OllamaLLM(model="llama3:latest", base_url=OLLAMA_BASE_URL, num_predict=1000)

# Enterprise-style model map
MODEL_MAP_OBJ = {
    "threat_ops_qa":      {"llm": mistral_llm,     "description": "ThreatOps Q&A Assistant (Mistral-based)"},
    "detection_studio":   {"llm": codellama_llm,   "description": "Detection Logic Studio (CodeLlama-based)"},
    "ttp_mapper":         {"llm": phi_llm,         "description": "MITRE TTP Mapper (Phi-based)"},
    "codegen_assistant":  {"llm": codellama_llm,   "description": "CodeGen Assistant for YARA & Scripts (CodeLlama-based)"},
    "playbook_designer":  {"llm": llama2_llm,      "description": "Playbook Designer for IR SOPs (Llama2-based)"},
    "rag_explorer":       {"llm": llama3_llm,      "description": "RAG Explorer – Query Uploaded Data Only (Llama3)"},
    "unified_analyst":    {"llm": llama3_llm,      "description": "Unified Analyst – General LLM + RAG (Llama3)"}
}

# RAG Configuration
VECTOR_DIR  = os.path.join(PROJECT_ROOT, 'vector_index')
EMBED_MODEL = HuggingFaceEmbeddings(model_name='all-MiniLM-L6-v2')

def retrieve_relevant_docs(query, top_k=3):
    try:
        if not os.path.exists(VECTOR_DIR):
            return None
        db = FAISS.load_local(VECTOR_DIR, EMBED_MODEL, allow_dangerous_deserialization=True)
        return db.similarity_search(query, k=top_k)
    except Exception as e:
        logging.error(f"Error retrieving docs: {e}")
        return None


def ask_ollama(llm_object, query_prompt):
    enhanced_prompt = f"{query_prompt}. Please provide a detailed and comprehensive answer."
    return llm_object.invoke(enhanced_prompt).strip()

def ask_rag_only(llm_object, user_query):
    docs = retrieve_relevant_docs(user_query)
    if docs:
        context = "\n\n".join(doc.page_content for doc in docs)
        prompt_tmplt = PromptTemplate.from_template(
            """Answer the following question based *only* on the provided documents. """
            """Documents:\n{documents}\nQuestion: {query}\nAnswer:"""
        )
        full = prompt_tmplt.format(documents=context, query=user_query)
        return ask_ollama(llm_object, full)
    return "No relevant information found in the knowledge base."

def ask_ollama_with_rag(llm_object, user_query):
    docs = retrieve_relevant_docs(user_query)
    if docs:
        context = "\n\n".join(doc.page_content for doc in docs)
        rag_prompt = f"Answer based on context:\n{context}\nQuestion: {user_query}\nAnswer:" 
        return ask_ollama(llm_object, rag_prompt)
    return ask_ollama(llm_object, user_query)

def display_help():
    print("\nAvailable commands:")
    for key, val in MODEL_MAP_OBJ.items():
        print(f"- {key}: {val['description']}")
    print("- plugin_ioc: Scan an IOC using enabled plugins")
    print("- help: Show this help message.")
    print("- exit: Exit the session.")


if __name__ == '__main__':
    print("Welcome to the LLM Interactive Console!")
    display_help()

    commands = list(MODEL_MAP_OBJ.keys()) + ['plugin_ioc', 'help', 'exit']
    completer = WordCompleter(commands)

    while True:
        command = prompt("Enter command: ", completer=completer).lower().strip()
        if command == 'exit':
            break
        elif command == 'help':
            display_help()
        elif command == 'plugin_ioc':
            user_ioc = prompt("Enter an IP, URL, or Hash to check with plugins: ").strip()
            if user_ioc:
                results = run_plugins(user_ioc)
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{user_ioc}_{timestamp}.json"
                filepath = os.path.join(EVIDENCE_DIR, filename)
                with open(filepath, 'w') as ef:
                    json.dump(results, ef, indent=2)

                print("\n=== Plugin Scan Summary ===")
                for plugin, res in results.items():
                    status = 'Error' if 'error' in res else 'OK'
                    summary = res.get('error') or str(res.get('result'))[:100] + ('...' if len(str(res.get('result')))>100 else '')
                    print(f"{plugin}: {status} - {summary}")
                print(f"\nFull results saved to: {filepath}\n")
        elif command in MODEL_MAP_OBJ:
            cfg = MODEL_MAP_OBJ[command]
            user_q = prompt(f"Ask {cfg['description']}: ")
            if user_q:
                if command == 'rag_explorer':
                    out = ask_rag_only(cfg['llm'], user_q)
                elif command == 'unified_analyst':
                    out = ask_ollama_with_rag(cfg['llm'], user_q)
                else:
                    out = ask_ollama(cfg['llm'], user_q)
                print("Response:\n", out)
        else:
            print("Invalid command. Type 'help' for options.")

    print("Exiting.")
