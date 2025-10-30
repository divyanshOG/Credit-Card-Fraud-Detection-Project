import requests
import json

# This is the URL where your local server is running
url = 'http://127.0.0.1:5000/predict'

# --- Sample Transaction 1 (Should be Legitimate) ---
# This data mimics what your frontend form would send
test_data = {
    "Amount": 120.50,
    "Age": 35.0,
    "Type of Card": "Visa",
    "Entry Mode": "Tap",
    "Type of Transaction": "POS",
    "Merchant Group": "Restaurant",
    "Gender": "M",
    "Bank": "Lloyds",
    "Day of Week": "Wednesday",
    "Country of Transaction": "United Kingdom",
    "Country of Residence": "United Kingdom",
    "Shipping Address": "United Kingdom"
}

print("Sending test request...")

try:
    # Send the data as JSON in a POST request
    response = requests.post(url, json=test_data)
    
    # Check if the request was successful
    if response.status_code == 200:
        print("\n--- ✅ Prediction Received ---")
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"\n--- ❌ Error ---")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")

except requests.exceptions.ConnectionError:
    print("\n--- ❌ Connection Error ---")
    print("Could not connect to the server. Is app.py running?")