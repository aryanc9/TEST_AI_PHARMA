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

### � Document Processing (NEW!)
- **Prescription Upload**: Extract medicine data from prescription images
- **Medical Report Upload**: Extract findings and test results from medical reports
- **Dual OCR Engines**:
  - **PaddleOCR**: Fast local OCR (2-3 seconds), offline-capable
  - **Google Document AI**: High-accuracy cloud OCR (95%+), structured data extraction
- **Automatic Fallback**: If primary OCR fails, automatically switches to alternative
- **Confidence Scoring**: Quality metrics for each extraction (0.0-1.0 scale)
- **Async Processing**: Background task handling for large files

### �🛡 Safety & Policy Enforcement
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

```
┌─────────────┐
│   Frontend  │ (React 5173)
│  Dashboard  │
└──────┬──────┘
       │
       ├──────► /chat API (Conversational)
       │
       ├──────► /documents/prescription/upload (OCR)
       │
       └──────► /documents/medical-report/upload (OCR)
               │
               ▼
         ┌──────────────────┐
         │   Backend API    │ (FastAPI 8000)
         └────────┬─────────┘
                  │
        ┌─────────┼─────────┐
        │         │         │
        ▼         ▼         ▼
    ┌────────┬──────────┬────────────┐
    │Memory  │Agents &  │Document    │
    │Agent   │LLM Logic │Processor   │
    └────┬───┴────┬─────┴─────┬──────┘
         │        │           │
         └────────┼───────────┘
                  │
              ┌───▼────┐
              │Database│ (SQLite)
              └────────┘
                  │
        ┌─────────┼──────────┐
        │         │          │
        ▼         ▼          ▼
    Orders   Documents  Prescriptions
```

### OCR Pipeline
```
Image Upload
    │
    ├─► PaddleOCR (Fast, Local)
    │   └─► Success? Return Results
    │   └─► Failed? Try Fallback
    │
    └─► Google Document AI (Accurate, Cloud)
        └─► Success? Return Results
        └─► Failed? Return Error
```


---

## 🛠 Tech Stack

- **Backend**: FastAPI
- **Agents**: LangGraph
- **LLM**: LLaMA 3.1 (via Ollama, optional)
- **Database**: SQLite
- **ORM**: SQLAlchemy
- **OCR/Document Processing**: 
  - PaddleOCR 3.3.3 (local, fast)
  - Google Document AI 3.8.0 (cloud, accurate)
  - Pillow 11.3.0 (image processing)
  - OpenCV 4.13.0.90 (computer vision)
- **Frontend**: React 18 + Vite + Tailwind CSS
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

### 1. Backend Setup
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Initialize Database
```bash
python3 -m backend.app.db.seed_data
```

### 3. Start Backend Server
```bash
cd backend
DISABLE_MODEL_SOURCE_CHECK=True python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```
Backend runs at: http://localhost:8000

### 4. Start Frontend Server (New Terminal)
```bash
cd frontend
npm install  # First time only
npm run dev
```
Frontend runs at: http://localhost:5173

### 5. Access Dashboard
Open your browser and navigate to: **http://localhost:5173**

### 6. Verify Installation
- **Swagger UI**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **Document Processing**: Navigate to "Document Processing" in sidebar

## 💬 API Examples

### Chat Endpoint
```bash
curl -X POST http://127.0.0.1:8000/chat/ \
  -H "Content-Type: application/json" \
  -d '{"customer_id":1,"message":"I need paracetamol 500mg"}'
```

Response:
```json
{
  "approved": true,
  "reply": "Order placed successfully",
  "order_id": 3
}
```

### Upload Prescription (Document Processing)
```bash
curl -X POST http://localhost:8000/documents/prescription/upload \
  -F "customer_id=1" \
  -F "file=@path/to/prescription.jpg" \
  -F "provider=paddle"
```

### Get Prescription Results
```bash
curl http://localhost:8000/documents/prescription/{document_id}
```

Response:
```json
{
  "status": "success",
  "document_id": "uuid",
  "medicines": [
    {
      "name": "Paracetamol",
      "dosage": "500mg",
      "frequency": "3 times daily",
      "quantity": "30 tablets"
    }
  ],
  "confidence_score": 0.95,
  "extracted_at": "2026-01-21T11:45:00Z"
}
```

## 🐳 Docker Installation (Optional)
```bash
docker build -t agentic-pharmacy .
docker run -p 8000:8000 -p 5173:5173 agentic-pharmacy
```
