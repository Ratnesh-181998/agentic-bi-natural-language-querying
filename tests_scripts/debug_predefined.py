import requests
import json

url = "http://localhost:8000/ask"
payload = {
    "question": "Calculate the average customer satisfaction score for bug-related tickets.",
    "tenant_id": "test_tenant",
    "user_id": "test_user"
}

print("Sending request...")
try:
    response = requests.post(url, json=payload)
    print(f"Status: {response.status_code}")
    data = response.json()
    print("Response JSON:")
    print(json.dumps(data, indent=2))
except Exception as e:
    print(f"Error: {e}")
