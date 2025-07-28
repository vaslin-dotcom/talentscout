import json
import streamlit as st
from groq import Groq

# Replace this with your actual Groq API key
groq_api_key = "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"
client = Groq(api_key=groq_api_key)

def ask_groq(messages):
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=messages,
        temperature=0.7
    )
    return response.choices[0].message.content.strip()

required_fields = [
    "name", "email", "phone", "experience",
    "desired_position", "location", "tech_stack"
]

# Initialize session state
if "candidate_info" not in st.session_state:
    st.session_state.candidate_info = {field: None for field in required_fields}
    st.session_state.candidate_info["responses"] = []
    st.session_state.candidate_info["proficiency_summary"] = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "system", "content": (
            "You are TalentScout, an AI Hiring Assistant chatbot for a tech recruitment agency. "
            "Greet candidates, gather their basic details (name, email, phone, years of experience, desired position, location, skills), "
            "convince them to provide the only the following details alone (name, email, phone, years of experience, desired position, location, tech stack) "
            "until they provide it. End the conversation when the user says 'exit', 'bye', or 'quit'. "
            "Keep the tone professional but friendly."
        )}
    ]

if "phase" not in st.session_state:
    st.session_state.phase = "collect"
    st.session_state.user_answers = []
    st.session_state.finished = False

if "question_index" not in st.session_state:
    st.session_state.question_index = 0

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
        return json.loads(response)
    except json.JSONDecodeError:
        st.warning("⚠️ JSON parsing failed. Please try again.")
        return {}

def update_candidate_info(parsed_data):
    for key in st.session_state.candidate_info:
        if key in parsed_data and st.session_state.candidate_info[key] is None:
            st.session_state.candidate_info[key] = parsed_data[key]

st.title("I am TalentScout AI Hiring Assistant.\nI am here to collect your data and evaluate ur proficiency in yor tech stack")

# Display chat history
for msg in st.session_state.chat_history[1:]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if not st.session_state.finished:
    user_input = st.chat_input("👤 You: ")
    if user_input:
        st.chat_message("user").markdown(user_input)

        if user_input.lower() in ["exit", "quit", "bye"]:
            st.session_state.finished = True
            st.chat_message("assistant").markdown("👋 Ending... Thank you!")
        else:
            if st.session_state.phase == "collect":
                st.session_state.chat_history.append({"role": "user", "content": user_input})
                bot_reply = ask_groq(st.session_state.chat_history)
                st.session_state.chat_history.append({"role": "assistant", "content": bot_reply})
                st.chat_message("assistant").markdown(bot_reply)

                parsed_data = extract_candidate_fields(user_input)
                update_candidate_info(parsed_data)

                if all(st.session_state.candidate_info[f] for f in required_fields):
                    st.session_state.phase = "interview"
                    st.session_state.chat_history = [
                        {"role": "system", "content": (
                            f"You are a friendly and intelligent technical interviewer. Ask 1 question at a time based on the candidate’s tech stack ({st.session_state.candidate_info['tech_stack']}). "
                            f"The candidate is a fresher. Ask coding, theory, or real-world application questions. Do not repeat questions. "
                            f"After each question, wait for the answer before asking the next one."
                        )}
                    ]
                    st.chat_message("assistant").markdown("✅ Thank you! I have all the details now.\n\nLet's begin the technical interview...")

            elif st.session_state.phase == "interview":
                if len(st.session_state.user_answers) < st.session_state.question_index:
                    st.session_state.user_answers.append(user_input)
                    st.session_state.chat_history.append({"role": "user", "content": user_input})

                if st.session_state.question_index < 5:
                    i = st.session_state.question_index
                    st.session_state.chat_history.append({"role": "user", "content": f"Ask question {i+1} for the interview."})
                    response = ask_groq(st.session_state.chat_history)

                    st.chat_message("assistant").markdown(f" {response}")
                    st.session_state.chat_history.append({"role": "assistant", "content": response})

                    st.session_state.question_index += 1
                else:
                    st.session_state.phase = "summary"

            elif st.session_state.phase == "summary":
                user_answers = []
                for i in range(5):
                    answer = st.session_state.user_answers[i] if i < len(st.session_state.user_answers) else ""
                    qindex = 2*i + 1
                    question = ""
                    if qindex < len(st.session_state.chat_history):
                        question = st.session_state.chat_history[qindex].get("content", "")
                    user_answers.append({"question": question, "answer": answer})

                st.session_state.candidate_info["responses"] = user_answers

                user_text = "\n".join(f"Q: {item['question']}\nA: {item['answer']}" for item in user_answers)
                summary_prompt = [
                    {"role": "system", "content": (
                        "You are a hiring expert. Write a short summary (3–5 lines) about the candidate's technical proficiency "
                        "based on their answers. Be fair, objective, and concise and also evaluate them considering them as freshers with lesser experience."
                    )},
                    {"role": "user", "content": user_text}
                ]
                summary = ask_groq(summary_prompt)
                st.session_state.candidate_info["proficiency_summary"] = summary

                filename = f"{st.session_state.candidate_info['name'].replace(' ', '_')}_profile.json"
                with open(filename, "w") as f:
                    json.dump(st.session_state.candidate_info, f, indent=4)

                st.chat_message("assistant").markdown(
                    "\n🤝 Thank you for your time! It was great learning more about you.\nYour responses have been recorded and will be reviewed shortly.  \nWe’ll get back to you soon with the next steps.\nHave a great day and best of luck! 🌟\n💾 Data saved successfully."
                )
                st.session_state.finished = True
