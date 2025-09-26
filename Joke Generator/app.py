from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# In-memory storage for favorite jokes
favorite_jokes = []

# Home page
@app.route("/")
def home():
    return render_template("index.html", favorites=favorite_jokes)

# ---------------------------
# 1. Fetch random joke
# ---------------------------
@app.route("/joke", methods=["GET"])
def get_joke():
    response = requests.get("https://official-joke-api.appspot.com/jokes/random")
    return jsonify(response.json())

# ---------------------------
# 2. Add joke to favorites
# ---------------------------
@app.route("/favorites", methods=["POST"])
def add_favorite():
    data = request.json
    if data not in favorite_jokes:
        favorite_jokes.append(data)
    return jsonify({"favorites": favorite_jokes})

# ---------------------------
# 3. Get favorite jokes
# ---------------------------
@app.route("/favorites", methods=["GET"])
def get_favorites():
    return jsonify({"favorites": favorite_jokes})

# ---------------------------
# 4. Remove a joke from favorites
# ---------------------------
@app.route("/favorites/<int:index>", methods=["DELETE"])
def remove_favorite(index):
    if 0 <= index < len(favorite_jokes):
        favorite_jokes.pop(index)
    return jsonify({"favorites": favorite_jokes})

if __name__ == "__main__":
    app.run(debug=True)
