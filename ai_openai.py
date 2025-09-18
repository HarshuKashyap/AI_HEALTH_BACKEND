import os
from openai import OpenAI
from dotenv import load_dotenv
from language_detect import detect_language

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def ask_openai(user_input: str) -> str:
    lang = detect_language(user_input)
    
    if lang == 'hi':
        system_prompt = (
            "You are a helpful health assistant. "
            "Always reply in clean, easy-to-read Hindi. "
            "Do NOT use Markdown symbols, hashtags, or dashes. "
            "Use line breaks for new points like in a list."
        )
    else:
        system_prompt = (
            "You are a helpful health assistant. "
            "Always reply in clean, easy-to-read English. "
            "Do NOT use Markdown symbols, hashtags, or dashes. "
            "Use line breaks for new points like in a list."
        )

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Sorry, I could not process your query right now: {e}"
