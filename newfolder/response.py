from data.data import RESPONSES, KEYWORDS # type: ignore

def match_keyword(text: str):
    text = text.lower()
    for intent, keywords in KEYWORDS.items():
        if any(kw in text for kw in keywords):
            return intent
    return None

def build_response(intent: str, username: str = "there"):
    response = RESPONSES.get(intent)
    if not response:
        return "🧐 I heard you, but I'm not sure how to respond.", None

    if callable(response):
        return response(), None
    elif isinstance(response, dict):
        text_func = response.get("text")
        keyboard = response.get("keyboard")

        if callable(text_func):
            if intent == "greet":
                return text_func(username), keyboard
            return text_func(), keyboard
        else:
            return text_func, keyboard
    return str(response), None