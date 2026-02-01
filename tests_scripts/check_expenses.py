import sqlite3

conn = sqlite3.connect('enterprise_bi_db.sqlite')
cursor = conn.cursor()

print("Analyzing IT Expenses...")
print("=" * 60)

it_count = cursor.execute('SELECT COUNT(*) FROM expenses WHERE department_id = "IT"').fetchone()[0]
print(f"Total IT expenses: {it_count}")

non_tax_it_gt_5k = cursor.execute('SELECT COUNT(*) FROM expenses WHERE department_id = "IT" AND tax_deductible = 0 AND amount > 5000').fetchone()[0]
print(f"Non-tax-deductible IT expenses > $5000: {non_tax_it_gt_5k}")

if non_tax_it_gt_5k > 0:
    print("\nSample records:")
    samples = cursor.execute('SELECT * FROM expenses WHERE department_id = "IT" AND tax_deductible = 0 AND amount > 5000 LIMIT 5').fetchall()
    for s in samples:
        print(s)

# Check unique values in department_id
depts = cursor.execute('SELECT DISTINCT department_id FROM expenses').fetchall()
print(f"\nAll departments in DB: {[d[0] for d in depts]}")

conn.close()
