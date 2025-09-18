import json

# KB file load
with open("kb_data.json", "r", encoding="utf-8") as f:
    kb_data = json.load(f)

def query_health(user_message: str) -> str:
    user_message = user_message.lower()
    for entry in kb_data:
        if entry["topic"].lower() in user_message:
            return entry["text"]
    return None
