**TalentScout AI Hiring Assistant**


**_Project Overview_**

TalentScout AI Hiring Assistant is an interactive chatbot built with Streamlit and powered by LLMs via Groq API. It simulates an intelligent recruiter that:
Gathers essential candidate information (name, email, phone, etc.)
Asks tailored technical questions based on the candidate’s tech stack
Generates a summary of the candidate’s proficiency
Saves the collected information and responses securely in a .json file
This tool helps automate the preliminary screening process in tech recruitment.



**_Installation Instructions_**

1.Clone the Repository

    git clone https://github.com/vaslin-dotcom\n
    cd talentscout

2. Set up a virtual environment (optional but recommended)

     python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

3. Install Dependencies

      pip install -r requirements.txt

4. Add Groq API Key
    In the Python file, replace the placeholder with your actual Groq key:
groq_api_key = "your_actual_groq_api_key"

5. Run the App

    streamlit run app.py


**_Usage Guide_**

The chatbot opens with a greeting and asks you for key details like your name, email, tech stack, etc.
Once all required information is collected, it begins a technical interview with 5 questions tailored to your tech stack.
Your responses are recorded.
The system generates a brief summary of your proficiency (not shown to you) and saves all your data in a .json file.



**_Technical Details_**

Frontend: Streamlit
Backend Model: llama3-8b-8192 via Groq API
Language: Python 3
File Storage: Responses saved locally in JSON format
State Management: Streamlit’s st.session_state


**_Prompt Design_**

For Candidate Info Extraction:

You are a JSON parser. Extract the following keys from user text: name, email, phone, experience, desired_position, location, tech_stack...

For Technical Questions:

You are a friendly and intelligent technical interviewer. Ask 1 question at a time based on the candidate’s tech stack...

For Summary Generation:

You are a hiring expert. Write a short summary (3–5 lines) about the candidate's technical proficiency...

These prompts ensure controlled, context-aware behavior from the model.



**_Challenges & Solutions_**

Challenge	Solution
LLM sometimes returned malformed JSON	Designed a prompt to strictly return JSON only
Maintaining chat context across Streamlit reruns	Used st.session_state effectively
Splitting bot replies into compliment/question wasn't robust	Simplified logic by printing full response directly
Avoiding repetition and managing user phases	Used phase and question_index in session state

**_Deployment_ **

This code is being deployed in aws EC2 and whenever somone tries to fill the data, their details will be stired in aws

**_requirements.txt_**

streamlit
groq
