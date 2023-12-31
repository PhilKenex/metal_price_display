import requests
import json
from datetime import datetime
import csv

with open(r"C:\Users\PhilGreville\OneDrive - Kenex Ltd\Projects_PG\metal_price_display\api_key.txt", 'r') as api_key_file:
    api_key = api_key_file.read().strip()

# 1. Load Existing Data from the provided file
with open(r"C:\Users\PhilGreville\OneDrive - Kenex Ltd\Projects_PG\metal_price_display\rounded_structured_metal_data.json", 'r') as file:
    data = json.load(file)
    metals_data = data["Metals"]

# Connect to API and define API parameters
url_1 = f"https://metals-api.com/api/latest?access_key={api_key}&base=AUD&symbols=ANTIMONY%2CLCO%2CLEAD%2CLITHIUM%2CMO"
url_2 = f"https://metals-api.com/api/latest?access_key={api_key}&base=AUD&symbols=NI%2CTIN%2CTUNGSTEN%2CXAG%2CXAU"
url_3 = f"https://metals-api.com/api/latest?access_key={api_key}&base=AUD&symbols=XCU%2CXPD%2CXPT%2CZNC%2CTE%2CGALLIUM"
# url_4 = f"https://metals-api.com/api/latest?access_key={api_key}&base=AUD&symbols=TE%2CGALLIUM"

response_1 = requests.request("GET", url_1)
response_2 = requests.request("GET", url_2)
response_3 = requests.request("GET", url_3)
# response_4 = requests.request("GET", url_4)

# Combine data from API responses
data = response_1.json()
data['rates'].update(response_2.json()['rates'])
data['rates'].update(response_3.json()['rates'])
# data['rates'].update(response_4.json()['rates'])

# Adjust rates
for key, value in data['rates'].items():
    if key not in ['XAU', 'XAG', 'XPD', 'XPT', 'XCU']:
        data['rates'][key] = 1 / value

# Conversion calculations
data['rates']['TUNGSTEN'] *= 3215000
for key in ['ANTIMONY', 'LEAD', 'NI', 'XCU', 'TIN','TE','GALLIUM']:
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
with open(r"C:\Users\PhilGreville\OneDrive - Kenex Ltd\Projects_PG\metal_price_display\rounded_structured_metal_data.json", 'w') as file:
    json.dump({"Metals": metals_data}, file)

# Load the JSON data from the file
with open(r"C:\Users\PhilGreville\OneDrive - Kenex Ltd\Projects_PG\metal_price_display\rounded_structured_metal_data.json", 'r') as file:
    data = json.load(file)

# Get the metal data from the 'Metals' key
metals_data = data['Metals']

# CSV file path
csv_file_path = r'C:\Users\PhilGreville\OneDrive - Kenex Ltd\Projects_PG\metal_price_display\test.csv'

# Flatten the data into rows with one price entry per row
flattened_rows = []
for entry in metals_data:
    metal_info = {key: value for key, value in entry.items() if key != 'Prices'}
    for price_entry in entry['Prices']:
        row = {**metal_info, **price_entry}
        flattened_rows.append(row)

# Write the flattened data to a CSV file
with open(csv_file_path, mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=flattened_rows[0].keys())
    writer.writeheader()
    for record in flattened_rows:
        writer.writerow(record)