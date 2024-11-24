import json
import csv
import requests
from requests_aws4auth import AWS4Auth

access_key = "AKIAYQNJSZOICHJU6J4B"
secret_key = "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"
region = "ap-southeast-1"

awsauth = AWS4Auth(
    access_key,
    secret_key,
    region,
    "sagemaker"
)

endpoint_url = "https://runtime.sagemaker.ap-southeast-1.amazonaws.com/endpoints/ep-time-ser-2024-11-23-17-24-04-265-trial-me-1-automl-ts/invocations"
headers = {"Content-Type": "csv"}

def getForecast():
    payload = [
    {"Product_ID": "af86b867929a073d9b6478adcb652d39", "Category": "Grocery & Gourmet Foods", "Sales": 24, "Date": "1/2/23", "Promotional_Info": "No", "Location_Code": "LOC-291"},
    {"Product_ID": "af86b867929a073d9b6478adcb652d39", "Category": "Grocery & Gourmet Foods", "Sales": 3, "Date": "1/3/23", "Promotional_Info": "No", "Location_Code": "LOC-376"},
    {"Product_ID": "af86b867929a073d9b6478adcb652d39", "Category": "Grocery & Gourmet Foods", "Sales": 53, "Date": "1/5/23", "Promotional_Info": "No", "Location_Code": "LOC-559"},
]

    payload_ko_csv = ",".join(payload[0].keys()) + "\n"
    payload_ko_csv += "\n".join(
        ",".join(map(str, row.values())) for row in payload
    )

    response = requests.post(endpoint_url, data=payload_ko_csv, headers=headers, auth=awsauth)

    response_text = response.text.strip()
    lines = response_text.split("\n")

    csv_reader = csv.DictReader(lines)
    output_data = [row for row in csv_reader]

    return output_data

def getForecastForId(productId):
    forecast = getForecast()
    
    data = []
    
    for row in forecast:
        if row["Product_ID"] == productId:
            data.append([row["Date"], row["p90"]])
            
            
    return data
