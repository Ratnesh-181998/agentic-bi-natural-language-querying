from app.agents.vault import get_vault_entry
import sqlite3
import pandas as pd

question = "Analyze the impact of product reviews on regional sales growth."
print(f"Testing Question: '{question}'")

entry = get_vault_entry(question)
if entry:
    print(f"✅ Vault Hit!")
    print(f"SQL: {entry['sql']}")
    
    # Test SQL execution
    try:
        conn = sqlite3.connect('enterprise_bi_db.sqlite')
        df = pd.read_sql_query(entry['sql'], conn)
        print("\nResult Data:")
        print(df)
        print(f"\nRow count: {len(df)}")
        conn.close()
    except Exception as e:
        print(f"❌ Execution Error: {e}")
else:
    print("❌ Vault Miss!")
