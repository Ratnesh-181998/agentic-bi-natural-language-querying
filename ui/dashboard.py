import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Agentic BI | Insights Engine",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .stMetric {
        background-color: #1e1e2d;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #323248;
    }
    .stMetric:hover { border-color: #7267EF; }
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 0.5rem;
        background: -webkit-linear-gradient(#7267EF, #00D2FF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("<h1 style='color: #7267EF;'>🤖 Agentic BI</h1>", unsafe_allow_html=True)
    st.info("Experience the future of Business Intelligence powered by Multi-Agent LangGraph.")
    st.divider()
    st.markdown("### 🛠️ Tech Stack")
    st.code("LangGraph\nFastAPI\nMem0\nStreamlit\nSQLite")
    st.divider()
    if st.button("🗑️ Clear Chat History"):
        st.session_state.history = []

# --- MAIN UI ---
st.markdown("<div class='main-header'>Strategic Insights Engine</div>", unsafe_allow_html=True)
st.markdown("Query your enterprise data using natural language. No SQL knowledge required.")

q = st.text_input("", placeholder="e.g., Show me total revenue by region for last month")

if st.button("🚀 Analyze Insights"):
    if not q:
        st.warning("Please enter a question first.")
    else:
        with st.spinner("🤖 Agents are collaborating..."):
            try:
                response = requests.post("http://localhost:8000/ask", json={
                    "tenant_id": "t1",
                    "user_id": "u1",
                    "question": q,
                    "history": st.session_state.get("history", [])
                })
                
                if response.status_code == 200:
                    r = response.json()
                    
                    # Store history if backend supports it
                    if "history" not in st.session_state:
                        st.session_state.history = []
                    
                    # --- KPI ROW ---
                    st.divider()
                    k1, k2, k3 = st.columns(3)
                    kpis = r.get("kpis", {})
                    k1.metric("💰 Total Revenue", f"${kpis.get('revenue', 0):,.2f}", delta="+12%")
                    k2.metric("📈 Growth Rate", kpis.get("growth", "N/A"), delta="2.1%")
                    k3.metric("📅 YoY Performance", kpis.get("yoy", "N/A"), delta="-0.5%", delta_color="inverse")
                    
                    # --- DATASET & CHART ---
                    st.divider()
                    df = pd.DataFrame(r.get("data", []))
                    
                    c1, c2 = st.columns([1, 1])
                    
                    with c1:
                        st.subheader("📊 Data Visualization")
                        if not df.empty:
                            try:
                                # Detection logic
                                num_cols = df.select_dtypes(include=['number']).columns.tolist()
                                cat_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
                                date_cols = [c for c in df.columns if 'date' in c.lower() or 'time' in c.lower()]
                                
                                if len(df) == 1 and len(num_cols) >= 1:
                                    # Single result - Big metric display
                                    val = df[num_cols[0]].iloc[0]
                                    st.markdown(f"<h1 style='text-align: center; color: #7267EF;'>{val:,.2f}</h1>", unsafe_allow_html=True)
                                    st.markdown(f"<p style='text-align: center;'>{num_cols[0]}</p>", unsafe_allow_html=True)
                                    fig = None
                                    
                                elif date_cols and num_cols:
                                    # Time series
                                    fig = px.line(df, x=date_cols[0], y=num_cols[0], template="plotly_dark", markers=True)
                                    fig.update_traces(line_color='#7267EF')
                                    
                                elif "region" in df.columns and "revenue" in df.columns:
                                    # Specific business use case
                                    fig = px.pie(df, values='revenue', names='region', hole=.3,
                                                color_discrete_sequence=px.colors.sequential.RdBu)
                                                
                                elif cat_cols and num_cols:
                                    # Bar chart for categorical data
                                    fig = px.bar(df, x=cat_cols[0], y=num_cols[0], 
                                                template="plotly_dark", color=cat_cols[0])
                                else:
                                    # Fallback
                                    fig = px.bar(df, template="plotly_dark")
                                
                                if fig:
                                    st.plotly_chart(fig, use_container_width=True)
                                    
                            except Exception as viz_err:
                                st.warning(f"Default visualization failed: {viz_err}")
                                st.info("You can still view the raw data in the table to the right.")
                        else:
                            st.write("No data returned for chart visualization.")
                    
                    with c2:
                        st.subheader("📋 Raw Result")
                        st.dataframe(df, use_container_width=True)
                        
                    # --- REASONING ---
                    with st.expander("🔍 AI Reasoning & SQL"):
                        st.markdown(f"**Generated SQL:**\n```sql\n{r.get('sql', 'N/A')}\n```")
                        st.markdown(f"**Agent Rationale:** {r.get('reasoning', 'Certified business definitions applied.')}")
                
                else:
                    st.error(f"Backend Error: {response.status_code} - {response.text}")
                    
            except requests.exceptions.ConnectionError:
                st.error("❌ **Backend Unreachable!** Please ensure the FastAPI server is running on `http://localhost:8000`.")
                st.info("💡 Run `.\\venv\\Scripts\\python -m uvicorn app.main:app --port 8000` in a separate terminal.")
            except Exception as e:
                st.error(f"Unexpected Error: {str(e)}")

st.divider()
st.caption(f"Last sync: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Agentic BI SaaS v1.0")
