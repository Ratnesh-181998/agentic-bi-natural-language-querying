import requests

payload = {
    "tenant_id": "t1",
    "user_id": "u1",
    "question": "give feb 2026 region wise data analysis",
    "history": []
}

try:
    response = requests.post("http://localhost:8000/ask", json=payload)
    if response.status_code == 200:
        print("Response Success!")
        print(response.json())
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
except Exception as e:
    print(f"Connection Error: {e}")
