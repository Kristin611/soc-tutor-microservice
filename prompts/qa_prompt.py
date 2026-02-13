import textwrap
from langchain.prompts import PromptTemplate

qa_prompt = PromptTemplate(
    input_variables=['context', 'question'], 
        template=textwrap.dedent("""
        You are a helpful assistant. Use ONLY the context provided to answer the user's question. 
        If the context does not contain the answer, simply say: "I don't know". Do not make up an answer.

        CONTEXT:
        {context}

        QUESTION:
        {question}
                                 
        ANSWER:
        """)
)