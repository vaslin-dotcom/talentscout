from chatbot import ask_groq

def generate_proficiency_summary(user_answers):
    user_text = "\n".join(
        f"Q: {item['question']}\nA: {item['answer']}" for item in user_answers
    )

    summary_prompt = [
        {"role": "system", "content": (
            "You are a hiring expert. Write a short summary (3–5 lines) about the candidate's technical proficiency "
            "based on their answers. Be fair, objective, and concise."
        )},
        {"role": "user", "content": user_text}
    ]

    summary = ask_groq(summary_prompt)
    return summary.strip()
