# AI-Powered Student Assistant App

A **Streamlit-based learning assistant** that uses Hugging Face AI models to summarize topics, explain concepts, generate practice questions, and create quizzes. This app provides an interactive, personalized learning experience for students.

---

## Features

* Summarizes any topic in simple language
* Explains concepts clearly with examples
* Generates practice questions and quizzes
* Interactive chatbot for personalized learning
* Secure API key management using `.env` file

---

## Tech Stack

* **Frontend:** Streamlit
* **Backend / AI:** Hugging Face Transformers API
* **Language:** Python
* **Environment Variables:** `.env` file for API keys

---

## Setup Instructions

1. **Clone the repository**

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Create a `.env` file**
   Copy `.env.example` and add your Hugging Face API key:

```bash
cp .env.example .env
```

Update `.env` with your API key:

```
HUGGINGFACE_API_KEY=your_actual_api_key_here
```

4. **Run the app**

```bash
streamlit run app.py
```

---

## Folder Structure

```
AI-Student-Assistant/
├── app.py
├── requirements.txt
├── .gitignore
├── .env.example
└── README.md
```

