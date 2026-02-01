import requests
import json

url = "http://localhost:8000/ask"
payload = {
    "tenant_id": "t1",
    "user_id": "u1",
    "question": "What is the total revenue?",
    "history": []
}

try:
    response = requests.post(url, json=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
except Exception as e:
    print(f"Error: {e}")
