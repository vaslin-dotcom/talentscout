import json
import os
import streamlit as st
from chatbot import ask_groq, split_question_response
from extract import extract_candidate_fields
from utils import update_candidate_info
from candidate_state import candidate_info, required_fields
from summary import generate_proficiency_summary

st.set_page_config(page_title="TalentScout AI", page_icon="🤖", layout="centered")
st.title("🤖 TalentScout - AI Hiring Assistant")

# Initialize session state for first run
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [{
        "role": "system",
        "content": (
            "You are TalentScout, an AI Hiring Assistant chatbot for a tech recruitment agency. "
            "Greet candidates, gather their basic details (name, email, phone, years of experience, desired position, location, skills). "
            "Convince them to provide **only** the following details: name, email, phone, experience, desired position, location, tech stack. "
            "End the conversation when the user says 'exit', 'bye', or 'quit'. Keep the tone professional but friendly."
        )
    }]
    st.session_state.phase = "collect"
    st.session_state.user_answers = []
    st.session_state.q_index = 0
    st.session_state.finished = False

# Display full chat history like a conversation scroll
st.markdown("### 💬 Chat History")
for msg in st.session_state.chat_history:
    if msg["role"] == "user":
        st.markdown(f"👤 **You**: {msg['content']}")
    elif msg["role"] == "assistant":
        st.markdown(f"🤖 **TalentScout**: {msg['content']}")

# PHASE 1: Collect Details
if st.session_state.phase == "collect" and not st.session_state.finished:
    st.subheader("📋 Please provide your details")
    user_input = st.text_input("Your message:", key="profile_input")

    if user_input:
        if user_input.lower().strip() in ["exit", "quit", "bye"]:
            st.warning("👋 Ending the conversation...")
            st.session_state.finished = True
        else:
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            bot_reply = ask_groq(st.session_state.chat_history)
            st.session_state.chat_history.append({"role": "assistant", "content": bot_reply})
            st.rerun()

        # Update candidate info from input
        parsed_data = extract_candidate_fields(user_input)
        update_candidate_info(parsed_data)

        # Check if all required fields are filled
        missing_fields = [f for f in required_fields if not candidate_info.get(f)]
        if not missing_fields:
            st.success("✅ Thank you! I have all the details now.")
            st.session_state.phase = "interview"
            st.rerun()

# PHASE 2: Interview
elif st.session_state.phase == "interview":
    st.subheader("💼 Technical Interview")

    stack = candidate_info["tech_stack"]
    if st.session_state.q_index == 0 and "interview_system_prompt" not in st.session_state:
        st.session_state.chat_history = [{
            "role": "system",
            "content": (
                f"You are a friendly and intelligent technical interviewer. Ask 1 question at a time based on the candidate’s tech stack ({stack}). "
                f"The candidate is a fresher. Ask coding, theory, or real-world application questions. Do not repeat questions. "
                f"After each question, wait for the answer before asking the next one.\n"
                f"Respond in this exact format:\n\n"
                f"Compliment: <short one-liner to motivate candidate>\n"
                f"Question: <the actual technical question>"
            )
        }]
        st.session_state.interview_system_prompt = True

    if st.session_state.q_index < 5:
        if "current_question" not in st.session_state:
            st.session_state.chat_history.append({
                "role": "user",
                "content": f"Ask question {st.session_state.q_index + 1} for the interview."
            })
            response = ask_groq(st.session_state.chat_history).strip()
            compliment, question = split_question_response(response)
            st.session_state.current_question = question or response
            st.session_state.compliment = compliment

        if st.session_state.compliment:
            st.markdown(f"💬 *{st.session_state.compliment}*")
        st.markdown(f"❓ **Question {st.session_state.q_index + 1}:** {st.session_state.current_question}")

        answer = st.text_input("Your Answer:", key=f"answer_{st.session_state.q_index}")
        if answer:
            st.session_state.user_answers.append({
                "question": st.session_state.current_question,
                "answer": answer.strip()
            })
            st.session_state.chat_history.append({"role": "assistant", "content": st.session_state.current_question})
            st.session_state.chat_history.append({"role": "user", "content": answer.strip()})
            st.session_state.q_index += 1
            del st.session_state.current_question
            del st.session_state.compliment
            st.rerun()
    else:
        st.success("✅ Interview complete!")
        st.session_state.phase = "summary"
        st.rerun()

# PHASE 3: Summary
elif st.session_state.phase == "summary":
    st.subheader("📊 Candidate Summary")
    candidate_info["responses"] = st.session_state.user_answers
    summary = generate_proficiency_summary(st.session_state.user_answers)
    candidate_info["proficiency_summary"] = summary

    st.markdown("### 📝 Proficiency Summary")
    st.markdown(summary)

    os.makedirs("profiles", exist_ok=True)
    filename = f"profiles/{candidate_info['name'].replace(' ', '_')}_profile.json"
    with open(filename, "w") as f:
        json.dump(candidate_info, f, indent=4)

    st.success(f"✅ Candidate data saved to `{filename}`")

    st.session_state.finished = True

# Final Goodbye Message
if st.session_state.finished:
    st.markdown("🎉 **Thank you for using TalentScout!**\nWe'll get back to you shortly.")
