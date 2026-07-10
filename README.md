# 🚀 AI Venture Studio

An intelligent **multi-agent startup consulting platform** built using **LangGraph**, **Google Gemini**, and **Streamlit**.

AI Venture Studio simulates a team of startup consultants by orchestrating multiple AI agents that collaboratively evaluate a startup idea, perform research, validate feasibility, assess risks, and generate an investor-ready pitch.

---

## ✨ Features

- 🧠 Supervisor (Venture Manager) Agent
- 📈 Market Research Agent
- 🏢 Competitor Analysis Agent
- 👥 Customer Research Agent
- 💼 Business Model Generator
- 🏗 Technical Architecture Validator
- ⚠ Risk Analysis Agent
- 🎤 Investor Pitch Deck Generator
- 🔄 Streaming Multi-Agent Workflow
- 📊 Interactive Streamlit Dashboard

---

## 🏛 Architecture

```
                           User Idea
                               │
                               ▼
                     Venture Manager Agent
                               │
        ┌───────────────┬───────────────┬───────────────┐
        ▼               ▼               ▼
 Market Research   Competitor Analysis   Customer Research
        │               │               │
        └───────────────┴───────────────┘
                        ▼
                 Business Model Agent
                        ▼
           Technical Architecture Agent
                        ▼
               Risk Analysis Agent
                        ▼
                Pitch Deck Generator
                        ▼
                 Final Startup Report
```

---

## 🛠 Tech Stack

### AI Framework

- LangGraph
- LangChain
- Google Gemini 2.5 Flash Lite
- Pydantic Structured Outputs

### Frontend

- Streamlit

### Language

- Python 3.13+

---

## 📋 Workflow

1. User enters a startup idea.
2. Venture Manager decomposes the problem into specialized tasks.
3. Three research agents execute in parallel:
   - Market Research
   - Competitor Analysis
   - Customer Research
4. Business Model Agent synthesizes the research.
5. Technical Architecture Agent evaluates implementation feasibility.
6. Risk Analysis Agent identifies technical and business risks.
7. Pitch Deck Agent generates an investor-ready startup pitch.

---

## 📸 Demo

*(Add screenshots or GIF here)*

Example:

```
assets/demo.gif
```

---

## ⚙ Installation

Clone the repository

```bash
git clone https://github.com/<your-username>/AI-Venture-Studio.git

cd AI-Venture-Studio
```

Create a virtual environment

```bash
python -m venv newenv
```

Activate

### macOS/Linux

```bash
source newenv/bin/activate
```

### Windows

```bash
newenv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file

```text
GOOGLE_API_KEY=YOUR_GOOGLE_API_KEY
TAVILY_API_KEY=YOUR_TAVILY_API_KEY
```

---

## ▶ Run

```bash
streamlit run app.py
```

---

## 📂 Project Structure

```
AI-Venture-Studio/

│── app.py
│── trendanalyser.py
│── requirements.txt
│── README.md
│── .env.example
│── assets/
```

---

## 📌 Example Startup Idea

> Build an AI-powered interview preparation platform that conducts realistic mock interviews, analyzes resumes against job descriptions, identifies skill gaps, recommends personalized learning resources, and helps universities improve placement rates through AI-driven career coaching.

---

## 🚀 Future Improvements

- Real-time Tavily Web Search
- Source Citations
- PDF Report Export
- Investor Review Agent
- Financial Projection Agent
- Startup Valuation Agent
- Multi-thread Memory
- Authentication
- Docker Deployment
- FastAPI Backend

---

## 🤝 Contributing

Contributions are welcome!

Feel free to open Issues or Pull Requests.

---

## 📜 License

This project is licensed under the MIT License.

---

## 👨‍💻 Author

**Sunay Goyal**

Engineering Student | AI & Backend Enthusiast
---