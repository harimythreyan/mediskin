from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
import json
from bson import ObjectId
from bson.json_util import dumps

app = Flask(__name__)
CORS(app)

# MongoDB connection
MONGO_CONN_URL = 'mongodb+srv://admin:admin_123@mediskin.cjgumpn.mongodb.net/'
MONGO_DB_NAME = "Medicine_db"
USER_COLLECTION = "medicine"

# Connect to MongoDB
client = MongoClient(MONGO_CONN_URL)
db = client[MONGO_DB_NAME]
collection = db[USER_COLLECTION]

# Helper function to convert MongoDB documents to JSON
def parse_json(data):
    return json.loads(dumps(data))

# Route to get all medicine names
@app.route('/medicines', methods=['GET'])
def get_medicines():
    try:
        # Debug: Print the count of documents in the collection
        count = collection.count_documents({})
        print(f"Total medicines in database: {count}")
        
        # Fetch all medicine names and IDs
        cursor = collection.find({}, {"name": 1, "id": 1, "_id": 1})
        medicines = list(cursor)
        
        # Debug: Print how many medicines we found
        print(f"Medicines found: {len(medicines)}")
        
        # Debug: Print the first few documents if any
        if medicines:
            print("Sample medicines:", medicines[:3])
        
        return jsonify({"status": "success", "data": parse_json(medicines)}), 200
    except Exception as e:
        print(f"Error in /medicines route: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

# Route to get all medicine names (alternative that returns everything)
@app.route('/all-medicines', methods=['GET'])
def get_all_medicines():
    try:
        # Return all documents without field filtering
        medicines = list(collection.find({}))
        return jsonify({"status": "success", "data": parse_json(medicines)}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# Route to get medicine details by name
@app.route('/medicine/<name>', methods=['GET'])
def get_medicine_by_name(name):
    try:
        # Search for the medicine case-insensitive
        medicine = collection.find_one({"name": {"$regex": f"^{name}$", "$options": "i"}})
        if medicine:
            return jsonify({"status": "success", "data": parse_json(medicine)}), 200
        else:
            return jsonify({"status": "error", "message": "Medicine not found"}), 404
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# Alternative route to get medicine details by ID
@app.route('/medicine/id/<id>', methods=['GET'])
def get_medicine_by_id(id):
    try:
        medicine = collection.find_one({"id": int(id)})
        if medicine:
            return jsonify({"status": "success", "data": parse_json(medicine)}), 200
        else:
            return jsonify({"status": "error", "message": "Medicine not found"}), 404
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# Route to list all collection names for debugging
@app.route('/collections', methods=['GET'])
def get_collections():
    try:
        collections = db.list_collection_names()
        return jsonify({"status": "success", "collections": collections}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# Debug route to verify connection
@app.route('/', methods=['GET'])
def home():
    return jsonify({"status": "success", "message": "API is running"}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
