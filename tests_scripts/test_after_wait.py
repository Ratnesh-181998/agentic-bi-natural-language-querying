import requests
import json
import time

print("Waiting 60 seconds for rate limit to reset...")
time.sleep(60)

query = "Calculate the average customer satisfaction score for bug-related tickets."
url = "http://localhost:8000/ask"

print(f"\nTesting: {query}")

payload = {
    "question": query,
    "tenant_id": "test_tenant",
    "user_id": "test_user"
}

try:
    response = requests.post(url, json=payload, timeout=30)
    print(f"Status Code: {response.status_code}")
    
    data = response.json()
    
    if "error" in data:
        print(f"\n❌ ERROR: {data['error']}")
    else:
        print(f"\n✅ SUCCESS!")
        print(f"Records returned: {len(data.get('data', []))}")
        print(f"Primary KPI: {data['kpis']['primary_label']} = {data['kpis']['primary_val']}")
        print(f"\nData: {json.dumps(data['data'], indent=2)}")
        print(f"\nSQL: {data['sql']}")
    
except Exception as e:
    print(f"❌ EXCEPTION: {str(e)}")
