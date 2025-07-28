import streamlit as st
import json

from chatbot import ask_groq
from extract import extract_candidate_fields, update_candidate_info
from prompts import system_intro_prompt, technical_round_prompt
from candidate_state import init_candidate_info, required_fields
from utils import split_question_response, safe_filename
from summary import generate_proficiency_summary

# Initialize candidate info
candidate_info = init_candidate_info()

# Initialize chat history
chat_history = [system_intro_prompt()]

# Streamlit UI setup
st.set_page_config(page_title="TalentScout AI Hiring Assistant", layout="centered")
st.title("🧠 TalentScout - AI Hiring Assistant")
st.markdown("Welcome! I’ll collect your details and ask a few technical questions based on your tech stack.")

# Session state for persistence
if "step" not in st.session_state:
    st.session_state.step = "collecting"
if "messages" not in st.session_state:
    st.session_state.messages = []
if "answers" not in st.session_state:
    st.session_state.answers = []

# Chat UI function
def chat_bot_response(user_input):
    chat_history.append({"role": "user", "content": user_input})
    bot_reply = ask_groq(chat_history)
    chat_history.append({"role": "assistant", "content": bot_reply})
    return bot_reply

# Step 1: Collect Required Fields
if st.session_state.step == "collecting":
    missing_fields = [f for f in required_fields if candidate_info[f] is None]

    user_input = st.text_input("👤 You: Enter your details here (you can write naturally)")

    if user_input:
        if user_input.lower() in ["exit", "quit", "bye"]:
            st.write("👋 Ending conversation...")
            st.stop()

        bot_reply = chat_bot_response(user_input)
        st.markdown(f"🤖 TalentScout: {bot_reply}")

        parsed_data = extract_candidate_fields(user_input)
        update_candidate_info(parsed_data, candidate_info)

        remaining = [f for f in required_fields if candidate_info[f] is None]
        if remaining:
            st.warning("Please provide the remaining details: " + ", ".join(remaining))
        else:
            st.success("✅ Thank you! I have all the details now.")
            st.session_state.step = "interview"
            st.rerun()

# Step 2: Technical Questions
elif st.session_state.step == "interview":
    stack = candidate_info["tech_stack"]
    experience = candidate_info["experience"]
    level = "fresher" if "0" in experience or "fresh" in experience.lower() else "experienced"
    chat_history.clear()
    chat_history.append(technical_round_prompt(stack, level))

    num_questions = 5

    for i in range(num_questions):
        if len(st.session_state.answers) <= i:
            user_question_prompt = f"Ask question {i+1} for the interview."
            chat_history.append({"role": "user", "content": user_question_prompt})
            response = ask_groq(chat_history)

            compliment, question = split_question_response(response)
            st.markdown(f"💬 {compliment}")
            st.markdown(f"❓ **Question {i+1}:** {question}")

            answer = st.text_input(f"👤 Your Answer {i+1}:", key=f"answer_{i}")
            if answer:
                st.session_state.answers.append({"question": question, "answer": answer})
                chat_history.append({"role": "assistant", "content": question})
                chat_history.append({"role": "user", "content": answer})
                st.rerun()
            else:
                st.stop()

    # Step 3: Wrap up
    st.session_state.step = "summary"
    st.rerun()

# Step 3: Summary + Save
elif st.session_state.step == "summary":
    st.markdown("🤝 Thank you for completing the technical round!")
    candidate_info["responses"] = st.session_state.answers
    summary = generate_proficiency_summary(st.session_state.answers)
    candidate_info["proficiency_summary"] = summary

    st.markdown("### 📋 Proficiency Summary")
    st.markdown(summary)

    filename = f"profiles/{safe_filename(candidate_info['name'])}_profile.json"
    with open(filename, "w") as f:
        json.dump(candidate_info, f, indent=4)

    st.success(f"✅ Candidate data saved to `{filename}`")
    st.balloons()
    st.markdown("Thank you! We'll be in touch. 👋")
