from typing import List, Tuple, Optional # allows you to specify that a value can be one of multiple types--in this case either str or None
from fastapi import FastAPI # class used to create web application
from pydantic import BaseModel
from retrievers.vector_retriever import get_vector_retriever 
from llms.mistral_llm import get_mistral_llm
from chains.rag_chain import build_qa_chain
from prompts.fallback_prompt import fallback_prompt
from utils.summarize import summarize_chat_history

app = FastAPI() # creates an instance of the FastAPI app: the app object is the main entry point of your web app. FastAPI uses it to register routes (endpoints) and handle HTTP requests

# classes ensure validation by checking incoming data types and required fields & fastapi uses these models to generate interactive api docs (swaggerUI) automatically. also vscode can help with autocomplete and typechecks

# Pydantic model for Ask Request: defines the structure of the JSON data the /ask endpoint expects in the POST request body. It basically says the request must have a question field of type string and may optionally include a chat_history field so React frontend can send context or not
class AskRequest(BaseModel):
    question: str
    chat_history: Optional[List[Tuple[str, str]]] = None

# Pydantic model for Ask Response: defines the structure of the JSON data the /ask endpoint will send back as a response. It says the response JSON will contain a single field answer which is a string.
class AskResponse(BaseModel):
    answer: str   

# Pydantic model for Summarize Request:
class SummarizeRequest(BaseModel):
    chat_history: List[Tuple[str, str]]

# Pydantic model for Summarize Response:      
class SummarizeResponse(BaseModel):
    summary: dict # this will contain the JSON returned by summarize_chat_history  

# initialize components once when app starts
retriever, embeddings = get_vector_retriever()
llm = get_mistral_llm()
qa_chain = build_qa_chain(llm, retriever)
MAX_HISTORY_TURNS = 3   

# functions are currently sync (instead of async) to match current llm api usage/setup
@app.post('/ask', response_model=AskResponse) # response will be automatically converted from AskResponse to JSON
def ask_endpoint(request: AskRequest): #incoming request body will be validated and parsed into an instance of AskRequest
    question = request.question # extracts the question str from the request
    chat_history = request.chat_history or [] # extracts chat_history from request; if none is provided it defaults to empty list
    trimmed_history = chat_history[-MAX_HISTORY_TURNS:]

    # calls qa_chain and invokes/returns a dictionary with the generated answer
    result = qa_chain.invoke({
        'question': question,
        'chat_history': trimmed_history
    })

    answer = result.get('answer', 'Sorry, no answer generated.') # extracts answer str from the result, and returns a fallback str if answer key is missing
    answer_lower = answer.lower() # normalizes the answer text to lowercase for simple keyword matching

    # fallback logic for low confidence answers
    low_confidence_phrases = [
        "i don't know",
        "i am not sure",
        "the context does not",
        "no relevant information"
    ]

    # checks if any low-confidence phrases appears in the answer. 
    if any(phrase in answer_lower for phrase in low_confidence_phrases):
        fallback_input = fallback_prompt.format(question=question)  #if yes, formats the fallback_prompt with the question
        fallback_answer = llm.invoke(fallback_input) # calls the llm directly with the fallback prompt to try for a better answer
        return AskResponse(answer=fallback_answer) # returns the fallback answer wrapped as an AskResponse
    
    # if not low-confidence phrase detected, returns the original answer wrapped as an AskResponse
    return AskResponse(answer=answer)

@app.post('/summarize', response_model=SummarizeResponse)
def summarize_endpoint(request: SummarizeRequest):
    chat_history = request.chat_history
    summary = summarize_chat_history(llm, chat_history) # summarize_chat_history handles trimming and MAX_TURNS internally so need need for that logic here
    return SummarizeResponse(summary=summary)



# health check route
@app.get('/health')
async def health_check():
    try:
        vectordb = retriever.vectorstore # access the underlying chroma object

        # using Chroma's API (len()) to retrieve active docs and count them; active meaning the ones retrievable by RAG app and does not include inactive vectors that are metadata, deleted, or otherwise. If you want all active and inactive vectors then use vectordb._collection.count()
        all_docs = vectordb.get()
        doc_count = len(all_docs)


        # DB status logic
        if doc_count == 0:
            db_status = 'warning: collection is empty'
        else:
            db_status = 'ok'    

        return {
            'api_status': 'ok',
            'db_status': 'ok',
            'document_count': doc_count,
            'embedding_model': embeddings.model_name
        }
    
    except Exception as e:

        return {
            "api_status": "ok",
            "db_status": f"error: {str(e)}",
            "document_count": None,
            "embedding_model": None
        }    
        
