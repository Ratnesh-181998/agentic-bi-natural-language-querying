# 🤖 Agentic BI SaaS: Enterprise Natural Language Analytics

<div align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&height=240&text=Agentic%20BI%20SaaS&fontSize=60&fontColor=ffffff&animation=fadeIn" alt="Agentic BI Header" />
  
  <p align="center">
    <b>A Production-Grade Generative BI Platform Powered by LangGraph & Multi-Agent Orchestration</b>
  </p>

  [![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
  [![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
  [![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
  [![LangChain](https://img.shields.io/badge/LangChain-Integration-1C3C3C?logo=langchain&logoColor=white)](https://langchain.com/)
  [![LangGraph](https://img.shields.io/badge/LangGraph-Orchestration-FF9900)](https://langchain-ai.github.io/langgraph/)
  [![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
  [![Git LFS](https://img.shields.io/badge/Git%20LFS-Enabled-orange?logo=git-lfs&logoColor=white)](https://git-lfs.github.com/)
</div>

---

## 📑 **Table of Contents**
- [📍 Live Demo](#-live-demo)
- [📖 Overview](#-overview)
- [🖼️ System Architecture](#-system-architecture)
- [🛠️ Tech Stack](#-tech-stack--libraries)
- [🚀 Key Features](#-key-features)
- [🖥️ UI Walkthrough](#-ui-walkthrough-application-tabs)
- [⚙️ Installation](#-installation--setup)
- [☁️ Deployment](#-deployment-guide)
- [📄 License](#-license)
- [📞 Contact](#-contact--support)

---

## 📍 **Live Demo**

🌟 **Try the Live Application Here:** [**Agentic BI SaaS Platform**](https://agentic-bi-natural-language-querying-xav6gvp2wxnpnn7q9caarf.streamlit.app/)

> **Note:** The live demo is hosted on Streamlit Cloud. It provides a full read-only experience of the platform, allowing you to ask queries and visualize data instantly.

---

## 📖 **Overview**

**Agentic BI SaaS** is a next-generation Business Intelligence platform that replaces static dashboards with **conversational analytics**. Instead of manually filtering charts, users ask questions in plain English (e.g., *"Show me the revenue trend for the East region in Feb 2026"*), and a swarm of **AI Agents** collaborates to generate real-time SQL queries, execute them securely, and visualize the results.

Built for **Enterprise Scalability**, this project features a **Service-Oriented Architecture (SOA)** with a decoupled React-like UI (Streamlit) and a robust API Backend (FastAPI + LangGraph).

---

## �️ **System Architecture**

This project leverages a **Multi-Agent Swarm Architecture** orchestrated by **LangGraph**. Each agent specializes in a distinct cognitive task, ensuring high accuracy and resilience.

<div align="center">
  <img src="agentic_bi_architecture.jpeg" alt="Agentic BI Architecture Diagram" width="100%" style="border-radius: 10px; border: 2px solid #ddd; box-shadow: 5px 5px 15px rgba(0,0,0,0.2);">
</div>

### **Core Agent Swarm (The "Brain")**
1.  **� Metadata Agent:** Analysis user intent & schema mapping (Context-Aware).
2.  **🕸️ RAG Agent:** Retrieves certified business definitions from Vector DB.
3.  **📝 SQL Agent:** Generates dialect-specific SQL (SQLite/PostgreSQL) with 99% syntax accuracy.
4.  **🛡️ Impact Agent:** Governance layer; predicts query cost & blocks destructive operations (DROP/DELETE).
5.  **⚙️ Execute Agent:** Runs verified SQL in a sandboxed environment.
6.  **📊 BI Agent:** synthesizes results into JSON configs for Front-end rendering.

---

## 🛠️ **Tech Stack & Libraries**

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Frontend** | **Streamlit** | Interactive UI with Tabs, Real-time Logs, and Plotly Charts. |
| **Backend** | **FastAPI** | High-performance Async REST API for Agent communication. |
| **Orchestration** | **LangGraph** | Stateful workflow management / Cyclic Graph for Agents. |
| **LLM Framework** | **LangChain** | Prompt engineering & Tool abstractions. |
| **AI Models** | **Groq (Llama 3)** | Ultra-fast inference for real-time SQL generation. |
| **Memory** | **Mem0 (mem0ai)** | Long-term user preference & session storage. |
| **Database** | **SQLite / SQLAlchemy** | Relational data storage with ORM. |
| **Task Scheduling** | **APScheduler** | Background jobs and reporting. |
| **Visualization** | **Plotly Express** | Dynamic, interactive data visualizations. |

---

## 🚀 **Key Features**

### 1. **Natural Language to SQL**
Type complex business questions like *"Compare marketing ROI vs Sales for Top 5 products"* and get instant charts. No SQL knowledge required.

### 2. **Self-Healing AI Pipeline**
The system uses `LangGraph` to implement **Reflexion**. If an agent generates invalid SQL, the **Execute Agent** feeds the error back to the **SQL Agent** for auto-correction.

### 3. **Enterprise Governance (RBAC)**
Built-in **Impact Agent** ensures security. It calculates "Query Cost" and blocks unauthorized access to sensitive PII columns or tables.

### 4. **Long-Term Memory**
Powered by `mem0`, the system "remembers" your preferred region, currency, and chart types across sessions.

### 5. **Real-Time System Logs**
A dedicated **"System Logs"** tab provides transparency. Watch the "Thought Process" of every agent in real-time (e.g., *Metadata Agent identified 'Sales' table*, *Impact Agent approved query*).

---

## 🖥️ **UI Walkthrough (Application Tabs)**

### **Tab 1: 🤖 Agentic BI Demo**
The main workspace.
- **Chat Interface:** Ask questions.
- **Dynamic Dashboard:** Charts (Bar, Line, Pie) render automatically based on data type.
- **Reasoning Engine:** View the "Why" behind the answer (Show SQL & Thinking).

### **Tab 2: 🛠️ Tech Stack & Specs**
Detailed documentation of the libraries used.
- Interactive **badges** for every tool.
- Explanation of **RAG (Retrieval Augmented Generation)** implementation.

### **Tab 3: 📊 Architecture & Design**
- High-Level Design (HLD) & Low-Level Design (LLD).
- Interactive **Graphviz** flowcharts showing data movement between Frontend -> API -> Database.

### **Tab 4: 📋 System Logs**
- **Live Event Feed:** See backend logs in the frontend.
- **Filters:** Filter by `Error`, `Success`, or specific `Agent`.
- **Export:** Download logs as `CSV` or `TXT` for auditing.

---

## ⚙️ **Installation & Setup**

### **Prerequisites**
- Python 3.10+
- Git

### **1. Clone the Repository**
```bash
git clone https://github.com/Ratnesh-181998/agentic-bi-natural-language-querying.git
cd agentic-bi-natural-language-querying/agentic-bi-saas
```

### **2. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **3. Configure Environment**
Create a `.env` file in the root directory:
```env
GROQ_API_KEY="your_groq_api_key"
OPENAI_API_KEY="optional_if_using_openai"
SIMULATION_MODE=False
```

### **4. Seed the Database**
Populate the SQLite database with synthetic enterprise data (Sales, CRM, Inventory):
```bash
python seed_db.py
```

### **5. Run the Application**
The app requires both the Backend (FastAPI) and Frontend (Streamlit) to run.

**Terminal 1 (Backend):**
```bash
uvicorn app.main:app --port 8000 --reload
```

**Terminal 2 (Frontend):**
```bash
streamlit run ui/presentation_app.py
```
> Access the app at `http://localhost:8501`

---

## ☁️ **Deployment Guide**

### **Option 1: Streamlit Cloud (Recommended)**
1. Fork this repo to your GitHub.
2. Login to [share.streamlit.io](https://share.streamlit.io).
3. "New App" -> Select Repository.
4. **Main File Path:** `agentic-bi-saas/ui/presentation_app.py`.
5. **Advanced Settings (Secrets):** Paste your `.env` contents here.
6. **Deploy!** 🚀

### **Option 2: Docker (Production)**
The project is container-ready.

**Dockerfile:**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
EXPOSE 8501 8000
CMD sh -c "uvicorn app.main:app --host 0.0.0.0 --port 8000 & streamlit run ui/presentation_app.py --server.port 8501"
```

**Build & Run:**
```bash
docker build -t agentic-bi .
docker run -p 8501:8501 -p 8000:8000 --env-file .env agentic-bi
```

---

## � **CI/CD Pipeline (GitHub Actions)**

Automate testing and deployment to AWS/GCP.

**`.github/workflows/deploy.yml`**
```yaml
name: Deploy to Cloud
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          lfs: true # Important for Large Files
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install Dependencies
        run: |
          pip install -r agentic-bi-saas/requirements.txt
      - name: Run Tests
        run: |
          cd agentic-bi-saas
          python -m pytest tests_scripts/
```

---

## 📄 **License**

Distributed under the **Apache 2.0 License**. See `LICENSE` for more information.

---

## 📞 **Contact & Support**

**Ratnesh Kumar Singh**  
*Data Scientist (AI/ML) | GenAI Specialist*

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?logo=linkedin)](https://www.linkedin.com/in/ratneshkumar1998/)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-black?logo=github)](https://github.com/Ratnesh-181998)
[![Email](https://img.shields.io/badge/Email-Contact-red?logo=gmail)](mailto:rattudacsit2021gate@gmail.com)
