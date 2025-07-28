from groq import Groq

groq_api_key = "**********"
client = Groq(api_key=groq_api_key)

def ask_groq(messages):
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=messages,
        temperature=0.7
    )
    return response.choices[0].message.content.strip()

def split_question_response(response: str):
    compliment = ""
    question = ""

    for line in response.strip().split('\n'):
        if line.startswith("Compliment:"):
            compliment = line.replace("Compliment:", "").strip()
        elif line.startswith("Question:"):
            question = line.replace("Question:", "").strip()

    return compliment, question
