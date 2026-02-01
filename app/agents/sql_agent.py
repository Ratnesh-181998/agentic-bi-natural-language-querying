from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

load_dotenv()

def get_llm():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key or api_key == "your_groq_key":
        return None
    return ChatGroq(model="llama-3.3-70b-versatile")

from app.agents.vault import get_vault_entry

def run(state):
    # --- ENTERPRISE QUERY JOIN VAULT (Instant Fallback & Performance) ---
    # Check if SQL was already set by metadata_agent vault check
    if "sql" in state and state["sql"]:
        print(f"[VAULT] SQL already set for: {state['question']}")
        return state

    # Direct check just in case
    entry = get_vault_entry(state["question"])
    if entry:
        state["sql"] = entry["sql"]
        return state

    llm = get_llm()
    if llm:
        prompt = f"""
        You are an Enterprise BI Expert. Generate only the SQL query for the following question.
        
        # SCHEMA CONTEXT (15 Enterprise Tables):
        1. sales: transaction_id, revenue, date, region, product, customer_id, discount, quantity, unit_price, tax
        2. customers: customer_id, name, email, country, signup_date, loyalty_tier, total_spend, acquisition_channel, last_login, age
        3. products: product_id, name, category, base_price, production_cost, stock_level, release_date, rating, returns_count, shelf_life_days
        4. regions: region_id, name, manager, budget_allocated, target_revenue, active_reps, population_coverage, office_count, tax_rate, seasonality_factor
        5. marketing: campaign_id, name, channel, spend, clicks, conversions, date, impressions, roi, manager_id, region
        6. subscriptions: sub_id, customer_id, plan_name, monthly_price, start_date, expiry_date, status, renewal_count, churn_reason, auto_renew
        7. support_tickets: ticket_id, customer_id, issue_type, priority, status, created_date, resolved_date, agent_name, resolution_time_hrs, customer_satisfaction
        8. inventory: entry_id, product_id, warehouse_location, quantity_on_hand, reorder_point, supplier_name, last_restock_date, unit_weight, storage_cost, bin_number
        9. employee_performance: emp_id, name, role, department, quota, actual_sales, bonus_percentage, join_date, training_completed, review_score
        10. website_traffic: traffic_id, date, sessions, users, bounce_rate, avg_session_duration, pageviews_per_session, conversion_rate, device_type, traffic_source
        11. expenses: expense_id, category, amount, date, department_id, vendor_name, payment_method, tax_deductible, approval_status, description
        12. competitor_metrics: comp_id, competitor_name, product_name, market_price, market_share, rating, year, tech_score, region, ad_spend_estimate
        13. churn_analysis: churn_id, customer_id, churn_date, primary_reason, secondary_reason, retention_offered, feedback_score, account_age_months, switch_to_competitor, refund_granted
        14. product_reviews: review_id, product_id, customer_id, rating, review_date, sentiment_score, verified_purchase, helpful_votes, review_length, platform
        15. operating_budget: budget_id, year, quarter, department, allocated_budget, actual_spend, variance, approved_by, last_updated, notes

        # RESILIENCE & INTENT RULES:
        1. **Handle Typos:** If the user makes spelling mistakes (e.g., "revnu" for revenue, "regin" for region), normalize them based on the Schema Context.
        2. **Infer Intent:** If the query is just a phrase (e.g. "Feb 2026 sales"), interpret it as a request for "Total revenue and related details for that time period".
        3. **Date Precision:** If a month/year is specified, use exact filters like `LIKE '2026-02%'` or `>= '2026-02-01'`.
        
        Strict Rules:
        1. Use SQLite syntax ONLY. No Postgres/MySQL specific functions (e.g. No CORR, STDDEV, MEDIAN).
        2. For correlations or trends, SELECT the raw columns (e.g. SELECT date, column1, column2) and let the system handle analysis.
        3. Respect the user's requested date range. If they ask for 2026, use 2026. Only use "BETWEEN '2024-01-01' AND '2025-12-31'" if the user asks for "recent" or "standard" data without specifying a year.
        4. JOIN tables whenever necessary (e.g. sales.customer_id = customers.customer_id).
        5. Output ONLY the raw SQL. No markdown, no "Query:", no formatting.
        
        # PREVIOUS CONVERSATION CONTEXT
        History: {state.get('history', [])}
        Question: {state.get('corrected_question', state['question'])}
        SQL Query:"""
        state["sql"] = llm.invoke(prompt).content.strip()
    else:
        # Fallback simple logic
        q = state["question"].lower()
        if "revenue" in q or "sales" in q:
            state["sql"] = "SELECT * FROM sales"
        else:
            state["sql"] = "SELECT * FROM sales LIMIT 10"
            
    # Clean SQL - remove all markdown and noise
    sql = state["sql"]
    if "```" in sql:
        # Extract content between backticks
        import re
        matches = re.findall(r"```(?:sql)?\s*(.*?)\s*```", sql, re.DOTALL)
        if matches:
            sql = matches[0]
        else:
            sql = sql.replace("```sql", "").replace("```", "")
    
    state["sql"] = sql.strip().rstrip(';')
    return state
