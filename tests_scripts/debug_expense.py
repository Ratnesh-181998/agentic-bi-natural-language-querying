import requests
import json

url = "http://localhost:8000/ask"
payload = {
    "question": "Identify all non-tax-deductible expenses greater than $5000 in the IT department.",
    "tenant_id": "test_tenant",
    "user_id": "test_user"
}

print("Sending request for Expense Audit...")
try:
    response = requests.post(url, json=payload)
    print(f"Status: {response.status_code}")
    data = response.json()
    print("Response JSON:")
    print(json.dumps(data, indent=2))
except Exception as e:
    print(f"Error: {e}")
