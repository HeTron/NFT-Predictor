# src/api.py

import requests
import os
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Retrieve API key from environment variable
OPENSEA_API_KEY = os.getenv("OPENSEA_API")

# Set the API endpoint URL for fetching the Bored Ape Yacht Club collection NFTs
COLLECTION_SLUG = "boredapeyachtclub"
URL = f"https://api.opensea.io/api/v2/collection/{COLLECTION_SLUG}/nfts"

# Set the headers including your API key
headers = {
    "Accept": "application/json",
    "X-API-KEY": OPENSEA_API_KEY
}

# Define the path for the raw data
RAW_DATA_PATH = '../data/raw/'

# Ensure the raw data directory exists
if not os.path.exists(RAW_DATA_PATH):
    os.makedirs(RAW_DATA_PATH)

# Define a function to fetch data and save it to the raw folder
def fetch_and_save_collection_data():
    response = requests.get(URL, headers=headers)
    if response.status_code == 200:
        data = response.json()

        # Define the file path relative to the current file
        file_path = os.path.join(os.path.dirname(__file__), RAW_DATA_PATH, 'bored_ape_yacht_club_data.json')

        # Write the data to a file in the raw folder
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)

        print(f"Data fetched and saved to {file_path}")
    else:
        print(f"Failed to fetch data: Status code {response.status_code}")
        print("Response content:", response.text)

# Run the function
if __name__ == "__main__":
    fetch_and_save_collection_data()