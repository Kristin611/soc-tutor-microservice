import os
import textwrap 
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import OllamaLLM  
#from langchain.chains import RetrievalQA 
from langchain.chains import ConversationalRetrievalChain
from langchain.prompts import PromptTemplate
from similarity import cosine_similarity
from retrievers.vector_retriever import get_vector_retriever
from llms.mistral_llm import get_mistral_llm
from chains.rag_chain import build_qa_chain
from prompts import fallback_prompt, summary_prompt
from utils.summarize import summarize_chat_history

def main():

    # MODULARIZED CODE STARTS HERE

    retriever, embeddings = get_vector_retriever()
    llm = get_mistral_llm()
    qa_chain = build_qa_chain(llm, retriever)

    # initialize chat history and config
    # Stores only the last 3 (question, answer) pairs to keep memory usage low and reduce prompt size bloat.
    chat_history = []
    MAX_HISTORY_TURNS = 3

    # creates interative loop in terminal to chat with doc in real time
    print("Ask a question about your document (or type 'exit' to quit):") # lets user know they can start asking questions; only runs once before the loop starts
    while True: # creates infinite loop to keep running  until the user explicitly exits
        query = input("Your question: ") # prompts user to ask a question
        if query.lower() in ['exit', 'quit']:
            break 

        if query.lower() == 'summarize':
            summary = summarize_chat_history(llm, chat_history, max_turns=3)
            print("\n Summary of recent conversation:")
            print(summary)
            print("-" * 50)
            continue

        # avoid sending an empty question to the model    
        if not query.strip():
            print("Please ask a question or type 'exit' to quit.")
            continue

        trimmed_history = chat_history[-MAX_HISTORY_TURNS:]

        # the line, result = qa_chain.invoke({}), is calling the ConversationalRetrievalChain you set up earlier with your query and prior conversation turns. At his momemnt it Retrieves relevant chunks from your Chroma vector database, Passes the conversation history and current question through your custom prompt, Uses the LLM (Mistral via Ollama) to generate a response, and Returns both the generated answer and the exact chunks it used to generate that answer.
        # The invoke() method is the updated, preferred way to send input to a chain and get output
        result = qa_chain.invoke({
            "question": query, # user's current input
            "chat_history": trimmed_history # list of previous (question, answer) tuples
        })

        # This line extracts the actual generated text answer from the result dictionary
        answer = result['answer']
        # This pulls out the retrieved chunks that the retriever found most relevant to your query
        # sources = result.get('source_documents', [])
        
        answer_lower = answer.lower() # normalize answer for comparison

        # FALLBACK PROMPT LOGIC 

        # check for low-confidence signals in the LLM's answer
        low_confidence = any(phrase in answer_lower for phrase in [
            "i don't know",
            "i am not sure",
            "the context does not",
            "no relevant information",
        ])

        if low_confidence:
            formatted_prompt = fallback_prompt.format(question=query)
            fallback_answer = llm.invoke(formatted_prompt)
            print('FALLBACK ANSWER:', fallback_answer)
            answer = fallback_answer
        else:
            print("Answer:", answer) # print's the model's answer
            print("Retrieved CONTEXT CHUNKS:")

        # this loop prints out which documents were used in forming the answer
        # if sources:
        #     for i, doc in enumerate(sources, 1):
        #         print(f"\n--- Chunk {i} ---")
        #         print(doc.page_content.strip())
        # else:
        #     print('No documents were retrieved.')        
        # print("-" * 50) # prints a visual divider line to separate each Q&A pair visually

        # add to chat history: Adds the current Q&A turn to memory for the next loop.
        chat_history.append((query, answer))


if __name__ == '__main__':
    main()

