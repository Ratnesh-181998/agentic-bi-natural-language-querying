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

## 🌐🎬 Live Demo
🚀 **Try it now:**


- **Streamlit Profile** -[[Link]](https://share.streamlit.io/user/ratnesh-181998)
  
- 🌟 **Project Demo Try the Live Application Here:** [**Agentic BI SaaS Platform**](https://agentic-bi-natural-language-querying-xav6gvp2wxnpnn7q9caarf.streamlit.app/)

- **Note:** The live demo is hosted on Streamlit Cloud. It provides a full read-only experience of the platform, allowing you to ask queries and visualize data instantly.
  
- **UI Walkthrough**
  
![Project Demo Walkthrough](https://github.com/Ratnesh-181998/agentic-bi-natural-language-querying/blob/main/UI_Walkthrough.gif)


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
| **Database** | **SQLite / SQLAlchemy and FAISS , VectorDB** | Relational data storage with ORM. |
| **Task Scheduling** | **APScheduler** | Background jobs and reporting. |
| **Visualization** | **Plotly Express** | Dynamic, interactive data visualizations. |

---

# 🚀 **Agentic BI SaaS: The Conversational Analytics**

How businesses interact with data.Instead of navigating complex dashboards, users simply ask questions in natural language and AI swarm does the rest.

## **🎯 The Problem**
Traditional BI tools require SQL expertise,static dashboard configurations, and constant IT dependency.Business users waste hours waiting for reports that could be answered instantly.

## **💡The Solution: Multi-Agent AI Architecture**

I built an **Enterprise-Grade Agentic BI Platform** using cutting-edge AI orchestration. Here's how it works:

**🧠 6-Agent Cognitive Swarm (LangGraph Orchestrated):**

1. **Metadata Agent** → Analyzes user intent & schema mapping
2. **RAG Agent** → Retrieves certified business definitions from Vector DB
3. **SQL Agent** → Generates production-ready SQL queries (99% accuracy)
4. **Impact Agent** → Governance layer; blocks unsafe queries & PII exposure
5. **Execute Agent** → Sandboxed SQL execution
6. **BI Agent** → Synthesizes results into intelligent visualizations
   
## **🛠️ Tech Stack (Production-Grade)**

**AI/ML & NLP Layer:**
- **LangGraph** (Multi-Agent Orchestration)
- **LangChain** (Prompt Engineering Framework)
- **Groq** (Llama 3.3 - 70B) for ultra-fast inference
- **HuggingFace** (Text embeddings & transformer models)
- **FuzzyWuzzy** (NLP fuzzy string matching for typo-tolerant queries)
- **Mem0** (Long-term AI memory for user preferences)
  
**Vector & Retrieval:**
- **FAISS** (Facebook AI Similarity Search - Vector DB)
- **RAG Pipeline** (Retrieval Augmented Generation)
- **MCP** (Model Context Protocol for agent-tool communication)
  
**Backend:**
- **FastAPI** (Async REST API)
- **SQLAlchemy** + SQLite/PostgreSQL
- **APScheduler** (Background task management)
  
**Frontend:**
- **Streamlit/Next.js** (Interactive UI with Real-time Agent Logs)
- **Plotly** (Dynamic, responsive visualizations)
  
**DevOps:**
- **Docker-ready** containers
- **CI/CD** pipeline (GitHub Actions)
  
## **🔐Enterprise-Ready Features**
- **Self-Healing Pipeline**:Auto-corrects SQL errors using reflexion loops
- **Typo-Resilient**:FuzzyWuzzy NLP handles misspelled queries intelligently
- **Semantic Search**:FAISS-powered vector similarity for context retrieval
- **Governance**:Built-in RBAC & PII detection
- **Memory**:Learns user preferences across sessions
- **Scalability**:SaaS & On-Prem deployment ready
  
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

<img width="1901" height="800" alt="image" src="https://github.com/user-attachments/assets/8041727b-91a5-4d5b-9dd3-fcd43e96cc96" />
<img width="1611" height="747" alt="image" src="https://github.com/user-attachments/assets/8329a070-4c80-4cbc-bea5-11ac0456dce8" />
<img width="1614" height="761" alt="image" src="https://github.com/user-attachments/assets/d574821f-7f0f-472b-8027-df0ce08f0ea8" />
<img width="1611" height="738" alt="image" src="https://github.com/user-attachments/assets/53db7bee-085d-43a2-af8a-07e2e77fce9d" />
<img width="1654" height="719" alt="image" src="https://github.com/user-attachments/assets/e64393d7-89fb-4f54-841b-ab1736387a5b" />
<img width="1601" height="672" alt="image" src="https://github.com/user-attachments/assets/1e8f1b5a-c27e-4120-b25e-229f46c2dc3e" />
<img width="1652" height="788" alt="image" src="https://github.com/user-attachments/assets/2a41bab2-7724-4286-bfda-6be0dbb97447" />
<img width="1657" height="695" alt="image" src="https://github.com/user-attachments/assets/57be8f4b-f19c-4e4d-a1c7-a7b4be6995bc" />
<img width="1598" height="798" alt="image" src="https://github.com/user-attachments/assets/f375b831-e7f8-47b2-a597-5e11e7f136af" />
<img width="1629" height="748" alt="image" src="https://github.com/user-attachments/assets/74e19f7c-9ce5-4dab-9cbb-4d77c0d5abad" />
<img width="1654" height="780" alt="image" src="https://github.com/user-attachments/assets/3327361b-57aa-400d-a55f-20af7bc23889" />

### **Tab 2:ℹ️ About Project**
-  Project Vision & Mission : Agentic BI SaaS is an enterprise-grade Business Intelligence platform powered by Agentic AI. Users can ask business questions in plain English, and the system intelligently converts them into trusted, governed, explainable insights.
- To democratize data access within enterprises, reducing the dependency on data analyst teams for routine reporting.
- 🚀 AI Analyst , 🧠 Long-Term Memory ,🔐 Enterprise Gov
- In simple words: This system replaces manual BI dashboards with an AI analyst that remembers, learns, and scales securely.

<img width="1892" height="770" alt="image" src="https://github.com/user-attachments/assets/d16afa94-7b4e-4ca0-8ec6-771691639f3b" />
<img width="1602" height="760" alt="image" src="https://github.com/user-attachments/assets/2f8a7c52-2c1c-4941-a237-487eb299b6fd" />
<img width="1629" height="672" alt="image" src="https://github.com/user-attachments/assets/7d2b87bd-fa14-4120-b36e-6681c056b8fb" />
<img width="1599" height="647" alt="image" src="https://github.com/user-attachments/assets/3e7ebb91-8f28-4549-a929-cd38e4aac089" />
<img width="1548" height="704" alt="image" src="https://github.com/user-attachments/assets/68d0d9db-8a6a-47be-8fdf-13951be5b5fc" />
<img width="1611" height="725" alt="image" src="https://github.com/user-attachments/assets/df0963b9-0f28-4bba-93bb-da59e2be5c1a" />

### **Tab 3: 🛠️ Tech Stack & Specs**
Detailed documentation of the libraries used.
- Interactive **badges** for every tool.
- Explanation of **RAG (Retrieval Augmented Generation)** implementation.
  
<img width="1866" height="805" alt="image" src="https://github.com/user-attachments/assets/5cfe8300-48ed-4311-ac04-284e58ef6be6" />
<img width="1589" height="714" alt="image" src="https://github.com/user-attachments/assets/22049204-4975-42e7-9ce5-4c4b0447157a" />
<img width="1588" height="781" alt="image" src="https://github.com/user-attachments/assets/65287de0-4639-4957-9b1d-986d9e1c1ac4" />
<img width="1611" height="729" alt="image" src="https://github.com/user-attachments/assets/e8be6c83-5abb-4c80-a1d1-ddd4aa96b25c" />

### **Tab 4: 📐 HLD & LLD**
- 📐 Design & Architecture Specification : Comprehensive documentation covering Software Requirements (SRS), High-Level Design (HLD), and Low-Level Design (LLD).
- 📝 1. Software Requirements Specification (SRS)
-m🏗️ 2. High Level Design (HLD)
- ⚙️ 3. Low Level Design (LLD)
  
<img width="1860" height="804" alt="image" src="https://github.com/user-attachments/assets/65ab79ad-c654-4ae0-82cc-27e7d76beca3" />
<img width="1609" height="791" alt="image" src="https://github.com/user-attachments/assets/d984d711-632a-4e30-8bed-f5bcaf8a2036" />
<img width="1586" height="769" alt="image" src="https://github.com/user-attachments/assets/466a38a0-8a88-45df-8c1d-20e2b46f6fb4" />
<img width="1608" height="632" alt="image" src="https://github.com/user-attachments/assets/b0e66f94-9c74-4da8-b538-8828a06c75d1" />
<img width="1619" height="734" alt="image" src="https://github.com/user-attachments/assets/b73249d7-abb6-47ff-804c-e5068f1b6a33" />

### **Tab 5: 📊 Architecture & Design**
- High-Level Design (HLD) & Low-Level Design (LLD).
- Interactive **Graphviz** flowcharts showing data movement between Frontend -> API -> Database.
  
<img width="1847" height="772" alt="image" src="https://github.com/user-attachments/assets/9b5e43de-d334-4a33-9249-2b17a85c811a" />
<img width="1339" height="714" alt="image" src="https://github.com/user-attachments/assets/af1636fe-404e-428b-b6a6-991273ea3287" />
<img width="1365" height="589" alt="image" src="https://github.com/user-attachments/assets/7dd249d8-58e5-4722-b388-1b03be0d20a6" />
<img width="1586" height="729" alt="image" src="https://github.com/user-attachments/assets/5c1e42b2-2c84-49bf-8d22-d854d8795a05" />
<img width="1611" height="757" alt="image" src="https://github.com/user-attachments/assets/17728d73-df8c-40f7-9e2e-88d71e5b21f5" />
<img width="1608" height="732" alt="image" src="https://github.com/user-attachments/assets/4b6456ae-98f1-485c-a7ed-2118d4d9b06c" />


### **Tab 6: 📋 System Logs**
- **Live Event Feed:** See backend logs in the frontend.
- **Filters:** Filter by `Error`, `Success`, or specific `Agent`.
- **Export:** Download logs as `CSV` or `TXT` for auditing.

<img width="1842" height="807" alt="image" src="https://github.com/user-attachments/assets/63c48c96-9675-4569-82f7-22006d3e5249" />
<img width="1603" height="784" alt="image" src="https://github.com/user-attachments/assets/f80a51ba-79c8-4de2-b49c-b87f8b2068de" />
<img width="1647" height="736" alt="image" src="https://github.com/user-attachments/assets/95b44552-b4f8-4dbb-a518-9a5d16c1c9c0" />

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

<img src="https://capsule-render.vercel.app/api?type=rect&color=gradient&customColorList=24,20,12,6&height=3" width="100%">


# 📞 **CONTACT & NETWORKING** 📞


### 💼 Professional Networks

[![LinkedIn](https://img.shields.io/badge/💼_LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/ratneshkumar1998/)
[![GitHub](https://img.shields.io/badge/🐙_GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Ratnesh-181998)
[![X](https://img.shields.io/badge/X-000000?style=for-the-badge&logo=x&logoColor=white)](https://x.com/RatneshS16497)
[![Portfolio](https://img.shields.io/badge/🌐_Portfolio-FF6B6B?style=for-the-badge&logo=google-chrome&logoColor=white)](https://share.streamlit.io/user/ratnesh-181998)
[![Email](https://img.shields.io/badge/✉️_Email-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:rattudacsit2021gate@gmail.com)
[![Medium](https://img.shields.io/badge/Medium-000000?style=for-the-badge&logo=medium&logoColor=white)](https://medium.com/@rattudacsit2021gate)
[![Stack Overflow](https://img.shields.io/badge/Stack_Overflow-F58025?style=for-the-badge&logo=stack-overflow&logoColor=white)](https://stackoverflow.com/users/32068937/ratnesh-kumar)

### 🚀 AI/ML & Data Science
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://share.streamlit.io/user/ratnesh-181998)
[![HuggingFace](https://img.shields.io/badge/HuggingFace-FFD21E?style=for-the-badge&logo=huggingface&logoColor=black)](https://huggingface.co/RattuDa98)
[![Kaggle](https://img.shields.io/badge/Kaggle-20BEFF?style=for-the-badge&logo=kaggle&logoColor=white)](https://www.kaggle.com/rattuda)

### 💻 Competitive Programming (Including all coding plateform's 5000+ Problems/Questions solved )
[![LeetCode](https://img.shields.io/badge/LeetCode-FFA116?style=for-the-badge&logo=leetcode&logoColor=black)](https://leetcode.com/u/Ratnesh_1998/)
[![HackerRank](https://img.shields.io/badge/HackerRank-00EA64?style=for-the-badge&logo=hackerrank&logoColor=black)](https://www.hackerrank.com/profile/rattudacsit20211)
[![CodeChef](https://img.shields.io/badge/CodeChef-5B4638?style=for-the-badge&logo=codechef&logoColor=white)](https://www.codechef.com/users/ratnesh_181998)
[![Codeforces](https://img.shields.io/badge/Codeforces-1F8ACB?style=for-the-badge&logo=codeforces&logoColor=white)](https://codeforces.com/profile/Ratnesh_181998)
[![GeeksforGeeks](https://img.shields.io/badge/GeeksforGeeks-2F8D46?style=for-the-badge&logo=geeksforgeeks&logoColor=white)](https://www.geeksforgeeks.org/profile/ratnesh1998)
[![HackerEarth](https://img.shields.io/badge/HackerEarth-323754?style=for-the-badge&logo=hackerearth&logoColor=white)](https://www.hackerearth.com/@ratnesh138/)
[![InterviewBit](https://img.shields.io/badge/InterviewBit-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://www.interviewbit.com/profile/rattudacsit2021gate_d9a25bc44230/)

---

## 📊 **GitHub Stats & Metrics** 📊



![Profile Views](https://komarev.com/ghpvc/?username=Ratnesh-181998&color=blueviolet&style=for-the-badge&label=PROFILE+VIEWS)





<img src="https://github-readme-streak-stats.herokuapp.com/?user=Ratnesh-181998&theme=radical&hide_border=true&background=0D1117&stroke=4ECDC4&ring=F38181&fire=FF6B6B&currStreakLabel=4ECDC4" width="48%" />




<img src="https://github-readme-activity-graph.vercel.app/graph?username=Ratnesh-181998&theme=react-dark&hide_border=true&bg_color=0D1117&color=4ECDC4&line=F38181&point=FF6B6B" width="48%" />

---

<img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&size=24&duration=3000&pause=1000&color=4ECDC4&center=true&vCenter=true&width=600&lines=Ratnesh+Kumar+Singh;Data+Scientist+%7C+AI%2FML+Engineer;4%2B+Years+Building+Production+AI+Systems" alt="Typing SVG" />

<img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&size=18&duration=2000&pause=1000&color=F38181&center=true&vCenter=true&width=600&lines=Built+with+passion+for+the+AI+Community+🚀;Innovating+the+Future+of+AI+%26+ML;MLOps+%7C+LLMOps+%7C+AIOps+%7C+GenAI+%7C+AgenticAI+Excellence" alt="Footer Typing SVG" />


<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=6,11,20&height=120&section=footer" width="100%">

    
  
