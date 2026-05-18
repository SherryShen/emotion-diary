# Healing Diary

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35+-red.svg)](https://streamlit.io)

An AI-powered healing diary for students to privately reflect on their feelings, track their mood over time, and receive psychological analysis from multiple frameworks.

**Live Demo:** [https://sherryshen-healing-diary.streamlit.app](https://sherryshen-healing-diary.streamlit.app)

---

## ✨ Features

- **PHQ-4 Mood Assessment** – Self-screen for anxiety and depression using a clinically validated questionnaire.
- **Mood Tracking** – Visualize your anxiety and depression scores over time with an interactive line chart.
- **AI Companion Chat** – Talk to a warm, empathetic AI companion anytime (powered by Groq API).
- **Multi-Perspective Psychological Analysis** – Get insight from five frameworks: Freud, Jung, Adler, CBT, and Humanistic.
- **Healing Diary** – All conversations and analyses are saved in your session as a private, scrollable diary.
- **Rational-User Button** – A dedicated “Analyze My Narrative” button for users who need cognitive understanding of their emotions.

---

## 🛠️ Tech Stack

- **Frontend & Backend**: Python, Streamlit
- **LLM API**: Groq (Llama 3.3‑70B)
- **Data Handling**: Pandas, local storage (session state)
- **Deployment**: Streamlit Community Cloud

---

## 🚀 Getting Started

### Prerequisites
- Python 3.11 or higher
- A Groq API key (free tier available at [console.groq.com](https://console.groq.com))

### Installation

1. Clone the repository
   ```bash
   git clone https://github.com/SherryShen/emotion-diary.git
   cd emotion-diary
Create and activate a virtual environment (optional but recommended)

bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
Install dependencies

bash
pip install -r requirements.txt
Set up your Groq API key

Create a file .streamlit/secrets.toml and add:

toml
GROQ_API_KEY = "your_gsk_api_key_here"
Alternatively, you can hardcode it in app.py (not recommended for public deployment).

Run the app

bash
streamlit run app.py
Open your browser at http://localhost:8501

📂 Project Structure
text
emotion-diary/
├── app.py                  # Main Streamlit application
├── requirements.txt        # Python dependencies
├── .streamlit/
│   └── secrets.toml        # API keys (ignored by git)
├── .gitignore              # Git ignore file
└── README.md               # This file
🔮 Future Improvements
Searchable timeline of past entries and conversations

Generate longitudinal reports for mental health professionals

Integrate brainwave‑informed music therapy

Provide acupressure guidance based on traditional Chinese medicine

🙋‍♀️ Contact
Sherry Shen – sherryshen818@gmail.com
GitHub: github.com/SherryShen
Live Demo: sherryshen-healing-diary.streamlit.app

🌟 Acknowledgments
Groq for providing fast, free LLM inference.

Streamlit for making full‑stack AI app development accessible.

The PHQ-4 scale for evidence‑based mental health screening.
