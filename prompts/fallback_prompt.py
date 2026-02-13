import textwrap
from langchain.prompts import PromptTemplate

fallback_prompt = PromptTemplate(
    input_variable=['question'],
    template=textwrap.dedent("""
        The system could not find relevant content in the document to answer the user's question.

        Please respond politely, letting the user know that based on the provided document context, 
        an answer could not be generated. Do not attempt to answer the question from general knowledge. 
        You may invite the user to rephrase or ask a different question more aligned with the document.
                             
        USER QUESTION:
        {question}
                             
        ASSISTANT RESPONSE:
    """)
)