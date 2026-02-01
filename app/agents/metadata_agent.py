from app.memory.mem0_client import memory
from langchain_groq import ChatGroq
import os
from app.agents.vault import get_vault_entry

def run(state):
    # 0. Check Vault First (Short Circuit Groq)
    entry = get_vault_entry(state["question"])
    if entry:
        state["metadata"] = {
            "tables": entry["tables"],
            "columns": ["*"]
        }
        state["sql"] = entry["sql"] # Pre-load SQL to skip sql_agent block
        print(f"[VAULT] Shortcut activated for: {state['question']}")
        return state

    # 1. Memory Context
    try:
        memory.search(state["question"], user_id=state["user_id"])
    except Exception as e:
        print(f"Memory warning: {e}")

    # 2. Dynamic Router LLM
    api_key = os.getenv("GROQ_API_KEY")
    if api_key and api_key != "your_groq_key":
        llm = ChatGroq(model="llama-3.3-70b-versatile")
        prompt = f"""
        You are a Metadata Router & Query Interpreter. 
        Your job is to identify the correct database tables and NORMALIZE the question even if it has typos or is incomplete.
        
        1. **Auto-Correct:** Fix obvious typos (e.g., "revnu" -> revenue, "regin" -> region).
        2. **Expand:** If the sentence is incomplete (e.g., "Feb 2026 region wise"), expand it (e.g., "Show region-wise sales and performance for February 2026").
        3. **Map:** Match the intent to these 15 tables:
           sales, customers, products, regions, marketing, subscriptions, support_tickets, 
           inventory, employee_performance, website_traffic, expenses, competitor_metrics, 
           churn_analysis, product_reviews, operating_budget
        
        History: {state.get('history', [])}
        Question: {state['question']}
        
        Output ONLY a JSON object:
        {{"corrected_question": "the fixed question", "tables": ["table1", "table2"]}}
        """
        import json
        try:
            raw_response = llm.invoke(prompt).content.strip()
            # Handle potential markdown backticks
            if "```" in raw_response:
                raw_response = raw_response.split("```")[1].replace("json", "").strip()
            
            data = json.loads(raw_response)
            state["corrected_question"] = data.get("corrected_question", state["question"])
            selected_tables = data.get("tables", ["sales"])
        except Exception as e:
            print(f"Metadata Parse Error: {e}")
            state["corrected_question"] = state["question"]
            selected_tables = ["sales"]
    else:
        state["corrected_question"] = state["question"]
        selected_tables = ["sales"] # Default fallback

    state["metadata"] = {
        "tables": selected_tables,
        "columns": ["*"] # Let SQL Agent handle specific columns
    }
    return state
