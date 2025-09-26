from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

BASE_URL = "https://fakerestapi.azurewebsites.net/api/v1/Books"

# Home page
@app.route("/")
def home():
    return render_template("index.html")

# ---------------------------
# 1. Display all books
# ---------------------------
@app.route("/books", methods=["GET"])
def get_books():
    response = requests.get(BASE_URL)
    return jsonify(response.json())

# ---------------------------
# 2. Add a new book
# ---------------------------
@app.route("/books", methods=["POST"])
def add_book():
    data = request.json
    response = requests.post(BASE_URL, json=data)
    return jsonify(response.json())

# ---------------------------
# 3. Update a book
# ---------------------------
@app.route("/books/<int:book_id>", methods=["PUT"])
def update_book(book_id):
    data = request.json
    response = requests.put(f"{BASE_URL}/{book_id}", json=data)
    return jsonify(response.json())

# ---------------------------
# 4. Delete a book
# ---------------------------
@app.route("/books/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    response = requests.delete(f"{BASE_URL}/{book_id}")
    if response.status_code in [200, 204]:
        return jsonify({"message": f"Book {book_id} deleted successfully"})
    else:
        return jsonify({"error": "Failed to delete book"}), response.status_code

if __name__ == "__main__":
    app.run(debug=True)
