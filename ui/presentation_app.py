import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import random
import os
try:
    from ui.render_utils import render_data_results
except ImportError:
    # Fallback if running from root
    from render_utils import render_data_results

try:
    from seed_db import seed as seed_data
except ImportError:
    seed_data = None

# Page Config
st.set_page_config(
    page_title="Agentic BI | Enterprise Suite",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    /* Global Styles */
    :root {
        --primary-gold: #FFD700;
        --secondary-gold: #FFC800;
        --accent-blue: #2874f0;
        --accent-green: #2ecc71;
        --accent-purple: #9b59b6;
        --background-dark: #0e1117;
    }
    
    .stApp {
        background-color: var(--background-dark);
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
        border-right: 3px solid var(--accent-blue);
    }
    
    h1, h2, h3 {
        color: #ffff !important;
        font-family: 'Inter', sans-serif;
    }
    
    /* Tabs & Cards (Improved Full-Width Tabs) */
    .stTabs [data-baseweb="tab-list"] { 
        gap: 8px; 
        width: 100% !important;
        display: flex !important;
    }
    .stTabs [data-baseweb="tab"] { 
        height: 55px; 
        background-color: #1e1e2d; 
        border-radius: 8px; 
        color: #ffffff; 
        font-weight: 700; 
        flex-grow: 1 !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        transition: all 0.3s ease;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #2e2e3f;
        transform: translateY(-2px);
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] { 
        background-color: #7267EF; 
        color: white; 
        border: 1px solid #00D2FF;
        box-shadow: 0 4px 15px rgba(114, 103, 239, 0.4);
    }
    .metric-card { background-color: #262730; padding: 20px; border-radius: 10px; border: 1px solid #41424C; text-align: center; }
    </style>
""", unsafe_allow_html=True)

# Helper: Get IST Time
def get_ist_time():
    utc_now = datetime.utcnow()
    ist_now = utc_now + timedelta(hours=5, minutes=30)
    return ist_now.strftime("%Y-%m-%d %H:%M:%S IST")

# Session State for Logs
if "system_logs" not in st.session_state:
    st.session_state.system_logs = []

# Global Configuration
SIMULATION_MODE = os.getenv("SIMULATION_MODE", "False").lower() == "true"

def log_event(event_type, details):
    timestamp = get_ist_time()
    st.session_state.system_logs.insert(0, {
        "Timestamp": timestamp,
        "Event": event_type,
        "Details": details,
        "User": "Admin_User" 
    })

# --- SUPERIOR SIDEBAR ---
with st.sidebar:
    # 1. Project Title Card
    st.markdown("""
    <div style='background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 41, 59, 0.9) 100%); padding: 20px; border-radius: 10px; text-align: center; border: 2px solid #7267EF; box-shadow: 0 4px 15px rgba(114, 103, 239, 0.3);'>
        <h2 style='margin: 0; font-size: 1.6rem; font-weight: 800;'>
            <span style='color: #FFD700;'>🤖</span> 
            <span style='background: -webkit-linear-gradient(left, #7267EF, #00D2FF); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>Agentic</span>
            <span style='background: -webkit-linear-gradient(left, #00D2FF, #2ecc71); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>BI</span>
        </h2>
        <p style='background: -webkit-linear-gradient(right, #a8c0ff, #3f2b96); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 0.8rem; font-weight: 900; margin-top: 5px; letter-spacing: 1px;'>
            SAAS INTELLIGENT ANALYTICS
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # 2. Developer Profile Profile
    st.markdown("### 👨‍💻 Developer")
    st.markdown("""
    <div style='background: linear-gradient(135deg, rgba(114, 103, 239, 0.2) 0%, rgba(0, 210, 255, 0.2) 100%); 
                padding: 15px; border-radius: 10px; border: 2px solid rgba(114, 103, 239, 0.4);'>
        <p style='margin: 5px 0; color: #00D2FF; font-weight: 600;'>Ratnesh Kumar Singh</p>
        <p style='margin: 5px 0; font-size: 0.9rem; color: #e0e0e0;'>
            Data Scientist (AI/ML) | 4+ Yrs
        </p>
        <div style='margin-top: 10px; font-size: 0.9rem;'>
            <a href='https://github.com/Ratnesh-181998' style='color: #ffffff; text-decoration: none; background-color: #24292e; padding: 4px 8px; border-radius: 4px; border: 1px solid #444;'>
                🔗 GitHub
            </a> 
            &nbsp;
            <a href='https://www.linkedin.com/in/ratneshkumar1998/' style='color: #ffffff; text-decoration: none; background-color: #0077b5; padding: 4px 8px; border-radius: 4px; border: 1px solid #444;'>
                💼 LinkedIn
            </a>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.info("**Agentic BI** empowers enterprises to query data using natural language, leveraging a Multi-Agent architecture for high-precision SQL generation and visualization.")

    st.markdown("---")
    
    # 3. User Resources
    st.markdown("### 📚 User Guide")
    try:
        with open("all_questions_list.txt", "rb") as file:
            st.download_button(
                label="📥 Download All Prompts",
                data=file,
                file_name="agentic_bi_prompts.txt",
                mime="text/plain",
                help="Get the full list of 24 supported Quick Start Questions to try out!",
                use_container_width=True
            )
    except FileNotFoundError:
        st.warning("Prompts file not found.")





# --- TOP BADGE (Developer Credential) ---
col_h1, col_h2 = st.columns([3, 1])
with col_h1:
    st.markdown("")  # Spacer for alignment
with col_h2:
    st.markdown("""
<div style='background: linear-gradient(135deg, #7267EF 0%, #00D2FF 100%); padding: 10px 15px; border-radius: 12px; box-shadow: 0 4px 20px rgba(114, 103, 239, 0.4); border: 1px solid rgba(255, 255, 255, 0.3); text-align: center; margin-bottom: 5px; transition: transform 0.2s;'>
    <p style='margin: 0; color: #ffffff; font-weight: 800; font-size: 0.9rem; line-height: 1.2; letter-spacing: 0.5px;'>Ratnesh Kumar Singh</p>
    <p style='margin: 2px 0 8px 0; color: rgba(255, 255, 255, 0.9); font-size: 0.75rem; font-weight: 600;'>Data Scientist (AI/ML) | 4+ Yrs</p>
    <div style='display: flex; justify-content: center; gap: 15px; border-top: 1px solid rgba(255,255,255,0.3); padding-top: 8px;'>
        <a href='https://github.com/Ratnesh-181998' target='_blank' style='color: white; text-decoration: none; font-size: 0.8rem; font-weight: 700; display: flex; align-items: center; gap: 5px;'>
            <img src="https://img.icons8.com/ios-filled/50/ffffff/github.png" width="16" height="16"/> GitHub
        </a>
        <a href='https://www.linkedin.com/in/ratneshkumar1998/' target='_blank' style='color: white; text-decoration: none; font-size: 0.8rem; font-weight: 700; display: flex; align-items: center; gap: 5px;'>
            <img src="https://img.icons8.com/ios-filled/50/ffffff/linkedin.png" width="16" height="16"/> LinkedIn
        </a>
    </div>
</div>
""", unsafe_allow_html=True)

# --- HERO HEADER (Premium UI) ---
st.markdown("""
<div style='text-align: center; padding: 30px 20px; background: linear-gradient(135deg, rgba(114, 103, 239, 0.1) 0%, rgba(0, 210, 255, 0.1) 100%); border-radius: 15px; margin-bottom: 25px; border: 1px solid rgba(114, 103, 239, 0.3); box-shadow: 0 8px 32px rgba(0,0,0,0.2);'>
    <div style='display: flex; align-items: center; justify-content: center; gap: 15px; margin-bottom: 10px;'>
        <span style='font-size: 2.5rem;'>🤖</span>
        <h1 style='color: #00D2FF; margin: 0; font-size: 2.5rem; font-weight: 800; text-shadow: 0 0 25px rgba(0, 210, 255, 0.4); letter-spacing: 2px; line-height: 1; font-family: "Inter", sans-serif;'>
            AGENTIC BI SAAS
        </h1>
    </div>
    <p style='font-size: 1.2rem; color: #e2e8f0; font-weight: 500; margin: 5px 0 0 0; letter-spacing: 0.5px;'>
        Next-Gen <b style='color: #7267EF;'>Natural Language Querying</b> Powered by Multi-Agent AI
    </p>
</div>
""", unsafe_allow_html=True)

# Tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🚀 Live Demo", 
    "ℹ️ About Project", 
    "🛠️ Tech Stack", 
    "📐 HLD & LLD", 
    "🏗️ Architecture", 
    "📝 System Logs"
])

# --- TAB 1: LIVE DEMO ---
with tab1:
    # Initialize Chat History (Must be at the top)
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # 1. Header Section
    # 1. Header Section
    st.markdown("""
    <div style='background: rgba(114, 103, 239, 0.1); padding: 20px; border-radius: 10px; border-left: 5px solid #7267EF; margin-bottom: 20px;'>
        <h3 style='margin: 0; color: #ffff;'>Agentic Ratnesh AI Analyst</h3>
        <p style='margin: 5px 0 0 0; color: #e2e8f0;'>Asking questions to your data has never been easier. Driven by <b>Multi-Agent LangGraph</b>. Type a question or pick a sample below to see the <b>Agentic Swarm</b> in action.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 2. How to Use Section
    st.markdown("""
<div style='background: linear-gradient(135deg, rgba(52, 152, 219, 0.1) 0%, rgba(46, 204, 113, 0.1) 100%); padding: 20px; border-radius: 12px; border: 1px solid rgba(52, 152, 219, 0.3); margin-bottom: 25px;'>
<h4 style='color: #3498db; margin: 0 0 15px 0; font-weight: 700;'>📚 How to Use This Live Demo</h4>
<div style='color: #e2e8f0; line-height: 1.8;'>
<p style='margin: 8px 0;'><span style='background: rgba(52, 152, 219, 0.3); padding: 3px 10px; border-radius: 12px; font-weight: 600;'>Step 1</span> <b>Choose a Quick Prompt</b> from the expandable categories below, or write your question.</p>
<p style='margin: 8px 0;'><span style='background: rgba(155, 89, 182, 0.3); padding: 3px 10px; border-radius: 12px; font-weight: 600;'>Step 2</span> Click the <b>🚀 Analyze Data</b> button to send your query to the AI Agent Swarm.</p>
<p style='margin: 8px 0;'><span style='background: rgba(46, 204, 113, 0.3); padding: 3px 10px; border-radius: 12px; font-weight: 600;'>Step 3</span> View the <b>KPIs, Charts, and Data Tables</b> generated by the intelligent agents.</p>
<p style='margin: 8px 0;'><span style='background: rgba(230, 126, 34, 0.3); padding: 3px 10px; border-radius: 12px; font-weight: 600;'>Step 4</span> Expand <b>"🔍 See Generated SQL & Reasoning"</b> to understand how the AI analyzed your request.</p>
</div>
<div style='margin-top: 15px; padding: 10px; background: rgba(0, 0, 0, 0.2); border-radius: 8px; border-left: 3px solid #f39c12;'>
<p style='color: #f39c12; margin: 0; font-size: 0.9rem;'>💡 <b>Pro Tip:</b> The system has <b>memory</b> - try asking follow-up questions like "Now show that for only the North region"!</p>
</div>
</div>
    """, unsafe_allow_html=True)
    
    
    
    # 2. Quick Prompts (User Interactive)
    if "main_query_input" not in st.session_state:
        st.session_state.main_query_input = ""
    
    def set_query(text):
        st.session_state.main_query_input = text
    
    st.write("###### ⚡ Quick Start Prompts Library:")
    
    # Vertical Expanders for Prompt Categories (Enterprise Edition)
    with st.expander("💰 Finance & Strategy", expanded=True):
        c1, c2 = st.columns(2)
        if c1.button("📊 Budget vs Actual '25", use_container_width=True): set_query("Compare allocated budget vs actual spend by department for all quarters of 2025.")
        if c2.button("💸 High Expense Depts", use_container_width=True): set_query("Which departments have the highest total expenses across 2024 and 2025?")
        c3, c4 = st.columns(2)
        if c3.button("📅 2026 Revenue Project", use_container_width=True): set_query("What is the total projected revenue for each month in 2026 based on current sales?")
        if c4.button("📉 Variance Analysis", use_container_width=True): set_query("Show me departments where actual spend exceeded the budget by more than 10%.")
        c5, c6 = st.columns(2)
        if c5.button("🏢 OpEx Breakdown", use_container_width=True): set_query("Break down total operating expenses by category for the last 12 months.")
        if c6.button("💎 ROI per Region", use_container_width=True): set_query("Calculate regional ROI by comparing marketing spend vs sales revenue for each region.")

    with st.expander("👥 CRM & Retention", expanded=False):
        c1, c2 = st.columns(2)
        if c1.button("📉 Churn Reasons", use_container_width=True): set_query("What are the top 3 reasons for customer churn in the last year?")
        if c2.button("🔄 Subscription Health", use_container_width=True): set_query("Show me the count of active vs canceled subscriptions across all plans.")
        c3, c4 = st.columns(2)
        if c3.button("🥇 Top Loyalty Tiers", use_container_width=True): set_query("Which loyalty tier (Gold/Silver/Bronze) has the highest total lifetime spend?")
        if c4.button("📅 Signup Trends", use_container_width=True): set_query("Show a monthly trend of new customer signups from 2023 to 2025.")
        c5, c6 = st.columns(2)
        if c5.button("🤝 Acquisition ROI", use_container_width=True): set_query("Compare the total spend of customers acquired through Google Ads vs Referrals.")
        if c6.button("🍰 Plan Revenue Mix", use_container_width=True): set_query("Show me the MRR (Monthly Recurring Revenue) share percentage of SaaS Pro vs Elite.")

    with st.expander("📣 Growth & Marketing", expanded=False):
        c1, c2 = st.columns(2)
        if c1.button("🌐 Traffic vs Leads", use_container_width=True): set_query("Show me the correlation between website sessions and marketing conversions for 2024.")
        if c2.button("🤺 Competitor Price Gap", use_container_width=True): set_query("Compare our SaaS Pro price against the average competitor market price.")
        c3, c4 = st.columns(2)
        if c3.button("📈 Best Campaign ROI", use_container_width=True): set_query("Identify the marketing campaign with the single highest ROI ever recorded.")
        if c4.button("📱 Mobile vs Desktop", use_container_width=True): set_query("Compare the conversion rates of Mobile traffic vs Desktop traffic.")
        c5, c6 = st.columns(2)
        if c5.button("🎯 Channel Efficiency", use_container_width=True): set_query("Which marketing channel (FB, GAds, LI) has the lowest cost-per-conversion?")
        if c6.button("⭐ Review Sentiments", use_container_width=True): set_query("Analyze the impact of product reviews on regional sales growth.")

    with st.expander("⚙️ Operations & Support", expanded=False):
        c1, c2 = st.columns(2)
        if c1.button("🎫 Support SLA Health", use_container_width=True): set_query("Show me the average resolution time for High Priority tickets by support agent.")
        if c2.button("📦 Low Stock Alerts", use_container_width=True): set_query("List all products where the current quantity on hand is below the reorder point.")
        c3, c4 = st.columns(2)
        if c3.button("🎖️ Top Sales Reps", use_container_width=True): set_query("Rank our top 5 Sales Reps by their Actual Sales vs Quota performance.")
        if c4.button("💳 Expense Audit", use_container_width=True): set_query("Identify all non-tax-deductible expenses greater than $5000 in the IT department.")
        c5, c6 = st.columns(2)
        if c5.button("🏢 Warehouse Load", use_container_width=True): set_query("Show the distribution of inventory quantity across all warehouse locations.")
        if c6.button("⭐ Cust Satisfaction", use_container_width=True): set_query("Calculate the average customer satisfaction score for bug-related tickets.")

    with st.expander("💡 Pro-Tip: Memory System", expanded=False):
        st.info("""
        **💡 Intelligent Memory System**
        
        The agent is powered by **Llama 3.3 (Groq)** and has a memory of your previous questions thanks to **Mem0**.
        
        **Try asking follow-up questions:**
        1. "Show me revenue for the North region"
        2. "Now filter that for only 'SaaS Pro'"
        
        *The agent understands "that" refers to the North region revenue context!*
        """)
    
    
    
    st.markdown("<div style='margin-bottom: 15px;'></div>", unsafe_allow_html=True)

    current_date_str = datetime.now().strftime("%B %Y")
    st.markdown(f"""
<h4 style='color: #3498db; margin: 20px 0 5px 0; font-weight: 700; font-size: 1.3rem;'>
�️ System Scope
</h4>
<hr style='border: 1px solid #e74c3c; background-color: #e74c3c; opacity: 1; margin: 0 0 10px 0;'>
<p style='color: #f1c40f; font-size: 0.95rem; font-weight: 700; margin-bottom: 15px;'>
    <span style='color: #ffffff; font-weight: 600;'>This AI is <span style='color: #3498db;'>Domain-Locked</span> for SaaS Business Intelligence. It analyzes performance strictly between <span style='color: #2ecc71;'>January 2023 and December 2026</span>. General knowledge or out-of-range queries are automatically restricted to maintain analytical precision.</span>
</p>
<div style='background: rgba(255, 255, 255, 0.05); padding: 15px; border-radius: 12px; border: 1px dashed rgba(255, 255, 255, 0.2); margin-bottom: 25px;'>
    <p style='color: #bdc3c7; font-size: 0.85rem; margin: 0 0 12px 0; font-weight: 600; text-transform: uppercase; letter-spacing: 1px;'>🏛️ Enterprise Data Catalog (15+ Modules):</p>
    <div style='display: flex; flex-wrap: wrap; gap: 8px;'>
        <span style='background: #2ecc7122; color: #2ecc71; border: 1px solid #2ecc7144; padding: 2px 10px; border-radius: 15px; font-size: 0.75rem; font-weight: 600;'>💰 Sales & Revenue</span>
        <span style='background: #3498db22; color: #3498db; border: 1px solid #3498db44; padding: 2px 10px; border-radius: 15px; font-size: 0.75rem; font-weight: 600;'>👥 Customers (CRM)</span>
        <span style='background: #9b59b622; color: #9b59b6; border: 1px solid #9b59b644; padding: 2px 10px; border-radius: 15px; font-size: 0.75rem; font-weight: 600;'>📦 Product Catalog</span>
        <span style='background: #e67e2222; color: #e67e22; border: 1px solid #e67e2244; padding: 2px 10px; border-radius: 15px; font-size: 0.75rem; font-weight: 600;'>📍 Regions & Geo</span>
        <span style='background: #e74c3c22; color: #e74c3c; border: 1px solid #e74c3c44; padding: 2px 10px; border-radius: 15px; font-size: 0.75rem; font-weight: 600;'>📣 Marketing ROI</span>
        <span style='background: #1abc9c22; color: #1abc9c; border: 1px solid #1abc9c44; padding: 2px 10px; border-radius: 15px; font-size: 0.75rem; font-weight: 600;'>🔄 Subscriptions (MRR)</span>
        <span style='background: #f1c40f22; color: #f1c40f; border: 1px solid #f1c40f44; padding: 2px 10px; border-radius: 15px; font-size: 0.75rem; font-weight: 600;'>🎫 Support Tickets</span>
        <span style='background: #34495e22; color: #34495e; border: 1px solid #34495e44; padding: 2px 10px; border-radius: 15px; font-size: 0.75rem; font-weight: 600;'>🏢 Inventory/Whse</span>
        <span style='background: #d3540022; color: #d35400; border: 1px solid #d3540044; padding: 2px 10px; border-radius: 15px; font-size: 0.75rem; font-weight: 600;'>🎖️ HR Performance</span>
        <span style='background: #7f8c8d22; color: #7f8c8d; border: 1px solid #7f8c8d44; padding: 2px 10px; border-radius: 15px; font-size: 0.75rem; font-weight: 600;'>📈 Web Traffic</span>
        <span style='background: #c0392b22; color: #c0392b; border: 1px solid #c0392b44; padding: 2px 10px; border-radius: 15px; font-size: 0.75rem; font-weight: 600;'>💸 Exp & Vendor</span>
        <span style='background: #8e44ad22; color: #8e44ad; border: 1px solid #8e44ad44; padding: 2px 10px; border-radius: 15px; font-size: 0.75rem; font-weight: 600;'>🤺 Competitor Int</span>
        <span style='background: #27ae6022; color: #27ae60; border: 1px solid #27ae6044; padding: 2px 10px; border-radius: 15px; font-size: 0.75rem; font-weight: 600;'>📉 Churn Analysis</span>
        <span style='background: #2980b922; color: #2980b9; border: 1px solid #2980b944; padding: 2px 10px; border-radius: 15px; font-size: 0.75rem; font-weight: 600;'>⭐ Product Reviews</span>
        <span style='background: #f39c1222; color: #f39c12; border: 1px solid #f39c1244; padding: 2px 10px; border-radius: 15px; font-size: 0.75rem; font-weight: 600;'>📝 Op Budgets</span>
    </div>
</div>
    """, unsafe_allow_html=True)
    
    # RELOCATED DATABASE TOOLS
    with st.expander("🛠️ Advanced Database & Catalog Options", expanded=False):
        col_db1, col_db2 = st.columns([1, 2])
        
        with col_db1:
            st.markdown("##### ⚙️ System Reset")
            if st.button("🌱 Seed Database", use_container_width=True):
                if seed_data:
                    with st.spinner("Seeding database..."):
                        seed_data()
                    st.success("✅ Database seeded with 500 records!")
                    log_event("Database Reset", "User re-seeded the demo database.")
                else:
                    st.error("Seed script not found!")
            
            st.markdown("---")
            st.markdown("##### 📖 Developer Note")
            st.caption("To expand this **Data Catalog**, update `seed_db.py` schema and the UI tags in `presentation_app.py`.")

        with col_db2:
            st.markdown("##### ➕ Add Custom Record")
            with st.form("manual_entry_tab"):
                f1, f2 = st.columns(2)
                new_rev = f1.number_input("Revenue ($)", min_value=0.0, value=500.0)
                new_date = f2.date_input("Transaction Date", value=datetime.now())
                
                f3, f4 = st.columns(2)
                new_region = f3.selectbox("Region", ["North", "South", "East", "West"])
                new_prod = f4.selectbox("Product", ["SaaS Pro", "SaaS Elite", "SaaS Basic"])

                f5, f6 = st.columns(2)
                new_cust_id = f5.number_input("Customer ID", min_value=1, step=1, value=1)
                new_qty = f6.number_input("Quantity", min_value=1, step=1, value=1)

                f7, f8, f9 = st.columns(3)
                new_price = f7.number_input("Unit Price", min_value=0.0, value=new_rev)
                new_tax = f8.number_input("Tax", min_value=0.0, value=new_rev * 0.1)
                new_disc = f9.number_input("Discount", min_value=0.0, value=0.0)
                
                if st.form_submit_button("Submit Enterprise Record to Database", use_container_width=True):
                    try:
                        import sqlite3
                        conn = sqlite3.connect('demo.db')
                        cursor = conn.cursor()
                        # Matching the 10-column Enterprise Schema (transaction_id is auto)
                        cursor.execute('''
                            INSERT INTO sales (revenue, date, region, product, customer_id, discount, quantity, unit_price, tax) 
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
                            (new_rev, new_date.strftime('%Y-%m-%d'), new_region, new_prod, 
                             new_cust_id, new_disc, new_qty, new_price, new_tax))
                        conn.commit()
                        conn.close()
                        st.success("✅ Enterprise Record Successfully Injected!")
                        log_event("Manual Entry", f"Injected: ${new_rev} | {new_region} | {new_prod} | Cust:{new_cust_id}")
                    except Exception as e:
                        st.error(f"Schema Mismatch Error: {e}")
                        log_event("Error", f"Manual Entry Failed: {e}")
    
    # Input Section (Moved to Bottom)


    # Results Section Title (Always Visible)
    st.markdown("<div style='margin-top: 40px;'></div>", unsafe_allow_html=True)
    st.markdown("""
<div style='text-align: center; padding: 10px; margin-bottom: 5px;'>
    <h2 style='color: #ffffff; font-weight: 800; margin: 0; font-size: 1.8rem; text-transform: uppercase; letter-spacing: 1px; white-space: nowrap;'>
    ✨ QUERIES - ANSWER'S TO <span style='color: #3498db;'>RATNESH AI ANALYST</span>
    </h2>
</div>
<hr style='border: 1px solid #e74c3c; background-color: #e74c3c; opacity: 1; margin: 5px 0 30px 0;'>
    """, unsafe_allow_html=True)

    # --- CHAT THREAD DISPLAY ---
    if st.session_state.chat_history:
        st.markdown("#### 💬 Conversation Thread")
        for i, turn in enumerate(st.session_state.chat_history):
            # User Message
            st.markdown(f"""
            <div style='background: rgba(52, 152, 219, 0.1); padding: 15px; border-radius: 12px; margin-bottom: 10px; border-left: 5px solid #3498db; box-shadow: 0 2px 5px rgba(0,0,0,0.1);'>
                <p style='color: #3498db; font-weight: 700; margin: 0 0 5px 0; font-size: 0.85rem; text-transform: uppercase;'>👤 User</p>
                <p style='color: #ffffff; margin: 0; line-height: 1.5;'>{turn['user']}</p>
            </div>
            """, unsafe_allow_html=True)
            # AI Summary (Using markdown for multi-line support)
            st.markdown(f"""
            <div style='background: rgba(46, 204, 113, 0.05); padding: 15px; border-radius: 12px 12px 0 0; border-left: 5px solid #2ecc71; margin-bottom: 0;'>
                <p style='color: #2ecc71; font-weight: 700; margin: 0; font-size: 0.85rem; text-transform: uppercase;'>🤖 Ratnesh AI Analyst</p>
            </div>
            """, unsafe_allow_html=True)
            st.markdown(f"""
            <div style='background: rgba(46, 204, 113, 0.05); padding: 0 15px 15px 15px; border-radius: 0 0 12px 12px; border-left: 5px solid #2ecc71; margin-bottom: 25px;'>
                <div style='color: #ecf0f1; font-style: normal; line-height: 1.6;'>
            """, unsafe_allow_html=True)
            st.markdown(turn['ai'])
            st.markdown("</div></div>", unsafe_allow_html=True)
            
            # RENDER DATA WITHIN CHAT THREAD
            if "full_data" in turn:
                with st.expander(f"📊 View Analysis Details for Question {i+1}", expanded=(i == len(st.session_state.chat_history)-1)):
                    render_data_results(turn["full_data"], turn_index=i)
            
            # Integrated Feedback Row for THIS turn
            _, feed_col, _ = st.columns([1, 2, 1])
            with feed_col:
                fc1, fc2, fc3 = st.columns([3, 1, 1])
                with fc1:
                    st.markdown("<div style='text-align: right; padding-top: 5px; font-weight: 600; color: #bdc3c7; font-size: 0.8rem;'>Was this answer helpful?</div>", unsafe_allow_html=True)
                with fc2:
                    if st.button("👍", key=f"thumbs_up_{i}", help="Yes, this was helpful"):
                        st.toast("Thanks for the feedback!", icon="⭐")
                        log_event("Thumbs Up", f"Query: {turn['user']}")
                with fc3:
                    if st.button("👎", key=f"thumbs_down_{i}", help="No, this needs improvement"):
                        st.toast("Noted, we'll improve!", icon="🔧")
                        log_event("Thumbs Down", f"Query: {turn['user']}")
            
            st.markdown("<div style='margin-bottom: 25px;'></div>", unsafe_allow_html=True)

                    
        st.markdown("<hr style='border-top: 1px dashed #444; margin-bottom: 40px;'>", unsafe_allow_html=True)

    # Results display moved to chat thread
    pass

    # --- QUICK FEEDBACK SECTION (Relocated to Bottom) ---
    st.markdown("<div style='margin-top: 40px;'></div>", unsafe_allow_html=True)
    st.markdown("""
    <style>
    .feedback-container {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 25px;
        padding: 15px 30px;
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.05) 0%, rgba(255, 255, 255, 0.02) 100%);
        border-radius: 100px;
        width: fit-content;
        margin: 0 auto;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    .feedback-text {
        color: #ecf0f1;
        font-size: 1rem;
        font-weight: 600;
    }
    </style>
    """, unsafe_allow_html=True)
    

    



    # --- INPUT SECTION (MOVED TO BOTTOM) ---
    st.markdown("<div style='margin-top: 50px;'></div>", unsafe_allow_html=True)
    
    # Callback function for Clear button (Complete Reset)
    def clear_input():
        st.session_state.main_query_input = ""
        st.session_state.show_result = False
        if "query_result" in st.session_state:
            del st.session_state["query_result"]
    
    # Heading for Input Section
    st.markdown("""
    <h4 style='color: #3498db; margin: 0 0 10px 0; font-weight: 700; font-size: 1.2rem;'>
    💬 Your Query - Answering to Ratnesh AI Analyst
    </h4>
    """, unsafe_allow_html=True)

    # Input bound to session state - Using text_area for larger input field
    q = st.text_area("Question Input", 
                      placeholder="e.g., Show me total revenue by region for last month",
                      key="main_query_input",
                      label_visibility="collapsed",
                      height=100)

    # Colorful Button Row: Analyze Data, Enter, Clear, Download, Feedback
    btn_col1, btn_col2, btn_col3, btn_col4, btn_col5 = st.columns(5)
    
    # Custom CSS for colorful buttons with distinct colors
    st.markdown("""
    <style>
    /* Analyze Data Button - Blue */
    div[data-testid="column"]:nth-child(1) button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }
    div[data-testid="column"]:nth-child(1) button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6) !important;
    }
    
    /* Enter Button - Green */
    div[data-testid="column"]:nth-child(2) button {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%) !important;
        color: white !important;
        border: none !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }
    div[data-testid="column"]:nth-child(2) button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(56, 239, 125, 0.6) !important;
    }
    
    /* Clear Button - Red/Orange */
    div[data-testid="column"]:nth-child(3) button {
        background: linear-gradient(135deg, #ee0979 0%, #ff6a00 100%) !important;
        color: white !important;
        border: none !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }
    div[data-testid="column"]:nth-child(3) button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(255, 106, 0, 0.6) !important;
    }
    
    /* Download Button - Purple */
    div[data-testid="column"]:nth-child(4) button {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%) !important;
        color: #333 !important;
        border: none !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }
    div[data-testid="column"]:nth-child(4) button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(168, 237, 234, 0.6) !important;
    }
    
    /* Feedback Button - Teal */
    div[data-testid="column"]:nth-child(5) button {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%) !important;
        color: white !important;
        border: none !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }
    div[data-testid="column"]:nth-child(5) button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(245, 87, 108, 0.6) !important;
    }
    </style>
    """, unsafe_allow_html=True)
    

    # Logic for handling query submission (Callback to safely clear input)
    def submit_query():
        q = st.session_state.main_query_input
        if not q:
            st.warning("Please enter a valid query.")
            return

        log_event("Query Initiated", f"Question: {q}")
        
        # Mock Response Class
        class MockResponse:
            def __init__(self, json_data, status_code=200):
                self._json = json_data
                self.status_code = status_code
            def json(self): return self._json

        try:
            # 3. Robust Backend Call
            try:
                # Pass history for context
                history_context = []
                for turn in st.session_state.chat_history[-5:]:
                    history_context.append(f"User: {turn['user']}")
                    history_context.append(f"AI: {turn['ai']}")
                    
                response = requests.post("http://localhost:8000/ask", json={
                    "tenant_id": "t1", "user_id": "u1", "question": q, "history": history_context
                }, timeout=10)
            except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
                # Fallback to Direct Agent Execution (Streamlit Cloud mode)
                log_event("Backend Unavailable", "Running agents locally in Streamlit")
                
                try:
                    # Import the LangGraph orchestration directly
                    import sys
                    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
                    from app.langgraph.graph import bi_graph
                    from app.billing.metering import record_usage
                    
                    # Run agents directly using the compiled graph
                    result = bi_graph.invoke({
                        "tenant_id": "t1",
                        "user_id": "u1", 
                        "question": q,
                        "history": history_context
                    })
                    
                    # Record usage
                    record_usage("t1", "query", 1)
                    
                    # Extract response
                    response = MockResponse(result.get("response", result))
                    log_event("Query Success", "Direct Agent Execution Completed Successfully")
                    log_event("Local Agents Success", f"Processed query: {q[:50]}...")
                    
                except Exception as agent_error:
                    # If agents also fail, show error to user
                    import traceback
                    error_details = traceback.format_exc()
                    log_event("Agent Error", f"{str(agent_error)}\n{error_details[:200]}")
                    st.error(f"⚠️ **Error running AI agents:** {str(agent_error)}")
                    st.session_state.show_result = False
                    return

            if response.status_code == 200:
                data = response.json()
                
                # Check for backend-level errors (like 429 Rate Limits from LLM)
                if "error" in data:
                    st.error(f"⚠️ **AI Agent Error:** {data['error']}")
                    log_event("Query Error", f"Backend reported: {data['error'][:100]}")
                    st.session_state.show_result = False
                    return

                log_event("Query Success", "Received 200 OK from Backend")
                
                # Build User/AI turn
                kpis = data.get("kpis", {})
                reasoning = data.get("reasoning", "Analysis optimized and completed successfully.")
                metric_label = kpis.get('primary_label', 'Records')
                metric_val = kpis.get('primary_val', 0)
                
                formatted_val = f"${metric_val:,.2f}" if any(x in metric_label.lower() for x in ['revenue', 'sales', 'spend', 'price', 'budget']) else f"{metric_val:,.0f}"
                ai_message = f"{reasoning}\n\n**Key Metric ({metric_label}):** {formatted_val}"
                
                # STORE IN HISTORY
                st.session_state.chat_history.append({
                    "user": q, 
                    "ai": ai_message,
                    "full_data": data 
                })
                
                st.session_state.query_result = data
                st.session_state.show_result = True
                st.session_state.main_query_input = "" # Clear input safely
                
            else:
                st.error(f"Error {response.status_code}: {response.text}")
                log_event("Query Error", f"Status: {response.status_code}")
                st.session_state.show_result = False
                
        except Exception as e:
            # Handle Simulation fallback errors if strictly needed, or generic error
            if SIMULATION_MODE:
                 # Simplified simulation fallback for generic errors
                 st.session_state.chat_history.append({
                     "user": q, 
                     "ai": "Simulated Response: Analysis Complete.",
                     "full_data": {"kpis": {}, "data": []}
                 })
                 st.session_state.show_result = True
                 st.session_state.main_query_input = ""
            else: 
                log_event("Connection Error", str(e))
                # We can't show st.error easily in callback so we use toast or just let it pass to main
                # ideally we set a state to show error
                st.session_state.last_error = str(e)

    analyze_clicked = btn_col1.button("🚀 Analyze Data", use_container_width=True, on_click=submit_query)
    enter_clicked = btn_col2.button("✅ Enter", use_container_width=True, on_click=submit_query)
    
    def clear_all():
        st.session_state.input_query = ""
        st.session_state.chat_history = []
        st.session_state.query_result = None
        st.session_state.show_result = False

    clear_clicked = btn_col3.button("🗑️ Clear", use_container_width=True, key="clear_btn", on_click=clear_all)
    download_clicked = btn_col4.button("📥 Download", use_container_width=True, key="download_btn")
    feedback_clicked = btn_col5.button("💬 Feedback", use_container_width=True, key="feedback_btn")
    
    # Clear button now uses on_click callback - no manual logic needed here
    
    # Download button logic
    if download_clicked:
        if "query_result" in st.session_state:
            result_data = st.session_state.query_result
            # Create downloadable text content
            txt_content = f"""AGENTIC BI QUERY RESULT
=====================================
Question: {q if q else 'N/A'}

KPIs:
-----
Revenue: ${result_data.get('kpis', {}).get('revenue', 'N/A')}
Growth: {result_data.get('kpis', {}).get('growth', 'N/A')}
YoY: {result_data.get('kpis', {}).get('yoy', 'N/A')}

Generated SQL:
--------------
{result_data.get('sql', 'N/A')}

Agent Reasoning:
----------------
{result_data.get('reasoning', 'N/A')}

Data:
-----
{result_data.get('data', 'N/A')}
"""
            st.download_button(
                label="💾 Download Results as TXT",
                data=txt_content,
                file_name=f"query_result_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain",
                use_container_width=True
            )
        else:
            st.warning("⚠️ No results to download. Please run a query first.")
    
    # Feedback button logic
    if feedback_clicked:
        st.info("💬 **Feedback Form**\n\nPlease share your thoughts about this AI analyst experience:")
        feedback_text = st.text_area("Your feedback:", key="feedback_input", height=100)
        if st.button("📨 Submit Feedback"):
            if feedback_text:
                log_event("Feedback Submitted", feedback_text)
                st.success("✅ Thank you for your feedback!")
            else:
                st.warning("Please enter your feedback before submitting.")
    
    # Display error if it occurred in callback
    if "last_error" in st.session_state and st.session_state.last_error:
        st.error(f"Connection Failed: {st.session_state.last_error}")
        st.info("Ensure the FastAPI backend is running on port 8000.")
        st.session_state.last_error = None # Clear after showing


# --- TAB 2: ABOUT ---
with tab2:
    # 1. Premium Header / Vision Section
    st.markdown("""
    <div style='background: linear-gradient(135deg, rgba(40, 116, 240, 0.1) 0%, rgba(155, 89, 182, 0.1) 100%); 
                padding: 30px; border-radius: 15px; border-left: 5px solid #00d4ff; margin-bottom: 30px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.2);'>
        <h2 style='color: #00d4ff; margin: 0 0 10px 0; font-weight: 800;'>🎯 Project Vision & Mission</h2>
        <p style='color: #e8e8e8; font-size: 1.1rem; line-height: 1.6;'>
            <b>Agentic BI SaaS</b> is an enterprise-grade Business Intelligence platform powered by Agentic AI. 
            Users can ask business questions in plain English, and the system intelligently converts them into 
            trusted, governed, explainable insights.
        </p>
        <p style='color: #bdc3c7; font-size: 1.0rem; margin-top: 10px; font-style: italic;'>
            "To democratize data access within enterprises, reducing the dependency on data analyst teams for routine reporting."
        </p>
        <hr style='border-color: rgba(255,255,255,0.1); margin: 20px 0;'>
        <div style='display: flex; gap: 15px; align-items: center;'>
            <div style='background: rgba(40, 116, 240, 0.2); padding: 5px 15px; border-radius: 20px; color: #00d4ff; font-weight: bold; font-size: 0.85rem;'>🚀 AI Analyst</div>
            <div style='background: rgba(155, 89, 182, 0.2); padding: 5px 15px; border-radius: 20px; color: #9b59b6; font-weight: bold; font-size: 0.85rem;'>🧠 Long-Term Memory</div>
            <div style='background: rgba(46, 204, 113, 0.2); padding: 5px 15px; border-radius: 20px; color: #2ecc71; font-weight: bold; font-size: 0.85rem;'>🔐 Enterprise Gov</div>
        </div>
        <p style='color: #e8e8e8; margin-top: 20px; font-weight: 500;'>
            In simple words: This system replaces manual BI dashboards with an <span style='color: #00d4ff;'>AI analyst</span> that remembers, learns, and scales securely.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")

    # 2. Agent Team (Cards Style)
    st.subheader("🤖 Meet the Agent Team")
    st.markdown("<p style='color: #bdc3c7; margin-bottom: 20px;'>A coordinated swarm of specialized AI agents working together to answer your questions.</p>", unsafe_allow_html=True)
    
    # CSS for cards
    st.markdown("""
    <style>
    .agent-card {
        background: rgba(30, 41, 59, 0.4);
        padding: 20px;
        border-radius: 12px;
        border: 1px solid rgba(255,255,255,0.1);
        height: 100%;
        transition: transform 0.2s;
    }
    .agent-card:hover {
        transform: translateY(-5px);
        border-color: #00d4ff;
        background: rgba(30, 41, 59, 0.7);
    }
    .agent-icon { font-size: 2rem; margin-bottom: 10px; display: block; }
    .agent-title { color: #fff; font-weight: 700; font-size: 1.1rem; margin-bottom: 8px; }
    .agent-desc { color: #a0aec0; font-size: 0.9rem; line-height: 1.4; margin-bottom: 0; }
    </style>
    """, unsafe_allow_html=True)

    # Row 1
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""
        <div class="agent-card">
            <span class="agent-icon">🗂️</span>
            <div class="agent-title">1. Metadata Agent</div>
            <ul class="agent-desc" style="padding-left: 1.2rem;">
                <li>Understands database schema</li>
                <li>Identifies tables & columns</li>
                <li>Prevents hallucinated SQL</li>
                <li>Reads user preferences</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="agent-card">
            <span class="agent-icon">📑</span>
            <div class="agent-title">2. RAG Agent</div>
            <ul class="agent-desc" style="padding-left: 1.2rem;">
                <li>Retrieves certified reports</li>
                <li>Ensures enterprise trust</li>
                <li>Overrides DB queries if needed</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown("""
        <div class="agent-card">
            <span class="agent-icon">💻</span>
            <div class="agent-title">3. SQL Agent</div>
            <ul class="agent-desc" style="padding-left: 1.2rem;">
                <li>Converts Natural Language to SQL</li>
                <li>Uses LLMs (Cloud or Local)</li>
                <li>Respects governance rules</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    # Spacer
    st.write("")

    # Row 2
    c4, c5, c6 = st.columns(3)
    with c4:
        st.markdown("""
        <div class="agent-card">
            <span class="agent-icon">🛡️</span>
            <div class="agent-title">4. Impact Agent</div>
            <ul class="agent-desc" style="padding-left: 1.2rem;">
                <li><b>Safety Guard</b>: Blocks risky queries</li>
                <li>Analyzes SQL cost & risk</li>
                <li>Protects DB performance</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    with c5:
        st.markdown("""
        <div class="agent-card">
            <span class="agent-icon">⚡</span>
            <div class="agent-title">5. Execute Agent</div>
            <ul class="agent-desc" style="padding-left: 1.2rem;">
                <li>Executes SQL securely</li>
                <li>Tenant-isolated access</li>
                <li>Returns only required data</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    with c6:
        st.markdown("""
        <div class="agent-card">
            <span class="agent-icon">📊</span>
            <div class="agent-title">6. BI Agent</div>
            <ul class="agent-desc" style="padding-left: 1.2rem;">
                <li>Converts raw data to KPIs</li>
                <li>Generates insights & explanations</li>
                <li>Builds dashboard config</li>
                <li><b>Writes to Memory</b></li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # 3. End-to-End Flow (Visual Pipeline)
    st.subheader("🔄 End-to-End Execution Flow")
    st.markdown("**(UI → AGENTS → BI OUTPUT)**")

    st.markdown("""
    <div style='display: flex; flex-direction: column; gap: 10px;'>
        <div style='background: rgba(40, 116, 240, 0.1); border-left: 4px solid #2874f0; padding: 15px; border-radius: 8px;'>
            <strong style='color: #2874f0;'>STEP 1: USER</strong><br>
            <span style='color: #e2e8f0; font-size: 0.9rem;'>Enters question in Streamlit UI (e.g., "Show revenue trends")</span>
        </div>
        <div style='text-align: center; color: #666;'>▼</div>
        <div style='background: rgba(155, 89, 182, 0.1); border-left: 4px solid #9b59b6; padding: 15px; border-radius: 8px;'>
            <strong style='color: #9b59b6;'>STEP 2: API & ORCHESTRATOR</strong><br>
            <span style='color: #e2e8f0; font-size: 0.9rem;'>FastAPI identifies tenant/user -> LangGraph takes control of the agent swarm.</span>
        </div>
        <div style='text-align: center; color: #666;'>▼</div>
        <div style='background: rgba(243, 156, 18, 0.1); border-left: 4px solid #f39c12; padding: 15px; border-radius: 8px;'>
            <strong style='color: #f39c12;'>STEP 3: AGENT PIPELINE</strong><br>
            <span style='color: #e2e8f0; font-size: 0.9rem;'>Metadata → RAG → SQL Generator → Impact Analysis → Execution → BI Logic</span>
        </div>
        <div style='text-align: center; color: #666;'>▼</div>
        <div style='background: rgba(46, 204, 113, 0.1); border-left: 4px solid #2ecc71; padding: 15px; border-radius: 8px;'>
            <strong style='color: #2ecc71;'>STEP 4: RESPONSE & MEMORY</strong><br>
            <span style='color: #e2e8f0; font-size: 0.9rem;'>Delivers KPIs, Charts, SQL Explanation, and updates long-term memory (Mem0).</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    
    # 5. Core Technologies & MCP
    col_tech_1, col_tech_2, col_tech_3 = st.columns(3)
    
    with col_tech_1:
        st.markdown("""
        <div style='background: #1e1e2d; padding: 20px; border-radius: 12px; border: 1px solid #323248; height: 100%;'>
            <h3 style='color: #00d4ff;'>🧠 LangGraph</h3>
            <p style='color: #7f8fa4; font-size: 0.9rem;'>The 'Brain Controller'</p>
            <ul style='color: #cfd8dc; font-size: 0.9rem; margin-bottom: 0;'>
                <li>Deterministic execution</li>
                <li>Debuggable agent flows</li>
                <li>Shared state management</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
    with col_tech_2:
        st.markdown("""
        <div style='background: #1e1e2d; padding: 20px; border-radius: 12px; border: 1px solid #323248; height: 100%;'>
            <h3 style='color: #ff007a;'>🧠 Mem0 Memory</h3>
            <p style='color: #7f8fa4; font-size: 0.9rem;'>The 'Long-Term Storage'</p>
            <ul style='color: #cfd8dc; font-size: 0.9rem; margin-bottom: 0;'>
                <li>Remembers user prefs</li>
                <li>Cross-session memory</li>
                <li>Personalized BI context</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col_tech_3:
        st.markdown("""
        <div style='background: #1e1e2d; padding: 20px; border-radius: 12px; border: 1px solid #323248; height: 100%;'>
            <h3 style='color: #f39c12;'>🧩 MCP Tools</h3>
            <p style='color: #7f8fa4; font-size: 0.9rem;'>The 'Agent Hands'</p>
            <ul style='color: #cfd8dc; font-size: 0.9rem; margin-bottom: 0;'>
                <li>folder: <code>mcp/</code></li>
                <li>Agents use tools, not just text</li>
                <li>SQL execution & Billing triggers</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    
    # 6. Enterprise Features (Vertical Layout)
    st.subheader("🏢 Enterprise Grade Capability")
    
    # Card 1: Monetization
    st.markdown("""
    <div style='background: rgba(40, 116, 240, 0.1); border-left: 5px solid #2874f0; padding: 20px; border-radius: 10px; margin-bottom: 20px;'>
        <h3 style='color: #2874f0; margin-top: 0;'>💰 Monetization & Billing</h3>
        <ul style='color: #e2e8f0; font-size: 0.95rem; line-height: 1.6;'>
            <li><b>Usage-Based Billing</b>: Tracks queries executed & LLM token usage.</li>
            <li><b>Subscription Management</b>: Supports Free, Pro & Enterprise tiers.</li>
            <li><b>Stripe Integration</b>: Ready-to-use module in <code>billing/metering.py</code>.</li>
            <li><b>Scheduled Reports</b>: Monetize automated insights delivery.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    # Card 2: Governance
    st.markdown("""
    <div style='background: rgba(46, 204, 113, 0.1); border-left: 5px solid #2ecc71; padding: 20px; border-radius: 10px; margin-bottom: 20px;'>
        <h3 style='color: #2ecc71; margin-top: 0;'>🔒 Governance, Security & Lineage</h3>
        <ul style='color: #e2e8f0; font-size: 0.95rem; line-height: 1.6;'>
            <li><b>RBAC (Role-Based Access Control)</b>: Granular permissions for Admins, Editors, Viewers.</li>
            <li><b>PII Protection</b>: Automatic masking of sensitive columns (e.g., SSN, Email) before SQL generation.</li>
            <li><b>Data Lineage</b>: End-to-end tracking: <i>Question → SQL → Tables → Dashboard</i>.</li>
            <li><b>Audit Trails</b>: Full compliance logging available in the <code>governance/</code> module.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    # Card 3: Deployment
    st.markdown("""
    <div style='background: rgba(155, 89, 182, 0.1); border-left: 5px solid #9b59b6; padding: 20px; border-radius: 10px; margin-bottom: 20px;'>
        <h3 style='color: #9b59b6; margin-top: 0;'>⚙️ Flexible Deployment Models</h3>
        <div style='display: flex; gap: 20px; flex-wrap: wrap; margin-top: 15px;'>
            <div style='flex: 1; background: rgba(0,0,0,0.2); padding: 15px; border-radius: 8px;'>
                <strong style='color: #fff;'>☁️ SaaS Mode</strong>
                <ul style='color: #bdc3c7; font-size: 0.9rem; padding-left: 20px; margin-bottom: 0;'>
                    <li>Multi-tenant Architecture</li>
                    <li>Cloud LLMs (OpenAI/Groq)</li>
                    <li>Central Billing System</li>
                </ul>
            </div>
            <div style='flex: 1; background: rgba(0,0,0,0.2); padding: 15px; border-radius: 8px;'>
                <strong style='color: #fff;'>🏢 On-Prem Mode</strong>
                <ul style='color: #bdc3c7; font-size: 0.9rem; padding-left: 20px; margin-bottom: 0;'>
                    <li>Single Tenant / Air-gapped</li>
                    <li>Local LLMs (Llama 3 via Ollama)</li>
                    <li>Docker/K8s Container Ready</li>
                </ul>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


    st.markdown("---")
    
    # 7. Deep Dive Expander (Covering specific File <-> Feature mappings from the Doc)
    with st.expander("📄 View Detailed Execution & File Structure (Project Explanation)", expanded=False):
        st.markdown("""
        ### 📂 Project Code Structure & Feature Mapping
        
        **1. USER INTERFACE**
        - `ui/dashboard.py`: Main Streamlit Dashboard (KPIs, Charts, Tables).
        
        **2. API LAYER**
        - `app/main.py`: FastAPI Gateway, Tenant Context, LangGraph Trigger.
        
        **3. INTELLIGENT AGENTS**
        - `agents/metadata_agent.py`: Schema awareness, prevention of hallucinations.
        - `agents/rag_agent.py`: Retrieval of certified reports.
        - `agents/sql_agent.py`: Natural Language to SQL conversion.
        - `agents/impact_agent.py`: **Cost Control & Safety** (Blocks 'SELECT *').
        - `agents/execute_agent.py`: Tenant-isolated secure execution.
        - `agents/bi_agent.py`: Insight generation & formatting.
        
        **4. ORCHESTRATION**
        - `app/langgraph/state.py`: Shared state definition.
        - `app/langgraph/graph.py`: Deterministic flow control.
        
        **5. PERSISTENCE**
        - `memory/mem0_client.py`: Long-term user memory storage.
        
        **6. ENTERPRISE MODULES**
        - `billing/metering.py`: Usage tracking (Stripe/Internal).
        - `governance/`: Audit logs, PII masking, Compliance.
        
        **7. MCP TOOLS**
        - `mcp/`: Tool definitions enabling agents to perform actions (Run SQL, Calculator).
        """)
    
    st.markdown("---")

    # 8. Final Summary
    st.markdown("""
    <div style='background: linear-gradient(to right, #243B55, #141E30); 
                padding: 25px; border-radius: 15px; text-align: center; border: 2px solid #00d4ff;'>
        <h3 style='color: #fff; margin-bottom: 10px;'>🚀 FINAL SUMMARY</h3>
        <p style='color: #a0aec0; margin-bottom: 20px;'>
            This is not just a demo. It is a <b>Startup-ready AI product</b>.
        </p>
        <div style='display: flex; justify-content: center; gap: 20px; flex-wrap: wrap;'>
            <span style='background: #00d4ff; color: #000; padding: 5px 15px; border-radius: 5px; font-weight: bold;'>✅ Agentic AI with Memory</span>
            <span style='background: #00d4ff; color: #000; padding: 5px 15px; border-radius: 5px; font-weight: bold;'>✅ Enterprise-grade BI</span>
            <span style='background: #00d4ff; color: #000; padding: 5px 15px; border-radius: 5px; font-weight: bold;'>✅ Monetization & Compliance</span>
            <span style='background: #00d4ff; color: #000; padding: 5px 15px; border-radius: 5px; font-weight: bold;'>✅ SaaS or On-Prem</span>
        </div>
        <h2 style='color: #00d4ff; margin-top: 25px;'>AGENTIC BI SAAS = FUTURE OF BUSINESS INTELLIGENCE</h2>
    </div>
    """, unsafe_allow_html=True)

# --- TAB 3: TECH STACK ---
# --- TAB 3: TECH STACK ---
with tab3:
    # 1. Premium Header
    st.markdown("""
    <div style='background: linear-gradient(135deg, rgba(40, 116, 240, 0.1) 0%, rgba(155, 89, 182, 0.1) 100%); 
                padding: 30px; border-radius: 15px; border-bottom: 4px solid #00d4ff; margin-bottom: 25px;'>
        <h2 style='color: #00d4ff; margin: 0 0 10px 0; font-weight: 800;'>🛠️ The Complete Technology Stack</h2>
        <p style='color: #e2e8f0; font-size: 1.1rem; line-height: 1.6;'>
            A robust, enterprise-grade stack built for scale, security, and intelligence. 
            <b>14 Layers</b> of modern engineering.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # --- DEFINERS for Reusability ---
    def tech_badge(label, color="#262730"):
        return f"<span style='display:inline-block; padding:4px 12px; margin:2px; border-radius:20px; background-color:{color}; border:1px solid #4B4B4B; font-size:0.8em; color:white;'>{label}</span>"

    # --- SECTION A: OVERVIEW (Always Visible) ---
    st.markdown("### 🏢 High-Level Snapshot")
    st.markdown("A quick glance at the primary engines powering Agentic BI.")
    
    ov_col1, ov_col2, ov_col3 = st.columns(3)
    with ov_col1:
        with st.container(border=True):
            st.markdown("#### 🎨 Frontend")
            st.markdown("Streamlit • Plotly")
            st.caption("Status: Active 🟢")
    with ov_col2:
        with st.container(border=True):
            st.markdown("#### 🧠 AI Brain")
            st.markdown("LangGraph • GPT-4o")
            st.caption("Status: Active 🟢")
    with ov_col3:
        with st.container(border=True):
            st.markdown("#### 💾 Memory")
            st.markdown("Mem0 • SQLite")
            st.caption("Status: Active 🟢")
            
    st.markdown("---")
    st.subheader("📚 Detailed Breakdown (Click to Expand)")

    # --- SECTION B: Vertical Interactive Layers ---
    
    # 1. FRONTEND
    with st.expander("🖥️ 1. Frontend & Visualization Layer", expanded=True):
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            st.markdown("#### 1. UI Framework")
            st.markdown(tech_badge("Streamlit") + tech_badge("Python"), unsafe_allow_html=True)
            st.markdown("""
            - **Interactive BI dashboards**
            - KPI cards, tables, charts
            - Dark mode support
            - Rapid UI development
            """)
        with col_f2:
            st.markdown("#### 1.1 Visualization")
            st.markdown(tech_badge("Plotly") + tech_badge("JSON"), unsafe_allow_html=True)
            st.markdown("""
            - **Dynamic charts** (bar, line, time-series)
            - BI-grade visualizations
            """)

    # 2. AI & BACKEND
    with st.expander("🧠 2. AI, Backend & Orchestration", expanded=False):
        c_ai1, c_ai2, c_ai3 = st.columns(3)
        with c_ai1:
            st.markdown("#### 2. Backend / API")
            st.markdown(tech_badge("FastAPI") + tech_badge("Uvicorn"), unsafe_allow_html=True)
            st.markdown("""
            - **Python 3.10+** (Core language)
            - **FastAPI**: REST API backend
              - High performance and async-ready
              - API documentation via Swagger
            - **Uvicorn**: ASGI server for FastAPI
            """)
            
            st.markdown("#### 5. Long-Term Memory")
            st.markdown(tech_badge("Mem0") + tech_badge("Personalization"), unsafe_allow_html=True)
            st.markdown("""
            - **Persistent AI memory layer**
            - Cross-session memory
            - User & tenant-level memory
            - Preference and context retention
            """)
            
        with c_ai2:
            st.markdown("#### 3. Orchestration")
            st.markdown(tech_badge("LangGraph") + tech_badge("LangChain"), unsafe_allow_html=True)
            st.markdown("""
            - **LangGraph**:
              - Agent orchestration framework
              - Deterministic state-based workflows
              - Enterprise-safe agent execution
            - **LangChain**:
              - LLM abstraction
              - Prompt management
              - Tool integration
            """)
            
            st.markdown("#### 7. RAG System")
            st.markdown(tech_badge("ChromaDB") + tech_badge("FAISS"), unsafe_allow_html=True)
            st.markdown("""
            - **Vector Databases**: FAISS, ChromaDB
            - **Embeddings**: 
              - OpenAI Embeddings
              - SentenceTransformers
            """)
            
        with c_ai3:
            st.markdown("#### 4. LLMs")
            st.markdown(tech_badge("GPT-4o") + tech_badge("Llama 3"), unsafe_allow_html=True)
            st.markdown("""
            - **OpenAI GPT-4o / GPT-4o-mini**:
              - SQL generation
              - BI reasoning
              - Natural language understanding
            - **Local LLMs (Optional)**:
              - LLaMA 3
              - Mixtral
              - Phi-3
            """)

    # 3. DATA & GOVERNANCE
    with st.expander("🛡️ 3. Data, Governance & Security", expanded=False):
        c_dat1, c_dat2 = st.columns(2)
        with c_dat1:
            st.markdown("#### 6. Database Layer")
            st.markdown(tech_badge("PostgreSQL") + tech_badge("SQLAlchemy"), unsafe_allow_html=True)
            st.markdown("""
            - **SQL Databases**:
              - PostgreSQL
              - MySQL
              - SQLite (development)
            - **SQLAlchemy**:
              - Database ORM & connection management
              - Secure query execution
            """)
            
            st.markdown("#### 9. Billing")
            st.markdown(tech_badge("Stripe API") + tech_badge("Metering"), unsafe_allow_html=True)
            st.markdown("""
            - **Usage-based Metering** (Custom)
            - **Stripe API (Optional)**:
              - Subscription billing
              - Usage tracking
            """)
            
        with c_dat2:
            st.markdown("#### 8. Governance & Security")
            st.markdown(tech_badge("RBAC") + tech_badge("PII Masking"), unsafe_allow_html=True)
            st.markdown("""
            - Role-Based Access Control (RBAC)
            - Data Lineage Tracking
            - Query Impact Analysis
            - PII & Sensitive Column Protection
            """)

    # 4. OPS & INFRA
    with st.expander("☁️ 4. Ops, Deployment & Infrastructure", expanded=False):
        c_ops1, c_ops2, c_ops3 = st.columns(3)
        with c_ops1:
            st.markdown("#### 10. MCP Tools")
            st.markdown("""
            - **MCP Tool Registry**:
              - SQL execution tools
              - Dashboard generation tools
              - Billing & governance tools
            """)
            
            st.markdown("#### 11. Automation")
            st.markdown("""
            - **APScheduler**:
              - Scheduled BI reports
              - Automated insights delivery
            """)
            
        with c_ops2:
            st.markdown("#### 12. Deployment")
            st.markdown(tech_badge("Docker") + tech_badge("K8s"), unsafe_allow_html=True)
            st.markdown("""
            - **Docker**: Containerized deployment
            - **Docker Compose**: Multi-service orchestration
            - **Kubernetes (Optional)**: Scalable production deployment
            """)
            
            st.markdown("#### 14. Configuration")
            st.markdown("""
            - **python-dotenv**: Environment variable management
            """)
            
        with c_ops3:
            st.markdown("#### 13. On-Prem Support")
            st.markdown(tech_badge("Local LLM"), unsafe_allow_html=True)
            st.markdown("""
            - Local LLM inference
            - Air-gapped deployment
            - No external API dependency
            """)

    st.markdown("---")
    # Final Summary Footer
    st.info("""
    **✅ FINAL ARCHITECTURE SUMMARY**
    
    The combination of **LangGraph**, **Mem0**, and **MCP** creates a system that is:
    1.  **Agentic**: It acts, doesn't just talk.
    2.  **Stateful**: It remembers you.
    3.  **Secure**: It respects enterprise governance.
    """)

# --- TAB 4: HLD & LLD ---
with tab4:
    # 1. Premium Header
    st.markdown("""
    <div style='background: linear-gradient(135deg, rgba(46, 204, 113, 0.1) 0%, rgba(26, 188, 156, 0.1) 100%); 
                padding: 30px; border-radius: 15px; border-bottom: 4px solid #2ecc71; margin-bottom: 25px;'>
        <h2 style='color: #2ecc71; margin: 0 0 10px 0; font-weight: 800;'>📐 Design & Architecture Specification</h2>
        <p style='color: #e2e8f0; font-size: 1.1rem; line-height: 1.6;'>
            Comprehensive documentation covering <b>Software Requirements (SRS)</b>, 
            <b>High-Level Design (HLD)</b>, and <b>Low-Level Design (LLD)</b>.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Helper for styled badges (Local scope to avoid errors)
    def design_badge(label, color="#1e272e"):
        return f"<span style='display:inline-block; padding:4px 10px; margin:2px; border-radius:15px; background-color:{color}; border:1px solid #4B4B4B; font-size:0.8em; color:white;'>{label}</span>"

    # 2. Vertical Expanders for Document Sections (Vertical Layout)
    
    # --- SECTION A: SRS ---
    with st.expander("📝 1. Software Requirements Specification (SRS)", expanded=True):
        st.markdown("### 1. Software Requirements Specification")
        
        c_srs1, c_srs2 = st.columns(2)
        with c_srs1:
            with st.container(border=True):
                st.markdown("#### 1.1 Purpose")
                st.info("To define the software requirements, architecture, and detailed design of the Agentic BI SaaS platform. This system enables users to query business data using natural language and receive governed, explainable BI insights.")
        with c_srs2:
            with st.container(border=True):
                st.markdown("#### 1.2 Scope")
                st.markdown("""
                - Natural language BI querying
                - AI agent-based orchestration
                - Long-term AI memory
                - Governance & data lineage
                - Usage-based monetization
                - SaaS and On-Prem deployment support
                """)

        st.markdown("#### 1.3 Functional Requirements (FR)")
        fr_data = [
            {"ID": "FR-01", "Requirement": "System shall accept natural language business questions."},
            {"ID": "FR-02", "Requirement": "System shall generate SQL queries using AI agents."},
            {"ID": "FR-03", "Requirement": "System shall execute SQL securely."},
            {"ID": "FR-04", "Requirement": "System shall generate KPIs and visualizations."},
            {"ID": "FR-05", "Requirement": "System shall store long-term memory using AI memory."},
            {"ID": "FR-06", "Requirement": "System shall support multi-tenant SaaS architecture."},
            {"ID": "FR-07", "Requirement": "System shall support on-prem deployment."},
            {"ID": "FR-08", "Requirement": "System shall enforce governance and data lineage."},
            {"ID": "FR-09", "Requirement": "System shall track usage for billing."}
        ]
        st.table(fr_data)
        
        c_nfr1, c_nfr2 = st.columns(2)
        with c_nfr1:
            st.markdown("#### 1.4 User Classes")
            st.markdown("- Business User\n- Analyst\n- Manager\n- Admin\n- System Administrator")
        with c_nfr2:
            st.markdown("#### 1.6 Non-Functional Requirements")
            st.markdown("""
            - **Performance**: Query response < 5 seconds (average)
            - **Security**: RBAC, tenant isolation
            - **Scalability**: Support multiple tenants
            - **Reliability**: Fault-tolerant agent execution
            - **Maintainability**: Modular agent-based design
            """)

    # --- SECTION B: HLD ---
    with st.expander("🏗️ 2. High Level Design (HLD)", expanded=False):
        st.markdown("### 2. High Level Design")
        
        with st.container(border=True):
            st.markdown("#### 2.1 Architectural Overview")
            st.code("User → Streamlit UI → FastAPI Backend → LangGraph Orchestrator → Agentic AI Pipeline → BI Output", language="text")
        
        c_hld1, c_hld2 = st.columns(2)
        with c_hld1:
            with st.container(border=True):
                st.markdown("#### 2.2 System Components")
                st.markdown("""
                - **Presentation Layer**: Streamlit
                - **API Layer**: FastAPI
                - **Orchestration**: LangGraph
                - **Agent Layer**: Metadata, RAG, SQL, Impact, Execute, BI
                - **Memory Layer**: mem0
                - **Governance & Billing**: Custom Modules
                - **Data Layer**: Databases & Reports
                """)
        with c_hld2:
            with st.container(border=True):
                st.markdown("#### 2.3 Deployment Architecture")
                st.markdown(design_badge("SaaS Mode") + " Multi-tenant, Cloud LLMs", unsafe_allow_html=True)
                st.markdown(design_badge("On-Prem Mode") + " Single-tenant, Local LLMs", unsafe_allow_html=True)
                st.divider()
                st.markdown("#### 2.4 Data Flow")
                st.markdown("**User Input** → Agent Processing → Secure Query Execution → BI Output → **Memory Storage**")

    # --- SECTION C: LLD ---
    with st.expander("⚙️ 3. Low Level Design (LLD)", expanded=False):
        st.markdown("### 3. Low Level Design")
        
        st.markdown("#### 3.1 Presentation & API Layers")
        c_lld1, c_lld2 = st.columns(2)
        with c_lld1:
            st.markdown("**3.1 Presentation Layer**")
            st.markdown("- Streamlit Dashboard\n- KPI cards, tables, charts\n- Dark mode support")
        with c_lld2:
            st.markdown("**3.2 API Layer**")
            st.markdown("- FastAPI REST endpoints\n- JSON request/response\n- Usage metering integration")
        
        st.divider()
        st.markdown("#### 3.3 & 3.4 Orchestration & Agents (Detailed)")
        st.markdown("**3.3 Orchestration Layer**: LangGraph state management, Deterministic agent flow, Error handling.")
        
        # Agent Grid
        ag1, ag2, ag3 = st.columns(3)
        with ag1:
            st.markdown(design_badge("3.4.1 Metadata Agent"), unsafe_allow_html=True)
            st.markdown("- Reads schema catalog\n- Reads preferences (mem0)\n- Outputs relevant tables")
            
            st.markdown(design_badge("3.4.4 Impact Agent"), unsafe_allow_html=True)
            st.markdown("- Analyzes query cost\n- Blocks unsafe SQL")
            
        with ag2:
            st.markdown(design_badge("3.4.2 RAG Agent"), unsafe_allow_html=True)
            st.markdown("- Retrieves certified docs\n- Adds trusted context")
            
            st.markdown(design_badge("3.4.5 Execute Agent"), unsafe_allow_html=True)
            st.markdown("- Executes SQL securely\n- Returns result set")
            
        with ag3:
            st.markdown(design_badge("3.4.3 SQL Agent"), unsafe_allow_html=True)
            st.markdown("- Converts Natural Language to SQL\n- Applies schema constraints")
            
            st.markdown(design_badge("3.4.6 BI Agent"), unsafe_allow_html=True)
            st.markdown("- Computes KPIs & Explanations\n- Writes memory to mem0")

        st.divider()
        st.markdown("#### 3.5, 3.6, 3.7 Memory & Governance")
        c_mg1, c_mg2, c_mg3 = st.columns(3)
        with c_mg1:
            st.markdown("**3.5 Memory Layer (mem0)**")
            st.markdown("- Persistent, cross-session AI memory\n- User and tenant scoped\n- Stores preferences & query patterns")
        with c_mg2:
            st.markdown("**3.6 Governance & Lineage**")
            st.markdown("- Tracks SQL, tables, columns\n- Enforces PII protection\n- Maintains audit logs")
        with c_mg3:
            st.markdown("**3.7 Billing Module**")
            st.markdown("- Tracks usage per tenant\n- Enables subscription & usage-based billing")

    st.markdown("---")
    # Conclusion Footer
    st.success("""
    **✅ CONCLUSION**
    
    The Agentic BI SaaS platform is a scalable, secure, and enterprise-ready AI-powered BI system. 
    The architecture supports extensibility, governance, and both SaaS and on-prem deployment models.
    """)

# --- TAB 5: ARCHITECTURE ---
with tab5:
    # 1. Premium Header
    st.markdown("""
    <div style='background: linear-gradient(135deg, rgba(243, 156, 18, 0.1) 0%, rgba(211, 84, 0, 0.1) 100%); 
                padding: 30px; border-radius: 15px; border-bottom: 4px solid #f39c12; margin-bottom: 25px;'>
        <h2 style='color: #f39c12; margin: 0 0 10px 0; font-weight: 800;'>🏗️ System Architecture & Blueprint</h2>
        <p style='color: #e2e8f0; font-size: 1.1rem; line-height: 1.6;'>
            A production-grade, <b>agentic AI architecture</b> supporting both SaaS and Air-Gapped deployments.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Helper for badges
    def arch_badge(label, color="#2c3e50"):
        return f"<span style='display:inline-block; padding:4px 10px; margin:2px; border-radius:15px; background-color:{color}; border:1px solid #4B4B4B; font-size:0.8em; color:white;'>{label}</span>"

    # 2. Architecture Diagram (Image)
    st.subheader("🖼️ Architectural Blueprint")
    
    # Robust Image Finder for Cloud/Local compatibility
    img_filename = "agentic_bi_architecture.jpeg"
    possible_paths = [
        img_filename, 
        os.path.join("agentic-bi-saas", img_filename),
        os.path.join(os.getcwd(), img_filename),
    ]
    
    img_found = None
    for p in possible_paths:
        if os.path.exists(p):
            img_found = p
            break
            
    if img_found:
        st.image(img_found, caption="Agentic BI SaaS - Official Architecture Diagram", use_container_width=True)
    else:
        st.warning(f"⚠️ Architecture Diagram ({img_filename}) not found in path. Ensure it is uploaded to the repository root.")

    # 3. Interactive Graphviz Chart
    with st.expander("🔍 Interactive Service Map (Live Diagram)", expanded=True):
        st.graphviz_chart("""
        digraph G {
            rankdir=LR;
            node [shape=box, style=filled, fillcolor="#faebcc", fontname="Sans-Serif", color="#8a6d3b"];
            edge [color="#8a6d3b"];
            
            User [shape=ellipse, fillcolor="#7267EF", fontcolor=white];
            Dashboard [label="Streamlit UI", fillcolor="#FF4B4B", fontcolor=white];
            
            subgraph cluster_backend {
                style=dashed; color="#8a6d3b";
                label = "Backend Service";
                API [label="FastAPI", fillcolor="#009688", fontcolor=white];
                Orchestrator [label="LangGraph", fillcolor="#ffbd45"];
            }
            
            subgraph cluster_data {
                style=filled;
                color="#fcf8e3";
                label = "Persistence";
                Database [label="SQLite DB", shape=cylinder, fillcolor="#ffffff"];
                Memory [label="Mem0 Store", shape=cylinder, fillcolor="#ffffff"];
            }
            
            User -> Dashboard [label="Queries"];
            Dashboard -> API [label="HTTP POST"];
            API -> Orchestrator [label="Invoke Graph"];
            Orchestrator -> Database [label="SQL Execution"];
            Orchestrator -> Memory [label="RAG Context"];
            Database -> Orchestrator [label="Result Set"];
            Orchestrator -> API [label="Synthesis"];
            API -> Dashboard [label="JSON Response"];
        }
        """)

    # 4. Detailed Architecture Content (Vertical Layout)
    
    # --- SECTION A: HLD ---
    with st.expander("1. High-Level Flow & Design (HLD)", expanded=False):
        c_hld1, c_hld2 = st.columns(2)
        with c_hld1:
            st.markdown("#### 1. System Flow")
            st.code("""
User (Browser)
  ↓
Streamlit BI Dashboard
  ↓
FastAPI Backend (API Gateway)
  ↓
LangGraph Orchestrator
  ↓
Agentic AI Pipeline (Metadata, RAG, SQL, Impact, Execute, BI)
  ↓
BI Output (KPIs, Tables, Charts)
  ↓
Memory Storage (mem0) + Lineage Logs
            """, language="text")
        
        with c_hld2:
            st.markdown("#### 2.2 System Components")
            st.markdown(f"""
            - **Presentation Layer**: Streamlit
            - **API Layer**: FastAPI (Gateway)
            - **Orchestration**: LangGraph (Controller)
            - **Agent Layer**: {arch_badge("Metadata")} {arch_badge("RAG")} {arch_badge("SQL")} {arch_badge("Impact")} {arch_badge("Execute")} {arch_badge("BI")}
            - **Shared Services**: {arch_badge("mem0 Memory", "#8e44ad")} {arch_badge("Billing", "#2ecc71")} {arch_badge("Governance", "#e74c3c")}
            - **Data Layer**: Databases & Reports
            """, unsafe_allow_html=True)
            
            st.markdown("#### 🔑 HLD Key Points")
            st.success("""
            - UI is separated from backend
            - Agents are centrally orchestrated
            - Memory, billing, governance are shared services
            - Supports SaaS & On-Prem deployments
            """)

    # --- SECTION B: LLD (Components) ---
    with st.expander("2. Component Details (LLD)", expanded=False):
        c_lld1, c_lld2 = st.columns(2)
        
        with c_lld1:
            st.markdown("#### 3.1 UI Layer (Streamlit)")
            st.markdown("- **Input**: Natural language question\n- **Output**: KPI cards, Tables, Charts\n- Maintains session context")
            
            st.markdown("#### 3.2 API Layer (FastAPI)")
            st.markdown("- Validates tenant & user\n- Records usage (billing)\n- Routes to LangGraph")
            
        with c_lld2:
            st.markdown("#### 3.3 LangGraph Orchestration")
            st.markdown("**Shared State (BIState)**: question, metadata, sql, result, response")
            st.markdown("**Responsibilities**: Controls execution order, Prevents unsafe execution, Audit & replay")
            st.markdown("**🔄 Agent Execution Order**:")
            st.code("""
1. Metadata Agent
2. RAG Agent
3. SQL Agent
4. Impact Agent
5. Execute Agent
6. BI Agent
            """, language="text")

        st.divider()
        st.markdown("#### 3.4 Agent Details (The Swarm)")
        
        # Agent Grid
        ag1, ag2, ag3 = st.columns(3)
        with ag1:
            st.info("**Metadata Agent**\n\n- Reads schema catalog\n- Reads preferences from mem0\n- Outputs relevant tables")
            st.info("**Impact Agent**\n\n- Analyzes SQL cost & risk\n- Blocks 'SELECT *'\n- Prevents full table scans")
        with ag2:
            st.info("**RAG Agent**\n\n- Queries vector DB\n- Retrieves certified docs\n- Adds trusted context")
            st.info("**Execute Agent**\n\n- Executes SQL securely\n- Tenant-isolated DB access\n- Returns result set")
        with ag3:
            st.info("**SQL Agent**\n\n- Converts text to SQL\n- Uses LLM or local model\n- Follows schema constraints")
            st.info("**BI Agent**\n\n- Calculates KPIs\n- Generates explanations\n- Writes memory to mem0")

    # --- SECTION C: Shared Services ---
    with st.expander("3. Shared Services, Governance & Deployment", expanded=False):
        c_srv1, c_srv2, c_srv3 = st.columns(3)
        
        with c_srv1:
            with st.container(border=True):
                st.markdown("#### 3.5 Memory (mem0)")
                st.markdown("- Persistent AI memory\n- Stores user preferences\n- KPI definitions & Query patterns\n- Enables follow-up questions")
        
        with c_srv2:
            with st.container(border=True):
                st.markdown("#### 3.6 Governance")
                st.markdown("- RBAC & PII protection\n- Captures SQL, tables, columns\n- Enforces certified data usage")
        
        with c_srv3:
            with st.container(border=True):
                st.markdown("#### 3.7 Billing")
                st.markdown("- Tracks usage per tenant\n- Metrics: Queries, Reports, LLM usage\n- Enables SaaS pricing")

        st.divider()
        st.markdown("#### 4. Deployment Models")
        d_col1, d_col2 = st.columns(2)
        with d_col1:
            st.markdown(f"### {arch_badge('☁️ SaaS Mode', '#3498db')}", unsafe_allow_html=True)
            st.markdown("- Multi-tenant\n- Cloud LLMs\n- Central billing\n- Subscription pricing")
        with d_col2:
            st.markdown(f"### {arch_badge('🏢 On-Prem Mode', '#34495e')}", unsafe_allow_html=True)
            st.markdown("- Single tenant\n- Local LLMs (Air-gapped)\n- No external API calls\n- Air-gapped security")

    st.markdown("---")
    st.success("""
    **✅ FINAL ARCHITECTURE SUMMARY**
    
    This production-grade architecture supports **Agentic workflows**, **Enterprise BI requirements**, 
    and **Secure, Scalable Deployment**.
    """)

# --- TAB 6: SYSTEM LOGS ---
# --- TAB 6: SYSTEM LOGS ---
with tab6:
    # 1. Premium Header
    st.markdown("""
    <div style='background: linear-gradient(135deg, rgba(52, 152, 219, 0.1) 0%, rgba(41, 128, 185, 0.1) 100%); 
                padding: 20px; border-radius: 15px; border-bottom: 4px solid #3498db; margin-bottom: 25px;'>
        <h2 style='color: #3498db; margin: 0 0 10px 0; font-weight: 800;'>📋 System Diagnostic & Event Logs</h2>
        <p style='color: #e2e8f0; font-size: 1.0rem; line-height: 1.5;'>
            Real-time monitoring of <b>Agent Orchestration</b>, <b>SQL Generation</b>, and <b>System Events</b>.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # helper for IST time
    def get_ist_time():
        # Assuming server is UTC or Local, we strictly format to what user asked
        # For this demo, we assume Local is IST or we add offset if needed.
        # Simplest consistent way:
        now = datetime.now()
        # If we wanted strict UTC+5:30: datetime.utcnow() + timedelta(hours=5, minutes=30)
        return now.strftime("%Y-%m-%d %H:%M:%S IST")

    # Session State Init for Start Time
    if "session_start_time" not in st.session_state:
        st.session_state.session_start_time = get_ist_time()
        st.session_state.session_user_id = f"Guest_User_{random.randint(1000, 9999)}"

    # 1.1 Session Login Details (New Requirement)
    with st.container(border=True):
        st.markdown("### 🔑 Session Login Details")
        c_sess1, c_sess2, c_sess3 = st.columns(3)
        with c_sess1:
            st.markdown(f"**User Identity**\n\n`{st.session_state.session_user_id}`")
        with c_sess2:
            st.markdown(f"**Connection Time**\n\n`{st.session_state.session_start_time}`")
        with c_sess3:
            st.markdown("**Status**\n\n<span style='color:#2ecc71'>● Active - Securely Connected</span>", unsafe_allow_html=True)

    st.markdown("---")

    logs = st.session_state.get('system_logs', [])
    
    # Inject initial connection logs if empty (Simulation of Boot Sequence)
    if not logs:
        boot_sequence = [
            ("System", "Kernel Initializing...", "INFO"),
            ("Security", "User Authentication Successful. Tenant: Demo_Corp", "SUCCESS"),
            ("Module Load", "LangGraph Orchestrator [OK]", "SUCCESS"),
            ("Module Load", "Tavily Search API [OK]", "SUCCESS"),
            ("Module Load", "Groq Inference Engine [OK]", "SUCCESS"),
            ("Agent Swarm", "6 Agents Registered (Metadata, RAG, SQL, Impact, Execute, BI)", "INFO"),
            ("System", f"Session initialized for {st.session_state.session_user_id}. Waiting for interactions...", "INFO")
        ]
        
        # Populate in newest-first order
        for idx, (evt, det, lvl) in enumerate(reversed(boot_sequence)):
             logs.append({
                "Timestamp": st.session_state.session_start_time, 
                "Event": evt,
                "Details": det,
                "Level": lvl 
            })

    # 2. Metrics & Parsing
    total_events = len(logs)
    unique_agents = len(set([l['Event'] for l in logs])) if logs else 0
    error_count = sum(1 for l in logs if 'error' in str(l.get('Details', '')).lower() or 'fail' in str(l.get('Details', '')).lower())
    
    # Summary Metrics (Custom HTML Cards)
    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown(f"""
        <div style='background: rgba(46, 204, 113, 0.1); padding: 15px; border-radius: 10px; border-left: 5px solid #2ecc71; text-align: center;'>
            <h4 style='color: #e8e8e8; margin: 0; font-size: 0.9rem;'>TOTAL EVENTS</h4>
            <p style='color: #2ecc71; font-size: 1.8rem; font-weight: bold; margin: 5px 0;'>{total_events}</p>
        </div>
        """, unsafe_allow_html=True)
    with m2:
        st.markdown(f"""
        <div style='background: rgba(52, 152, 219, 0.1); padding: 15px; border-radius: 10px; border-left: 5px solid #3498db; text-align: center;'>
            <h4 style='color: #e8e8e8; margin: 0; font-size: 0.9rem;'>ACTIVE AGENTS</h4>
            <p style='color: #3498db; font-size: 1.8rem; font-weight: bold; margin: 5px 0;'>{unique_agents}</p>
        </div>
        """, unsafe_allow_html=True)
    with m3:
        err_color = "#e74c3c" if error_count > 0 else "#95a5a6"
        st.markdown(f"""
        <div style='background: rgba(231, 76, 60, 0.1); padding: 15px; border-radius: 10px; border-left: 5px solid {err_color}; text-align: center;'>
            <h4 style='color: #e8e8e8; margin: 0; font-size: 0.9rem;'>ERRORS DETECTED</h4>
            <p style='color: {err_color}; font-size: 1.8rem; font-weight: bold; margin: 5px 0;'>{error_count}</p>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("---")

    # 3. Controls (Advanced Omni-Filters)
    f_col1, f_col2, f_col3 = st.columns([2, 1, 1])
    
    with f_col1:
        all_event_types = sorted(list(set([l['Event'] for l in logs]))) if logs else []
        selected_types = st.multiselect("🔍 Filter by Agent / Event Type:", all_event_types, default=all_event_types)
    
    with f_col2:
        severity_options = ["All Levels", "🔴 Errors Only", "🟢 Success Only", "🟡 Warnings Only", "🔵 Info Only"]
        selected_severity = st.selectbox("🚦 Severity Filter:", severity_options)
        
    with f_col3:
        search_query = st.text_input("📝 Keyword Search:", placeholder="e.g. 'SQL' or 'North'")

    # Download & Refresh Row (Aligned in one line)
    c_act1, c_act2, c_act3, c_spacer = st.columns([1.2, 1.2, 1.2, 4])
    with c_act1:
        if st.button("🔄 Refresh Logs", key="btn_refresh_logs", use_container_width=True):
            st.rerun()
            
    with c_act2:
        if logs:
            # TEXT EXPORT
            log_text = "AGENTIC BI SYSTEM LOGS\n======================\n"
            log_text += f"Export Time: {get_ist_time()}\n\n"
            for log in reversed(logs):
                log_text += f"[{log.get('Timestamp', '')}] {log.get('Event', '')}: {log.get('Details', '')}\n"
            
            st.download_button(
                label="📄 Export TXT",
                data=log_text,
                file_name=f"agentic_bi_logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain",
                use_container_width=True,
                key="btn_export_txt"
            )

    with c_act3:
        if logs:
            # CSV EXPORT
            df_logs = pd.DataFrame(logs)
            csv_logs = df_logs.to_csv(index=False).encode('utf-8')
            
            st.download_button(
                label="📊 Export CSV",
                data=csv_logs,
                file_name=f"agentic_bi_logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True,
                key="btn_export_csv"
            )
            
    with st.sidebar:
        st.markdown("---")
        if st.sidebar.button("🚨 Simulate System Error", help="Add a manual error log for testing"):
            log_event("Security", "MANUAL ALERT: Simulated system error triggered by admin.")

    # 4. Scrollable Log Feed
    st.markdown("### 📜 Real-time Event Feed")
    
    # Remove fixed height to show ALL logs as requested
    log_container = st.container(border=True)
    with log_container:
        if not logs:
            st.info("📭 No logs generated yet. Start interacting with the Demo tab to see the Agent Swarm in action!")
        else:
            # log_event inserts at 0, so the list 'logs' is already newest-first.
            # Showing newest at the top.
            for log in logs:
                # 1. Type Filter
                type_match = log['Event'] in selected_types
                
                # 2. Severity Filter
                details_lower = str(log.get('Details', '')).lower()
                is_err = any(x in details_lower for x in ['error', 'fail', 'exception'])
                is_succ = any(x in details_lower for x in ['success', 'complete', 'finished', 'generated'])
                is_warn = 'warning' in details_lower
                
                sev_match = True
                if selected_severity == "🔴 Errors Only": sev_match = is_err
                elif selected_severity == "🟢 Success Only": sev_match = is_succ
                elif selected_severity == "🟡 Warnings Only": sev_match = is_warn
                elif selected_severity == "🔵 Info Only": sev_match = not (is_err or is_succ or is_warn)
                
                # 3. Keyword Filter
                kw_match = True
                if search_query:
                    kw_match = search_query.lower() in details_lower or search_query.lower() in str(log['Event']).lower()
                
                # Combined Logic
                if type_match and sev_match and kw_match:
                    # Enforce IST Formatting if missing
                    raw_time = str(log.get('Timestamp', ''))
                    if "IST" not in raw_time:
                         timestamp = f"{raw_time} IST"
                    else:
                         timestamp = raw_time
                         
                    event = log.get('Event', 'Unknown')
                    details = log.get('Details', '')
                    
                    # Style Logic
                    if any(x in details.lower() for x in ['error', 'fail', 'exception']):
                        st.error(f"**[{timestamp}] {event}**: {details}", icon="🚨")
                    elif any(x in details.lower() for x in ['success', 'complete', 'finished', 'generated']):
                        st.success(f"**[{timestamp}] {event}**: {details}", icon="✅")
                    elif 'warning' in details.lower():
                        st.warning(f"**[{timestamp}] {event}**: {details}", icon="⚠️")
                    else:
                        st.info(f"**[{timestamp}] {event}**: {details}", icon="ℹ️")

# --- FOOTER ---
st.markdown("<hr style='border: 1px solid #e74c3c; background-color: #e74c3c; opacity: 1; margin: 30px 0;'>", unsafe_allow_html=True)
st.markdown("""
<div style='text-align: center; padding: 20px 20px 10px 20px; background: linear-gradient(135deg, rgba(46, 204, 113, 0.15) 0%, rgba(52, 152, 219, 0.15) 100%); border-radius: 10px; border-top: 2px solid #2ecc71;'>
    <p style='color: #2ecc71; font-weight: 600; font-size: 1.1rem; margin-bottom: 10px;'>🤖 Agentic BI SaaS Platform</p>
    <p style='color: #3498db; font-weight: 600; font-size: 1.1rem; margin-bottom: 15px;'>Built with ❤️ by Ratnesh Kumar Singh | Data Scientist (AI/ML Engineer 4+Years Exp)</p>
    <div style='background: rgba(0, 0, 0, 0.2); padding: 10px; border-radius: 8px; display: inline-block; margin-bottom: 10px;'>
        <span style='color: #bdc3c7; font-size: 0.9rem; margin-right: 10px; font-weight: 600;'>Tech Stack Used:</span>
        <span style='display: inline-block; padding: 4px 10px; margin: 2px; border-radius: 15px; background-color: #2c3e50; border: 1px solid #3498db; font-size: 0.8em; color: white;'>LangGraph 🦜🕸️</span>
        <span style='display: inline-block; padding: 4px 10px; margin: 2px; border-radius: 15px; background-color: #2c3e50; border: 1px solid #2ecc71; font-size: 0.8em; color: white;'>LangChain 🦜🔗</span>
        <span style='display: inline-block; padding: 4px 10px; margin: 2px; border-radius: 15px; background-color: #2c3e50; border: 1px solid #e67e22; font-size: 0.8em; color: white;'>Groq ⚡</span>
        <span style='display: inline-block; padding: 4px 10px; margin: 2px; border-radius: 15px; background-color: #2c3e50; border: 1px solid #009688; font-size: 0.8em; color: white;'>FastAPI 🚀</span>
        <span style='display: inline-block; padding: 4px 10px; margin: 2px; border-radius: 15px; background-color: #2c3e50; border: 1px solid #E056FD; font-size: 0.8em; color: white;'>MCP 🔌</span>
        <span style='display: inline-block; padding: 4px 10px; margin: 2px; border-radius: 15px; background-color: #2c3e50; border: 1px solid #F0932B; font-size: 0.8em; color: white;'>Mem0 🧠</span>
        <span style='display: inline-block; padding: 4px 10px; margin: 2px; border-radius: 15px; background-color: #2c3e50; border: 1px solid #4834D4; font-size: 0.8em; color: white;'>VectorDb 🗄️</span>
        <span style='display: inline-block; padding: 4px 10px; margin: 2px; border-radius: 15px; background-color: #2c3e50; border: 1px solid #6AB04C; font-size: 0.8em; color: white;'>NLP 🗣️</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Social links
col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])

with col2:
    st.markdown('<p style="text-align: center; margin: 0;"><a href="https://github.com/Ratnesh-181998" target="_blank" style="text-decoration: none; color: #2ecc71; font-size: 1.1rem; font-weight: 600;">🔗 GitHub</a></p>', unsafe_allow_html=True)

with col3:
    st.markdown('<p style="text-align: center; margin: 0;"><a href="mailto:rattudacsit2021gate@gmail.com" style="text-decoration: none; color: #3498db; font-size: 1.1rem; font-weight: 600;">📧 Email</a></p>', unsafe_allow_html=True)

with col4:
    st.markdown('<p style="text-align: center; margin: 0;"><a href="https://www.linkedin.com/in/ratneshkumar1998/" target="_blank" style="text-decoration: none; color: #9b59b6; font-size: 1.1rem; font-weight: 600;">💼 LinkedIn</a></p>', unsafe_allow_html=True)

# Close the visual footer
st.markdown("""
<div style='height: 10px; background: linear-gradient(135deg, rgba(46, 204, 113, 0.15) 0%, rgba(52, 152, 219, 0.15) 100%); border-radius: 0 0 10px 10px; border-bottom: 2px solid #2ecc71; margin-top: -10px;'></div>
""", unsafe_allow_html=True)

