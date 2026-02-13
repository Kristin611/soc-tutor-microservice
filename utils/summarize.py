from langchain_core.language_models.base import BaseLanguageModel
from prompts.summary_prompt import summary_prompt
import json

def summarize_chat_history(llm, chat_history, max_turns=3):
    if not chat_history:
        return "There's no recent chat history to summarize."
    
    recent_turns = chat_history[-max_turns:]

    # format into a readable string
    formatted_history = "\n\n".join(
        f"User: {q}\nBot: {a}" for q, a in recent_turns if q and a
    )

    prompt = summary_prompt.format(context=formatted_history)
    summary = llm.invoke(prompt)

    # parse json
    try: 
        return json.loads(summary)
    except json.JSONDecodeError as e:
        return {
            'error': 'LLM returned invalid JSON', 
            'details': str(e), 
            'raw': summary
        }