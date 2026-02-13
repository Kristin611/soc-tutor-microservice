#this code file handles vector DB and retriever logic
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

def get_vector_retriever(persist_directory='data/chroma_db', k=4):
    embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
    vectordb = Chroma(
        collection_name='soc_chunks',
        persist_directory=persist_directory,
        embedding_function=embeddings
    )
    retriever = vectordb.as_retriever(search_type='mmr', search_kwargs={'k' : k})
    return retriever, embeddings