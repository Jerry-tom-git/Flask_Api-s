from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

BASE_URL = "https://reqres.in/api/users"

# Home page
@app.route("/")
def home():
    return render_template("index.html")

# Fetch all users
@app.route("/users", methods=["GET"])
def get_users():
    response = requests.get(BASE_URL)
    return jsonify(response.json())

# Add a new user
@app.route("/users", methods=["POST"])
def add_user():
    data = request.json
    response = requests.post(BASE_URL, json=data)
    return jsonify(response.json())

# Update user details
@app.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.json
    response = requests.put(f"{BASE_URL}/{user_id}", json=data)
    return jsonify(response.json())

# Delete a user
@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    response = requests.delete(f"{BASE_URL}/{user_id}")
    if response.status_code == 204:
        return jsonify({"message": f"User {user_id} deleted successfully"})
    else:
        return jsonify({"error": "Failed to delete user"}), response.status_code

if __name__ == "__main__":
    app.run(debug=True)
