import requests
import json
from datetime import datetime

api_key = "ml97jh99o23eay57z38r0gba871dc13wr3csqg39bw87ywd7d35qd38lfjca"

# 1. Load Existing Data from the provided file
with open('rounded_structured_metal_data.json', 'r') as file:
    data = json.load(file)
    metals_data = data["Metals"]

# Connect to API and define API parameters
url_1 = f"https://metals-api.com/api/latest?access_key={api_key}&base=AUD&symbols=ANTIMONY%2CLCO%2CLEAD%2CLITHIUM%2CMO"
url_2 = f"https://metals-api.com/api/latest?access_key={api_key}&base=AUD&symbols=NI%2CTIN%2CTUNGSTEN%2CXAG%2CXAU"
url_3 = f"https://metals-api.com/api/latest?access_key={api_key}&base=AUD&symbols=XCU%2CXPD%2CXPT%2CZNC"

response_1 = requests.request("GET", url_1)
response_2 = requests.request("GET", url_2)
response_3 = requests.request("GET", url_3)

# Combine data from API responses
data = response_1.json()
data['rates'].update(response_2.json()['rates'])
data['rates'].update(response_3.json()['rates'])

# Adjust rates
for key, value in data['rates'].items():
    if key not in ['XAU', 'XAG', 'XPD', 'XPT', 'XCU']:
        data['rates'][key] = 1 / value

# Conversion calculations
data['rates']['TUNGSTEN'] *= 3215000
for key in ['ANTIMONY', 'LEAD', 'NI', 'XCU', 'TIN']:
    data['rates'][key] *= 35270
for key in ['LCO','LITHIUM','MO','ZNC']:
    data['rates'][key] *= 32150

# Update metals_data with the new prices
now = datetime.now().strftime('%Y-%m-%d')
for metal in metals_data:
    metal_symbol = metal["Metal"]
    if metal_symbol in data["rates"]:
        # Round the price to 2 decimal places
        rounded_price = round(data["rates"][metal_symbol], 2)
        metal["Prices"].append({
            "Date_Collected": now,
            "Price": rounded_price
        })

# Save the updated data back to the file
with open('rounded_structured_metal_data.json', 'w') as file:
    json.dump({"Metals": metals_data}, file)