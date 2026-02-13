import textwrap
from langchain.prompts import PromptTemplate

summary_prompt = PromptTemplate(
    input_variables=['context'],
    template=textwrap.dedent("""
        You are an assistant that helps users understand information efficiently.
        
        Based on the following context, return a summary in **valid JSON format** using this schema:

        {{
          "topic": "<main topic discussed>",
          "key_points": [
            "<bullet point 1>",
            "<bullet point 2>",
            "<bullet point 3>"
          ]
        }}

        Do not include any explanation or extra text. Only return valid JSON.
        Ensure any quotation marks in the content are escaped properly.

        CONTEXT:
        {context}
                             
    """)
)