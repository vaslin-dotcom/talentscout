import json
from chatbot import ask_groq, split_question_response
from extract import extract_candidate_fields
from utils import update_candidate_info
from candidate_state import candidate_info, required_fields
from summary import generate_proficiency_summary
import os

def main():
    chat_history = [
        {
            "role": "system",
            "content": (
                "You are TalentScout, an AI Hiring Assistant chatbot for a tech recruitment agency. "
                "Greet candidates, gather their basic details (name, email, phone, years of experience, desired position, location, skills),convince them to provide the only the following details alone (name, email, phone, years of experience, desired position, location, tech stack) untill they provide it"
                "End the conversation when the user says 'exit', 'bye', or 'quit'. Keep the tone professional but friendly."
            )
        }
    ]

    print("🧠 TalentScout AI Hiring Assistant\n(Type 'exit' anytime to end)\n")

    while any(candidate_info[f] is None for f in required_fields):
        user_input = input("👤 You: ")

        if user_input.lower() in ["exit", "quit", "bye"]:
            print("👋 Ending...")
            return

        chat_history.append({"role": "user", "content": user_input})
        bot_reply = ask_groq(chat_history)
        chat_history.append({"role": "assistant", "content": bot_reply})
        print("🤖 TalentScout:", bot_reply)

        parsed_data = extract_candidate_fields(user_input)
        update_candidate_info(parsed_data)

        missing_fields = [field for field in required_fields if not candidate_info.get(field)]
        if missing_fields:
            print("Let's collect the data before moving on.")
            continue
        else:
            print("✅ Thank you! I have all the details now.\n")
            print("Let's begin the technical interview...")
            break

    stack = candidate_info["tech_stack"]
    chat_history = [
        {"role": "system", "content": (
            f"You are a friendly and intelligent technical interviewer. Ask 1 question at a time based on the candidate’s tech stack ({stack}). "
            f"The candidate is a fresher. Ask coding, theory, or real-world application questions. Do not repeat questions. "
            f"After each question, wait for the answer before asking the next one."
            f"Respond in this exact format :\n\n"
            "Compliment: <short one-liner to motivate candidate>\n"
            "Question: <the actual technical question>"
        )}
    ]

    user_answers = []

    for i in range(5):
        chat_history.append({"role": "user", "content": f"Ask question {i+1} for the interview."})
        response = ask_groq(chat_history).strip()
        compliment, question = split_question_response(response)

        if compliment:
            print(f"💬 {compliment}")
            print(f"❓ Question {i+1}: {question}")
        else:
            print(f"❓ Question {i+1}: {response}")
            question = response

        answer = input("👤 Your Answer: ").strip()
        user_answers.append({"question": question, "answer": answer})
        chat_history.append({"role": "assistant", "content": question})
        chat_history.append({"role": "user", "content": answer})

    candidate_info["responses"] = user_answers
    print("🤝 Thank you for your time! It was great learning more about you.")

    summary = generate_proficiency_summary(user_answers)
    candidate_info["proficiency_summary"] = summary

    os.makedirs("profiles", exist_ok=True)
    filename = f"profiles/{candidate_info['name'].replace(' ', '_')}_profile.json"
    with open(filename, "w") as f:
        json.dump(candidate_info, f, indent=4)

    print(f"\n✅ Candidate data saved to {filename}")

if __name__ == "__main__":
    main()
