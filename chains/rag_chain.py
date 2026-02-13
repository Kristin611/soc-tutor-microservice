# this code builds the RAG chain with prompts and retriever
import textwrap
from langchain.prompts import PromptTemplate
from langchain.chains import ConversationalRetrievalChain
from prompts import chat_history_prompt, qa_prompt

def build_qa_chain(llm, retriever):
    return ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        condense_question_prompt=chat_history_prompt,
        combine_docs_chain_kwargs={'prompt': qa_prompt},
        return_source_documents=True
    )