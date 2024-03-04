from pymongo import MongoClient
from dotenv import load_dotenv
import os
import json

# Load environment variables
load_dotenv()

# Retrieve the MongoDB connection string from the environment variable
connection_string = os.getenv('COSMOSDB_DB_CONNECTION')

# Validate that the connection string is present
if connection_string is None:
    raise Exception("The CosmosDB connection string is not set in the environment variables.")

# Connect to your Cosmos DB account
client = MongoClient(connection_string)

# Specify your database and container
database_name = 'NFTDatabase'
container_name = 'BoredApeYachtClubCollection'

# Now you can work with your database and container (collection in MongoDB terms)
db = client[database_name]
collection = db[container_name]

# Path to the JSON file that contains your data
json_file_path = "E:\\4GeeksProjects\\Final_Project\\NFT_Predictor delete soon\\data\\raw\\bored_ape_yacht_club_data.json"

# Open the JSON file and load its content
with open(json_file_path, 'r') as file:
    data = json.load(file)

# Iterate over each NFT in the JSON data
for nft in data['nfts']:
    # Add the shard key to the document if it's not already present
    nft['collectionName'] = nft.get('collection', 'BoredApeYachtClub')

    # Insert the document into Cosmos DB
    insert_result = collection.insert_one(nft)
    print(f"Inserted document with id: {insert_result.inserted_id}")