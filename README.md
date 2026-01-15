# 🧠 Agentic AI Pharmacy System

An autonomous, agent-based pharmacy backend that transforms traditional
search-and-click ordering into a proactive, safety-first AI system.

This system behaves like an expert pharmacist:
- Understands natural language (text)
- Enforces prescription and stock rules
- Predicts refill needs
- Executes real backend actions autonomously
- Provides full, judge-visible decision traces

---

## 🚀 Key Features

### 🗣 Conversational Ordering
- Natural language input
- Robust extraction of medicine, dosage, and quantity
- Handles messy human language

### 🛡 Safety & Policy Enforcement
- Inventory is the single source of truth
- Prescription enforcement
- Stock validation
- Quantity limits

### 🔁 Autonomous Refill Intelligence
- Background scheduler scans patient history
- Predicts when medicines are running low
- Generates proactive refill alerts

### 🤖 Agentic Architecture
Multiple specialized agents collaborate:
- Memory Agent
- Conversation Agent (LLM-powered)
- Safety Agent (deterministic)
- Action Agent
- Predictive Refill Agent

### 🔍 Full Observability
- Judge-visible decision traces
- Clear explanation of why actions were approved or blocked
- No black-box behavior

---

## 🧩 System Architecture

User → /chat API
→ Memory Agent
→ Conversation Agent (LLM)
→ Safety Agent
→ Action Agent
→ Refill Intelligence
→ Database + Alerts


---

## 🛠 Tech Stack

- **Backend**: FastAPI
- **Agents**: LangGraph
- **LLM**: LLaMA 3.1 (via Ollama, optional)
- **Database**: SQLite
- **ORM**: SQLAlchemy
- **Containerization**: Docker
- **Observability**: Decision Trace Logs

---

## 📦 Installation Guide

### 1. How to install
```bash

This project is designed to run fully offline with free tools.

Prerequisites

Ensure you have the following installed:

Python 3.9+

pip

Git

(Optional) Ollama for local LLM inference

Verify versions:
python3 --version
pip --version
git --version

Step 1: Clone the Repository
git clone https://github.com/<your-username>/agentic-ai-pharmacy.git
cd agentic-ai-pharmacy

Step 2: Create and Activate Virtual Environment
python3 -m venv venv
source venv/bin/activate

On Windows:
venv\Scripts\activate

Step 3: Install Python Dependencies
pip install --upgrade pip
pip install -r requirements.txt

Step 4: (Optional) Install Local LLM with Ollama

If you want local, offline LLM reasoning:
brew install ollama
ollama pull llama3.1:8b
ollama serve

Step 5: Initialize Database
python3 -m backend.app.db.seed_data

This creates:

Medicines

Customers

Sample inventory

Safety rules baseline
Step 6: Start the Server
uvicorn backend.app.main:app --reload

Server runs at:http://127.0.0.1:8000

Step 7: Verify Installation

Open Swagger UI:
http://127.0.0.1:8000/docs

Test chat endpoint:
curl -X POST http://127.0.0.1:8000/chat/ \
  -H "Content-Type: application/json" \
  -d '{"customer_id":1,"message":"I need paracetamol 500mg"}'

🐳 Docker Installation (Optional)
docker build -t agentic-pharmacy .
docker run -p 8000:8000 agentic-pharmacy



## ⚙️ How to Run (Local)

### 2. Create virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

2. Initialize database
python3 -m backend.app.db.seed_data

3. Start server
uvicorn backend.app.main:app --reload

4. Open Swagger
http://127.0.0.1:8000/docs

💬 Chat API Example
curl -X POST http://127.0.0.1:8000/chat/ \
  -H "Content-Type: application/json" \
  -d '{"customer_id":1,"message":"I need paracetamol 500mg"}'


  
Response:
{
  "approved": true,
  "reply": "Order placed successfully",
  "order_id": 3
}

## 3 ⚙️ How to Run (Production)

uvicorn backend.app.main:app --host 0.0.0.0 --port 8000
