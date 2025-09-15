# ai_logic.py
from typing import Dict, Any, List

# simple keyword -> condition map
CONDITION_KEYWORDS = {
    "flu": ["fever", "body ache", "chills", "muscle pain", "sore throat"],
    "common cold": ["runny nose", "sneeze", "sneezing", "sore throat", "stuffy nose"],
    "covid-like": ["loss of taste", "loss of smell", "shortness of breath", "fever", "cough"],
    "migraine": ["severe headache", "throbbing headache", "sensitivity to light", "nausea"],
    "indigestion": ["stomach pain", "bloating", "acid reflux", "heartburn"],
    "food poisoning": ["vomiting", "diarrhea", "stomach pain", "fever"],
    "asthma attack": ["wheezing", "shortness of breath", "difficulty breathing"],
    "chest emergency": ["chest pain", "pressure in chest", "pain radiating to arm/jaw"],
}

# symptoms that require immediate care
DANGER_KEYWORDS = [
    "chest pain", "difficulty breathing", "shortness of breath", "loss of consciousness",
    "severe bleeding", "sudden weakness", "slurred speech"
]

def analyze_symptoms(text: str) -> Dict[str, Any]:
    txt = text.lower()
    hits: Dict[str, int] = {}
    matched_keywords: List[str] = []

    # count matches per condition
    for cond, kws in CONDITION_KEYWORDS.items():
        for kw in kws:
            if kw in txt:
                hits[cond] = hits.get(cond, 0) + 1
                matched_keywords.append(kw)

    # rank probable conditions
    probable = sorted(hits.items(), key=lambda x: x[1], reverse=True)
    probable_conditions = [p[0] for p in probable] if probable else []

    # severity detection
    severity = "low"
    for danger in DANGER_KEYWORDS:
        if danger in txt:
            severity = "high"
            break
    # if many matched keywords, mark moderate
    if severity != "high" and len(matched_keywords) >= 3:
        severity = "moderate"

    # advice generation (simple templating)
    if severity == "high":
        advice = ("Symptoms indicate potentially serious condition. Seek immediate medical attention "
                  "(visit ER / call emergency services). Do not ignore these symptoms.")
    elif probable_conditions:
        # give condition-based advice for top 1-2 conditions
        top = probable_conditions[:2]
        adv_list = []
        for cond in top:
            if cond in ("flu", "covid-like"):
                adv_list.append("Rest, hydrate, paracetamol for fever; isolate if covid suspected; consult doctor for testing.")
            elif cond == "common cold":
                adv_list.append("Rest, fluids, warm saline gargle for sore throat; OTC cold medicines if needed.")
            elif cond == "migraine":
                adv_list.append("Rest in dark room, avoid triggers; take migraine medication if prescribed; see physician if new/worse.")
            elif cond == "indigestion":
                adv_list.append("Avoid oily/spicy foods, use antacids, eat light; consult if pain severe or persistent.")
            elif cond == "food poisoning":
                adv_list.append("Hydrate (ORS), avoid solid food until vomiting stops; see doctor if severe or high fever.")
            elif cond == "asthma attack":
                adv_list.append("Use inhaler (if available) and seek urgent care if breathing worsens.")
            elif cond == "chest emergency":
                adv_list.append("This might be an emergency — seek immediate medical help (call ambulance).")
            else:
                adv_list.append("Rest and monitor symptoms; consult doctor if it persists.")
        advice = " ".join(adv_list)
    else:
        advice = "Not enough specific symptoms detected. Please provide more details (duration, severity, other symptoms)."

    recommendations = []
    if severity == "high":
        recommendations.append("Go to nearest emergency room or call emergency services.")
    else:
        recommendations.append("Rest and hydrate.")
        recommendations.append("Monitor symptoms for 24-48 hours; if worsening, consult a doctor.")

    return {
        "advice": advice,
        "probable_conditions": probable_conditions,
        "severity": severity,
        "recommendations": recommendations,
        "matched_keywords": matched_keywords
    }
