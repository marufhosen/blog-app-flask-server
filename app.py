from flask import Flask, jsonify, request
from datetime import datetime, timezone
from bson.objectid import ObjectId
from pymongo import MongoClient
import json

# Flask = class, an intance of WSGI application & __name__ is module so that it can be used to access the static files & templates
app = Flask(__name__)

# MONGODB CLIENT INITIALIZATION
client = MongoClient(
    "mongodb+srv://flask_db:flask_db@cluster0.lvals.mongodb.net/?retryWrites=true&w=majority")

db = client.new_flask_db
collection = db.flask_db

# root route


@app.route('/')
def root():
    return "<h1>Welcome to the Flask API<h1>"

# FILE ALL DATA


@app.route('/data', methods=['GET'])
def get_all_data():
    try:
        result = []
        for doc in collection.find():
            # Convert each document to a dictionary format that can be serialized to JSON
            doc_dict = {"_id": str(
                doc["_id"]), "title": doc["title"], "description": doc["description"], "url": doc["url"], "like": doc["like"], "created_at": doc["created_at"]}
            result.append(doc_dict)
        return jsonify({"data": result})
    except Exception as e:
        error_message = str(e)
        return jsonify({"error": error_message}), 500

# CREATE DATA


@app.route("/create", methods=["POST"])
def insert_data():
    try:
        data = request.json

        # ADD TIMESTAMP
        now = datetime.now(timezone.utc)
        data['created_at'] = now.isoformat()

        result = collection.insert_one(data)
        inserted_property = collection.find_one({"_id": result.inserted_id})
        inserted_doc_dict = {"_id": str(
            inserted_property["_id"]), "title": inserted_property["title"], "description": inserted_property["description"], "url": inserted_property["url"], "like": inserted_property["like"]}
        return jsonify({"status": 200, "message": "Data inserted successfully", "data": inserted_doc_dict}), 200
    except Exception as err:
        error_message = str(err)
        return jsonify({"status": 400, "message": error_message}), 500

# GET DETAIL DATA


@app.route("/detail", methods=["GET"])
def get_single_data():
    try:
        post_id = request.args.get('id')
        print(post_id)
        data = collection.find_one({"_id": ObjectId(post_id)})
        # data = collection.find()
        # for doc in data:
        #     if str(doc["_id"]) == post_id:
        #         data = doc
        #         break
        get_single_doc = {"_id": str(
            data["_id"]), "title": data["title"], "description": data["description"], "url": data["url"], "like": data["like"], "created_at": data["created_at"]}
        return jsonify({"status": 200, "message": "Trying to update data",  "data": get_single_doc}), 200
    except Exception as err:
        error_message = str(err)
        return jsonify({"status": 400, "message": error_message}), 500

# UPDATE DATA


@app.route("/update", methods=["PUT"])
def update_data():
    try:
        update_id = request.args.get('id')
        query = {'_id': ObjectId(update_id)}
        new_data = request.json
        # ADD UPDATE TOME
        now = datetime.now(timezone.utc)
        new_data['updated_at'] = now.isoformat()
        updated_data = {'$set': new_data}
        print(updated_data)
        res = collection.update_one(query, updated_data)
        return jsonify({"status": 200, "message": "Data updated sucessfully"}), 200
    except Exception as err:
        error_message = str(err)
        return jsonify({"status": 400, "message": error_message}), 500


# DELETE DATA


@app.route("/delete", methods=["DELETE"])
def delete_data():
    try:
        delete_id = request.args.get('id')
        query = {'_id': ObjectId(delete_id)}
        res = collection.delete_one(query)
        return jsonify({"status": 200, "message": "Data deleted sucessfully"}), 200
    except Exception as err:
        error_message = str(err)
        return jsonify({"status": 400, "message": error_message}), 500


# SEARCH DATA
@app.route('/search')
def search_data():
    try:
        search_title = request.args.get('search')
        data = collection.find(
            {"title": {"$regex": search_title, "$options": "i"}})
        result = []
        for doc in data:
            # Convert each document to a dictionary format that can be serialized to JSON
            doc_dict = {"_id": str(
                doc["_id"]), "title": doc["title"], "description": doc["description"], "url": doc["url"], "like": doc["like"], "created_at": doc["created_at"]}
            result.append(doc_dict)
        return jsonify({"data": result})
    except Exception as e:
        error_message = str(e)
        return jsonify({"error": error_message}), 500


# ADD LIKE
# SEARCH DATA
@app.route('/like', methods=['PUT'])
def handle_like():
    try:
        id = request.args.get('id')
        query = {'_id': ObjectId(id)}

        # UPDATEABLE DATA
        updateable_data = collection.find_one({"_id": ObjectId(id)})
        result = collection.update_one(
            query, {"$set": {"like": int(updateable_data["like"]) + 1}})
        return jsonify({"status": 200, "message": "Add like successfully"})
    except Exception as e:
        error_message = str(e)
        return jsonify({"error": error_message}), 500


if __name__ == '__main__':
    app.run(debug=True)
