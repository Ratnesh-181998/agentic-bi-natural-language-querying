import requests
import json
import time

# Test Growth & Marketing and Operations & Support queries
queries = [
    # Growth & Marketing
    {
        "category": "Growth & Marketing",
        "name": "Traffic vs Leads",
        "question": "Show me the correlation between website sessions and marketing conversions for 2024."
    },
    {
        "category": "Growth & Marketing",
        "name": "Competitor Price Gap",
        "question": "Compare our SaaS Pro price against the average competitor market price."
    },
    {
        "category": "Growth & Marketing",
        "name": "Best Campaign ROI",
        "question": "Identify the marketing campaign with the single highest ROI ever recorded."
    },
    {
        "category": "Growth & Marketing",
        "name": "Mobile vs Desktop",
        "question": "Compare the conversion rates of Mobile traffic vs Desktop traffic."
    },
    {
        "category": "Growth & Marketing",
        "name": "Channel Efficiency",
        "question": "Which marketing channel (FB, GAds, LI) has the lowest cost-per-conversion?"
    },
    {
        "category": "Growth & Marketing",
        "name": "Review Sentiments",
        "question": "Analyze the impact of product reviews on regional sales growth."
    },
    # Operations & Support
    {
        "category": "Operations & Support",
        "name": "Support SLA Health",
        "question": "Show me the average resolution time for High Priority tickets by support agent."
    },
    {
        "category": "Operations & Support",
        "name": "Low Stock Alerts",
        "question": "List all products where the current quantity on hand is below the reorder point."
    },
    {
        "category": "Operations & Support",
        "name": "Top Sales Reps",
        "question": "Rank our top 5 Sales Reps by their Actual Sales vs Quota performance."
    },
    {
        "category": "Operations & Support",
        "name": "Expense Audit",
        "question": "Identify all non-tax-deductible expenses greater than $5000 in the IT department."
    },
    {
        "category": "Operations & Support",
        "name": "Warehouse Load",
        "question": "Show the distribution of inventory quantity across all warehouse locations."
    },
    {
        "category": "Operations & Support",
        "name": "Cust Satisfaction",
        "question": "Calculate the average customer satisfaction score for bug-related tickets."
    }
]

url = "http://localhost:8000/ask"
results = []

print("=" * 80)
print("TESTING GROWTH & MARKETING + OPERATIONS & SUPPORT QUERIES")
print("=" * 80)
print("Note: Adding 15-second delays between queries to avoid rate limits")
print("=" * 80)

for i, query in enumerate(queries, 1):
    print(f"\n[{i}/12] Testing: {query['name']} ({query['category']})")
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
            error_msg = data['error']
            if "rate_limit" in error_msg.lower():
                print(f"⏸️  RATE LIMITED - Waiting 30 seconds...")
                time.sleep(30)
                # Retry once
                response = requests.post(url, json=payload, timeout=30)
                data = response.json()
                
            if "error" in data:
                print(f"❌ ERROR: {data['error'][:150]}...")
                results.append({
                    "query": query['name'],
                    "category": query['category'],
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
                results.append({
                    "query": query['name'],
                    "category": query['category'],
                    "status": "PASS" if has_data else "NO_DATA",
                    "records": record_count
                })
        else:
            record_count = len(data.get('data', []))
            has_data = record_count > 0
            
            status = "✅ PASS" if has_data else "⚠️  NO DATA"
            print(f"{status} - {record_count} records returned")
            
            if has_data:
                print(f"   Primary KPI: {data['kpis']['primary_label']} = {data['kpis']['primary_val']:,.2f}")
            
            results.append({
                "query": query['name'],
                "category": query['category'],
                "status": "PASS" if has_data else "NO_DATA",
                "records": record_count
            })
        
        # Wait between queries
        if i < len(queries):
            print(f"   Waiting 15 seconds before next query...")
            time.sleep(15)
        
    except Exception as e:
        print(f"❌ EXCEPTION: {str(e)}")
        results.append({
            "query": query['name'],
            "category": query['category'],
            "status": "EXCEPTION",
            "error": str(e)
        })

# Summary
print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)

# Group by category
categories = {}
for r in results:
    cat = r['category']
    if cat not in categories:
        categories[cat] = []
    categories[cat].append(r)

for cat, cat_results in categories.items():
    passed = sum(1 for r in cat_results if r['status'] == 'PASS')
    total = len(cat_results)
    print(f"\n{cat}: {passed}/{total} passed")
    for r in cat_results:
        status_icon = "✅" if r['status'] == 'PASS' else "❌"
        print(f"  {status_icon} {r['query']}: {r['status']}")

total_passed = sum(1 for r in results if r['status'] == 'PASS')
print(f"\n{'=' * 80}")
print(f"OVERALL: {total_passed}/12 queries passed")
print(f"{'=' * 80}")
