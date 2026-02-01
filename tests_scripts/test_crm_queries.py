import requests
import json
import time

# Test all CRM & Retention queries
queries = [
    {
        "name": "Churn Reasons",
        "question": "What are the top 3 reasons for customer churn in the last year?"
    },
    {
        "name": "Subscription Health",
        "question": "Show me the count of active vs canceled subscriptions across all plans."
    },
    {
        "name": "Top Loyalty Tiers",
        "question": "Which loyalty tier (Gold/Silver/Bronze) has the highest total lifetime spend?"
    },
    {
        "name": "Signup Trends",
        "question": "Show a monthly trend of new customer signups from 2023 to 2025."
    },
    {
        "name": "Acquisition ROI",
        "question": "Compare the total spend of customers acquired through Google Ads vs Referrals."
    },
    {
        "name": "Plan Revenue Mix",
        "question": "Show me the MRR (Monthly Recurring Revenue) share percentage of SaaS Pro vs Elite."
    }
]

url = "http://localhost:8000/ask"
results = []

print("=" * 80)
print("TESTING CRM & RETENTION QUERIES")
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
                "error": data['error'][:100]
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
