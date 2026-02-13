# this code file handles LLM instantiation via Ollama
from langchain_ollama import OllamaLLM

def get_mistral_llm():
    return OllamaLLM(model='mistral')
