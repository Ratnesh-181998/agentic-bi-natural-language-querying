from app.agents.sql_agent import run
import sqlite3
import pandas as pd

# Mock state
state = {
    "question": "Calculate regional ROI by comparing marketing spend vs sales revenue for each region.",
    "history": []
}

# Run Agent
print("Running Agent...")
result_state = run(state)
sql = result_state.get("sql")
print(f"Generated SQL: {sql}")

# Execute SQL
print("Executing SQL...")
try:
    conn = sqlite3.connect('enterprise_bi_db.sqlite')
    df = pd.read_sql_query(sql, conn)
    print("Result Data:")
    print(df)
    print(f"Row count: {len(df)}")
    conn.close()
except Exception as e:
    print(f"SQL Execution Error: {e}")
