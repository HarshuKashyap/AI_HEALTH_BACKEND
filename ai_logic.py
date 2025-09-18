import logging
from rapidfuzz import fuzz
from ai_openai import ask_openai  # OpenAI call + language detect

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# ------------------- Knowledge Base -------------------
CONDITIONS_DB = {
    "fever": {"keywords": ["fever", "temperature", "bukhar", "bhukhar"], "conditions": ["Common Cold", "Flu", "Malaria"]},
    "headache": {"keywords": ["headache", "sir dard", "migraine"], "conditions": ["Migraine", "Tension Headache", "Stress"]},
    "cough": {"keywords": ["cough", "khansi", "sardi"], "conditions": ["Common Cold", "Bronchitis", "Asthma"]}
}

# ------------------- KB search -------------------
def search_kb(user_input: str):
    for condition, data in CONDITIONS_DB.items():
        for keyword in data["keywords"]:
            score = fuzz.ratio(user_input.lower(), keyword.lower())
            if score > 70:
                return "Possible conditions:\n" + "\n".join(data['conditions'])
    return None

# ------------------- Main Answer Function -------------------
def get_answer(user_input: str):
    try:
        kb_answer = search_kb(user_input)
        if kb_answer:
            return kb_answer
        else:
            answer = ask_openai(user_input)
            return "\n".join([line.strip() for line in answer.splitlines() if line.strip() != ""])
    except Exception as e:
        import traceback
        print("get_answer error:", traceback.format_exc())  # terminal me full error show hoga
        return "Sorry, backend failed. Check logs."
