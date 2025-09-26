from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

BASE_URL = "https://dummyjson.com/todos"

# Home page
@app.route("/")
def home():
    return render_template("index.html")

# ---------------------------
# 1. Display all todos
# ---------------------------
@app.route("/todos", methods=["GET"])
def get_todos():
    response = requests.get(BASE_URL)
    return jsonify(response.json())

# ---------------------------
# 2. Add a new todo
# ---------------------------
@app.route("/todos", methods=["POST"])
def add_todo():
    data = request.json
    response = requests.post(f"{BASE_URL}/add", json=data)
    return jsonify(response.json())

# ---------------------------
# 3. Update a todo
# ---------------------------
@app.route("/todos/<int:todo_id>", methods=["PUT"])
def update_todo(todo_id):
    data = request.json
    response = requests.put(f"{BASE_URL}/{todo_id}", json=data)
    return jsonify(response.json())

# ---------------------------
# 4. Delete a todo
# ---------------------------
@app.route("/todos/<int:todo_id>", methods=["DELETE"])
def delete_todo(todo_id):
    response = requests.delete(f"{BASE_URL}/{todo_id}")
    if response.status_code == 200:
        return jsonify({"message": f"Todo {todo_id} deleted successfully"})
    else:
        return jsonify({"error": "Failed to delete todo"}), response.status_code

if __name__ == "__main__":
    app.run(debug=True)

