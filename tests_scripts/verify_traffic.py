import sqlite3
import pandas as pd

conn = sqlite3.connect('enterprise_bi_db.sqlite')
cursor = conn.cursor()

print("Verifying website_traffic table...")
print("=" * 60)

# Check columns
columns = cursor.execute('PRAGMA table_info(website_traffic)').fetchall()
print("Columns:")
for col in columns:
    print(f"  {col[1]} ({col[2]})")

# Check 2024 data
count_2024 = cursor.execute('SELECT COUNT(*) FROM website_traffic WHERE date LIKE "2024%"').fetchone()[0]
print(f"\nTotal 2024 records: {count_2024}")

# Sample join logic used in vault
sql = "SELECT strftime('%Y-%m', date) as month, SUM(sessions) as sessions, SUM(conversions) as conversions FROM website_traffic WHERE date LIKE '2024%' GROUP BY month"
try:
    df = pd.read_sql_query(sql, conn)
    print("\nVault Query Result (Correlation):")
    print(df)
except Exception as e:
    print(f"\n❌ Vault Query Error: {e}")

conn.close()
