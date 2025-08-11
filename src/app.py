"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
# from models import Person


app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# Create the jackson family object
jackson_family = FamilyStructure("Jackson")


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


# Generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/members', methods=['GET'])
def get_all_members():
    try:
        members = jackson_family.get_all_members()
        return jsonify(members), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/members/<int:member_id>', methods=['GET'])
def get_one_member(member_id):
    try:
        member = jackson_family.get_member(member_id)
        
        if member:
            response = {
                "id": member["id"],
                "first_name": member["first_name"],
                "age": member["age"],
                "lucky_numbers": member["lucky_numbers"]
            }
            return jsonify(response), 200
        else:
            return jsonify({"error": "Member not found"}), 404
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500        
    
@app.route('/members', methods=['POST'])
def add_member():
    member = request.get_json()
    
    if not all(key in member for key in ['first_name', 'age', 'lucky_numbers']):
        return jsonify({"error": "Missing required fields"}), 400
    
    added_member = jackson_family.add_member(member)
    
    return jsonify(added_member), 200

@app.route('/members/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    if jackson_family.delete_member(member_id):
        return jsonify({"done": True}), 200
    else:
        return jsonify({"error": "Member not found"}), 404

# This only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
