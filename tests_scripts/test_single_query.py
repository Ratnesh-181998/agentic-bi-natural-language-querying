import requests
import json

# Test individual query
query = {
    "name": "Subscription Health",
    "question": "Show me the count of active vs canceled subscriptions across all plans."
}

url = "http://localhost:8000/ask"

print(f"Testing: {query['name']}")
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
        print(f"❌ ERROR: {data['error']}")
    else:
        record_count = len(data.get('data', []))
        print(f"✅ PASS - {record_count} records returned")
        print(f"Primary KPI: {data['kpis']['primary_label']} = {data['kpis']['primary_val']:,.2f}")
        print(f"Data: {json.dumps(data['data'], indent=2)}")
        
except Exception as e:
    print(f"❌ EXCEPTION: {str(e)}")
