from flask import Flask, jsonify, request, render_template_string
from flask_cors import CORS
from pymongo import MongoClient
import json
import os

app = Flask(__name__)
CORS(app)  

MONGO_URI = "mongodb://localhost:27017"
client = MongoClient(MONGO_URI)
db = client["mydatabase"]
collection = db["mycollection"]


@app.route('/api', methods=['GET'])
def get_data():
    file_path = os.path.join(os.path.dirname(__file__), 'data.json')
    with open(file_path, 'r') as f:
        data = json.load(f)
    return jsonify(data)

@app.route('/submit', methods=['POST'])
def submit_data():
    try:
        form_data = request.json  
        collection.insert_one(form_data)
        return jsonify({"success": True, "message": "Data submitted successfully"}), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
