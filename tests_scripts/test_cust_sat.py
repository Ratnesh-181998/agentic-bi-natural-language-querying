import requests
import json

# Test the customer satisfaction query
query = "Calculate the average customer satisfaction score for bug-related tickets."

url = "http://localhost:8000/ask"

print(f"Testing: {query}")

payload = {
    "question": query,
    "tenant_id": "test_tenant",
    "user_id": "test_user"
}

try:
    response = requests.post(url, json=payload, timeout=30)
    print(f"Status Code: {response.status_code}")
    
    data = response.json()
    
    # Save full response
    with open("cust_satisfaction_response.json", "w") as f:
        json.dump(data, f, indent=2)
    
    print("\nResponse:")
    print(json.dumps(data, indent=2))
    
except Exception as e:
    print(f"❌ EXCEPTION: {str(e)}")
