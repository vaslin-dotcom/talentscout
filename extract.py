import json
from chatbot import ask_groq

def extract_candidate_fields(user_input):
    prompt = [
        {"role": "system", "content": (
            "You are a JSON parser. Extract the following keys from user text: "
            "name, email, phone, experience, desired_position, location, tech_stack. "
            "Return only a valid JSON object with those keys and string values or null if missing. Do NOT explain anything."
        )},
        {"role": "user", "content": user_input}
    ]
    response = ask_groq(prompt)
    try:
        data = json.loads(response)
        return data
    except json.JSONDecodeError:
        print("Sorry for inconvenience please enter the details again")
        return {}
