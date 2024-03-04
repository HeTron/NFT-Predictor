from flask import Flask, jsonify
import requests
import pandas as pd

app = Flask(__name__)

# Function to fetch data from an API
def fetch_api_data(url, headers=None):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch data from {url}")
        return {}

# Assuming these are your API URLs and headers
url1 = "https://api.opensea.io/api/v2/collections/mutant-ape-yacht-club/stats"
url2 = "https://api.opensea.io/api/v2/collections/mutant-ape-yacht-club"
url3 = "https://api.opensea.io/api/v2/events/collection/mutant-ape-yacht-club"
headers1 = {"accept": "application/json", "x-api-key": "your_api_key"}
headers2 = {"accept": "application/json", "x-api-key": "your_api_key"}
headers3 = {"accept": "application/json", "x-api-key": "your_api_key"}

@app.route('/api1_stats')
def api1_stats():
    data = fetch_api_data(url1, headers1)
    df_total = pd.DataFrame([data['total']])
    df_intervals = pd.DataFrame(data['intervals'])
    # Combine and return as JSON
    combined = pd.concat([df_total, df_intervals], axis=1)
    return combined.to_json(orient='records')

@app.route('/api2_collection')
def api2_collection():
    data = fetch_api_data(url2, headers2)
    collection_fields = ['collection', 'name', 'description', 'image_url', 'banner_image_url', 'owner', 'category', 'is_disabled', 'is_nsfw', 'trait_offers_enabled', 'collection_offers_enabled', 'opensea_url', 'project_url', 'wiki_url', 'discord_url', 'telegram_url', 'twitter_username', 'instagram_username', 'total_supply', 'created_date']
    df_collection = pd.DataFrame([{field: data.get(field, '') for field in collection_fields}])
    return df_collection.to_json(orient='records')

@app.route('/api3_events')
def api3_events():
    data = fetch_api_data(url3, headers3)
    events_normalized = normalize_events(data['asset_events'])
    df_events = pd.DataFrame(events_normalized)
    return df_events.to_json(orient='records')

def normalize_events(events):
    events_normalized = []
    for event in events:
        event_data = {k: v for k, v in event.items() if k not in ['nft', 'asset', 'payment', 'criteria']}
        additional_data = {}
        for key in ['nft', 'asset', 'payment']:
            if key in event and event[key] is not None:
                additional_data.update({f'{key}_{k}': v for k, v in event[key].items()})
        event_data.update(additional_data)
        events_normalized.append(event_data)
    return events_normalized

if __name__ == '__main__':
    app.run(debug=True)