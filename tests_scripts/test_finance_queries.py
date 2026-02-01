import requests
import json
import time

# Test all Finance & Strategy queries
queries = [
    {
        "name": "Budget vs Actual '25",
        "question": "Compare allocated budget vs actual spend by department for all quarters of 2025."
    },
    {
        "name": "High Expense Depts",
        "question": "Which departments have the highest total expenses across 2024 and 2025?"
    },
    {
        "name": "2026 Revenue Project",
        "question": "What is the total projected revenue for each month in 2026 based on current sales?"
    },
    {
        "name": "Variance Analysis",
        "question": "Show me departments where actual spend exceeded the budget by more than 10%."
    },
    {
        "name": "OpEx Breakdown",
        "question": "Break down total operating expenses by category for the last 12 months."
    },
    {
        "name": "ROI per Region",
        "question": "Calculate regional ROI by comparing marketing spend vs sales revenue for each region."
    }
]

url = "http://localhost:8000/ask"
results = []

print("=" * 80)
print("TESTING FINANCE & STRATEGY QUERIES")
print("=" * 80)

for i, query in enumerate(queries, 1):
    print(f"\n[{i}/6] Testing: {query['name']}")
    print(f"Question: {query['question']}")
    
    payload = {
        "question": query["question"],
        "tenant_id": "test_tenant",
        "user_id": "test_user"
    }
    
    try:
        response = requests.post(url, json=payload, timeout=30)
        data = response.json()
        
        if "error" in data:
            print(f"❌ ERROR: {data['error'][:200]}...")
            results.append({
                "query": query['name'],
                "status": "FAILED",
                "error": data['error']
            })
        else:
            record_count = len(data.get('data', []))
            has_data = record_count > 0
            
            status = "✅ PASS" if has_data else "⚠️  NO DATA"
            print(f"{status} - {record_count} records returned")
            
            if has_data:
                print(f"   Primary KPI: {data['kpis']['primary_label']} = {data['kpis']['primary_val']:,.2f}")
                print(f"   Sample data: {data['data'][0]}")
            
            results.append({
                "query": query['name'],
                "status": "PASS" if has_data else "NO_DATA",
                "records": record_count,
                "kpi": data['kpis']['primary_label'] if has_data else None
            })
        
        time.sleep(1)  # Rate limiting
        
    except Exception as e:
        print(f"❌ EXCEPTION: {str(e)}")
        results.append({
            "query": query['name'],
            "status": "EXCEPTION",
            "error": str(e)
        })

# Summary
print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)
passed = sum(1 for r in results if r['status'] == 'PASS')
print(f"Passed: {passed}/6")
print(f"Failed: {6 - passed}/6")

for r in results:
    status_icon = "✅" if r['status'] == 'PASS' else "❌"
    print(f"{status_icon} {r['query']}: {r['status']}")
