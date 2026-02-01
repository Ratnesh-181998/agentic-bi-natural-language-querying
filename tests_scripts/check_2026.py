import sqlite3
conn = sqlite3.connect('enterprise_bi_db.sqlite')
cursor = conn.cursor()
count = cursor.execute("SELECT COUNT(*) FROM sales WHERE date LIKE '2026-02%'").fetchone()[0]
print(f"Sales for Feb 2026: {count}")

# Check other tables too
count_marketing = cursor.execute("SELECT COUNT(*) FROM marketing WHERE date LIKE '2026-02%'").fetchone()[0]
print(f"Marketing for Feb 2026: {count_marketing}")

conn.close()
