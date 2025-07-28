import re

def split_question_response(response: str):
    compliment = ""
    question = ""

    for line in response.strip().split('\n'):
        if line.startswith("Compliment:"):
            compliment = line.replace("Compliment:", "").strip()
        elif line.startswith("Question:"):
            question = line.replace("Question:", "").strip()

    return compliment, question

def safe_filename(name):
    return re.sub(r'\W+', '_', name)
