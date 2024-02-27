import requests
import pandas as pd
import numpy as np


url = "https://api.opensea.io/api/v2/collections/mutant-ape-yacht-club/stats"

headers = {
    "accept": "application/json",
    "x-api-key": "29b6c9b1120748878ac7f50821ec4d0b"
}

response = requests.get(url, headers=headers)

response_data = response.json()

total_data = response_data['total']
df_total = pd.DataFrame([total_data])

intervals_data = response_data['intervals']
df_intervals = pd.DataFrame(intervals_data)

df_total.to_csv('total_stats.csv', index=False)
df_intervals.to_csv('intervals_stats.csv', index=False)

print(df_intervals)
print(df_total)

