# 🚀 AI Venture Studio

> An intelligent multi-agent startup consultant built using **LangGraph**, **Gemini**, **Tavily**, **Streamlit**, and **Pydantic Structured Outputs**.

AI Venture Studio transforms a startup idea into a comprehensive investor-ready business report by orchestrating multiple AI agents that collaborate, use external tools, validate decisions, and generate structured insights.

---

## 📸 Demo

> **Live Demo:** https://ai-venture-studio-cppaxvpdm5mtvqcsyddejg.streamlit.app/

> **GitHub:** https://github.com/sunay1524/AI-Venture-Studio

---

# ✨ Features

✅ Multi-Agent Architecture using LangGraph

✅ Parallel Agent Execution

✅ Conditional Routing

✅ Tool-Using AI Agents

✅ Structured Outputs (Pydantic)

✅ Market Research using Tavily

✅ Competitor Analysis using Tavily

✅ Customer Research using Reddit Discussions

✅ Automatic Business Model Generation

✅ Technical Architecture Recommendation

✅ Risk Analysis

✅ Investor Pitch Deck Generation

✅ Interactive Streamlit Dashboard

✅ Markdown Report Export (Download completed reports instantly)

---

# 🧠 Architecture

```

                     User Idea
                         │
                         ▼
                Venture Manager Agent
                         │
        ┌────────────────┼────────────────┐
        ▼                ▼                ▼
 Market Research   Competitor Analysis  Customer Research
      (Tavily)         (Tavily)      (Reddit + Tavily)
        │                │                │
        └────────────────┼────────────────┘
                         ▼
                Business Model Agent
                         │
                         ▼
            Technical Architecture Agent
                         │
          Feasible? ─────┴─────── No
                │                 ▲
               Yes                │
                ▼                 │
             Risk Analysis Agent──┘
                │
      Acceptable Risk?
          │            │
         Yes          No
          │            ▲
          ▼            │
     Pitch Deck Agent──┘
          │
          ▼
    Investor Ready Report

```

---

# 🤖 Agents

## 🚀 Venture Manager

Breaks down the startup idea into specialized tasks and delegates work to downstream agents.

---

## 📈 Market Research Agent

Uses **Tavily Search** to retrieve:

- Market Size
- CAGR
- Industry Trends
- Growth Opportunities
- Challenges

---

## 🏢 Competitor Analysis Agent

Performs live competitor research using Tavily.

Analyzes:

- Direct Competitors
- Indirect Competitors
- Pricing
- Business Models
- Competitive Advantages

---

## 👥 Customer Research Agent

Uses Reddit discussions (via Tavily Search) to discover:

- Customer Personas
- Pain Points
- Feature Requests
- Buying Motivation
- Objections

---

## 💼 Business Model Agent

Creates:

- Revenue Model
- Pricing Strategy
- Value Proposition
- Go-To-Market Strategy

---

## 🏗 Technical Architecture Agent

Designs the technical solution including:

- Tech Stack
- System Components
- APIs
- Scalability
- Deployment Strategy

---

## ⚠ Risk Analysis Agent

Evaluates:

- Business Risk
- Technical Risk
- Financial Risk
- Market Risk

If risk exceeds acceptable limits, the workflow automatically loops back to improve the business model.

---

## 🎤 Pitch Deck Agent

Produces an investor-ready startup summary including:

- Executive Summary
- Problem Statement
- Solution
- Market Opportunity
- Business Model
- Competitive Advantage
- Investment Highlights

---

# 🔁 Workflow

```

User Idea

↓

Venture Manager

↓

Parallel Research

↓

Business Model

↓

Technical Review

↓

Risk Analysis

↓

Conditional Retry (if required)

↓

Pitch Deck

↓

Final Report

```

---

# 🛠 Tech Stack

| Category | Technologies |
|-----------|--------------|
| Language | Python |
| Agent Framework | LangGraph |
| LLM | Gemini 3.1 Flash |
| AI Framework | LangChain |
| Search Tool | Tavily |
| Customer Research | Reddit Search |
| Frontend | Streamlit |
| Data Validation | Pydantic |
| Workflow | Stateful Graph |
| Environment | Python + dotenv |

---

# 📂 Project Structure

```

AI-Venture-Studio

├── app.py
├── venture_studio.py
├── requirements.txt
├── README.md
├── .env
└── assets/

```

---

# 🚀 Getting Started

Clone the repository

```bash
git clone https://github.com/sunay1524/AI-Venture-Studio.git
cd AI-Venture-Studio
```

Install dependencies

```bash
pip install -r requirements.txt
```

Create a `.env`

```text
GOOGLE_API_KEY=YOUR_KEY
TAVILY_API_KEY=YOUR_KEY
```

Run

```bash
streamlit run app.py
```

---

# 📊 Example Startup Ideas

- AI Interview Coach
- AI Legal Assistant
- Smart Farming Platform
- AI Healthcare Assistant
- AI Finance Advisor
- Creator Marketplace

---

# 🎯 Future Improvements

- Investor Score
- Financial Projection Agent
- Live Citations
- PowerPoint Generation
- Multi-language Support
- Memory Support
- Crew Collaboration Dashboard

---

# 📚 What I Learned

Building AI Venture Studio helped me gain hands-on experience with:

- Multi-Agent AI Systems
- Agent Orchestration
- LangGraph
- Structured Outputs
- Conditional Graph Routing
- Parallel Agent Execution
- Tool-Using AI Agents
- Prompt Engineering
- Streamlit Deployment
- Production AI Workflow Design

---

# ⭐ If you found this project interesting

Please consider starring the repository!
