import sqlite3

conn = sqlite3.connect('enterprise_bi_db.sqlite')
cursor = conn.cursor()

print("Checking support_tickets data...")
print("=" * 60)

# Check total tickets
total = cursor.execute('SELECT COUNT(*) FROM support_tickets').fetchone()[0]
print(f"Total tickets: {total}")

# Check bug tickets
bug_count = cursor.execute('SELECT COUNT(*) FROM support_tickets WHERE issue_type = "Bug"').fetchone()[0]
print(f"Bug tickets: {bug_count}")

# Check average satisfaction for bug tickets
avg_sat = cursor.execute('SELECT AVG(customer_satisfaction) FROM support_tickets WHERE issue_type = "Bug"').fetchone()[0]
print(f"Average satisfaction (Bug): {avg_sat}")

# Sample data
print("\nSample bug tickets:")
samples = cursor.execute('SELECT ticket_id, issue_type, customer_satisfaction FROM support_tickets WHERE issue_type = "Bug" LIMIT 5').fetchall()
for s in samples:
    print(f"  Ticket {s[0]}: {s[1]} - Satisfaction: {s[2]}")

conn.close()
