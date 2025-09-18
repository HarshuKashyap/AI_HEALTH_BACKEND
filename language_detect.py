from langdetect import detect, DetectorFactory

DetectorFactory.seed = 0  # deterministic

def detect_language(text: str) -> str:
    try:
        return detect(text)  # 'en', 'hi', etc.
    except:
        return 'en'
