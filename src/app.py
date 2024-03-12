from flask import Flask, render_template, request, jsonify
from builtins import FileNotFoundError
import json

app = Flask(__name__, static_url_path='/static', template_folder='../templates')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/nfts')
def get_nfts():
    with open('data/raw/bored_ape_yacht_club_data.json') as file:
        data = json.load(file)
        nfts = data['nfts']
        return jsonify(nfts)

@app.route('/predict', methods=['POST'])
def predict():
    nft_input = request.form.get('nft_input')
    try:
        # Load your NFT data
        with open('data/raw/bored_ape_yacht_club_data.json', 'r') as file:
            nfts = json.load(file)['nfts']
        
        # Find the NFT by identifier
        nft_data = next((item for item in nfts if item["identifier"] == nft_input), None)
        
        if nft_data:
            # Process the NFT data and make a prediction
            prediction = "This NFT will be worth X amount"
            return render_template('nft_details.html', nft_data=nft_data, prediction=prediction)
        else:
            # NFT was not found
            return jsonify({"message": "NFT not found"}), 404
    except FileNotFoundError:
        return jsonify({"message": "Data file not found"}), 500

if __name__ == '__main__':
    app.run(debug=True)