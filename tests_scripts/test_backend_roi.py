import requests
import json

# Test the backend API directly
url = "http://localhost:8000/ask"
payload = {
    "question": "Calculate regional ROI by comparing marketing spend vs sales revenue for each region.",
    "tenant_id": "test_tenant",
    "user_id": "test_user"
}

print("Sending request to backend...")
response = requests.post(url, json=payload)
print(f"Status Code: {response.status_code}")

# Save to file
with open("backend_response.json", "w") as f:
    json.dump(response.json(), f, indent=2)

print("Response saved to backend_response.json")
print("\nData preview:")
data = response.json()
if "data" in data:
    print(f"Number of records: {len(data['data'])}")
    print("First record:", data['data'][0] if data['data'] else "No data")
