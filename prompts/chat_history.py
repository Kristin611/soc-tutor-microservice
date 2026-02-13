import textwrap
from langchain.prompts import PromptTemplate 

chat_history_prompt = PromptTemplate(
    input_variables=['question', 'chat_history'],
        template=textwrap.dedent("""
            Given the following conversation and a follow-up question, rephrase the follow-up question to be a standalone question.

            Chat History:
            {chat_history}

            Follow-Up Question:
            {question}

            Standalone Question:
        """)
)