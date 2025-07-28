#  TalentScout – AI Hiring Assistant

TalentScout is an intelligent AI-powered chatbot designed to automate the initial screening process in tech hiring. Built with Streamlit and powered by Groq’s LLaMA 3 LLM, the assistant gathers candidate information, asks technical questions based on their declared tech stack, and generates a professional summary — all through an interactive chat interface.

> Hosted and run on an AWS EC2 instance. All candidate data is securely stored in structured JSON format for future review.

---

##  Features

- ✅ Interactive chatbot UI using **Streamlit**
- ✅ Dynamic question generation using **Groq’s LLaMA 3 model**
- ✅ Intelligent parsing of candidate details using **prompt-driven extraction**
- ✅ Adaptive questioning based on declared **tech stack**
- ✅ Summary generation of candidate proficiency for recruiter use
- ✅ Local **JSON-based data storage** of candidate responses
- ✅ Hosted via **AWS EC2** (terminal-based access)

---

##  Tech Stack

| Layer           | Tech Used                     |
|----------------|-------------------------------|
| Frontend       | Streamlit                     |
| LLM Backend    | Groq API (LLaMA3-8B-8192)     |
| Language       | Python 3                      |
| Hosting        | AWS EC2 (Ubuntu 22.04)        |
| Data Storage   | Local JSON Files              |

---

## How It Works

### Phase 1: Information Gathering

- Candidate is prompted to provide:
  - Name
  - Email
  - Phone
  - Experience
  - Desired Position
  - Location
  - Tech Stack (e.g., Python, Django, React)

###  Phase 2: Technical Interview

- Based on the tech stack, the bot asks **5 unique technical questions**
- Each answer is saved and added to the candidate’s record

###  Phase 3: Summary Generation

- The candidate’s answers are fed back into the LLM
- A concise summary is generated and stored with the record

### Final Step: Save JSON

- All information is stored locally as `<candidate_name>_profile.json`

---

##  Deployment Instructions

###  Prerequisites

- Python 3.9+
- Streamlit
- Groq API key (you can get it from https://console.groq.com)
- AWS EC2 instance (Ubuntu recommended)

###  Installation

```bash
# Clone the repo
git clone https://github.com/vaslin-dotcom/talentscout.git
cd talentscout

# Set up Python environment (optional but recommended)
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
