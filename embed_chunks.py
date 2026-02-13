import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

def main():
    # path for chunk files and saved Chroma vector DB
    chunks_dir = 'data/chunks'

    print(f'READING FROM: {chunks_dir}')
    print('FILES FOUND:', os.listdir(chunks_dir))

    persist_directory = 'data/chroma_db'

    # load all text files from chunks_dir into a single list of LangChain documents that can be processed and embedded next.
    texts = [] # an empty list to store all the docs that will load
    # loop through each chunk.txt file
    for filename in sorted(os.listdir(chunks_dir)):
        if filename.endswith('.txt'):
            loader = TextLoader(os.path.join(chunks_dir, filename)) # use langchain's TextLoader to load one file
            doc = loader.load() # read the file and return a list of LangChain document objects
            texts.extend(doc) # add the document objects to the full texts list

    # use a basic splitter for safety (each chunk is already ~500 tokens); this step is optional but it makes sure that None of the chunks are too long, the embeddings don’t break due to unexpected length, and you stay within model limits
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=750, 
        chunk_overlap=150, # overlap slightly for context
        separators=["\n\n", "\n", ".", " "] # keeps sentence-level meaning intact
    )
    docs = splitter.split_documents(texts)

    # use huggingFace embedding model (this can be changed later): tells LangChain to use a HuggingFace model to turn each document into a vector (list of numbers).
    embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')

    # initialize empty chroma db with embeddings 
    vectordb = Chroma(
        collection_name='soc_chunks',
        embedding_function=embeddings,
        persist_directory=persist_directory # Save this vector DB to a local folder (data/chroma_db), so you don’t lose your work after the script exits.
    )

    # add documents to db 
    vectordb.add_documents(documents=docs)

    print(f"Vectorstore persisted to: {persist_directory}")

    


    print(f'Embedded {len(docs)} chunks and saved to {persist_directory}')

    
if __name__ == '__main__':
    main()        