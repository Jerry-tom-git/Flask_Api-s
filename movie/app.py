from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

OMDB_KEY = "YOUR_API_KEY"
favorite_movies = []

@app.route("/")
def home():
    return render_template("index.html", favorites=favorite_movies)

# ---------------------------
# 1. Search movie by title
# ---------------------------
@app.route("/search", methods=["GET"])
def search_movie():
    title = request.args.get("title")
    if not title:
        return jsonify({"error": "Title parameter required"}), 400

    url = f"http://www.omdbapi.com/?apikey={OMDB_KEY}&t={title}"
    res = requests.get(url).json()
    if res.get("Response") == "False":
        return jsonify({"error": "Movie not found"}), 404

    movie_data = {
        "title": res.get("Title"),
        "actors": res.get("Actors"),
        "released": res.get("Released"),
        "imdb": res.get("imdbRating"),
        "poster": res.get("Poster")
    }
    return jsonify(movie_data)

# ---------------------------
# 2. Add favorite
# ---------------------------
@app.route("/favorites", methods=["POST"])
def add_favorite():
    data = request.json
    if data not in favorite_movies:
        favorite_movies.append(data)
    return jsonify({"favorites": favorite_movies})

# ---------------------------
# 3. Get favorites
# ---------------------------
@app.route("/favorites", methods=["GET"])
def get_favorites():
    return jsonify({"favorites": favorite_movies})

# ---------------------------
# 4. Delete favorite
# ---------------------------
@app.route("/favorites/<string:title>", methods=["DELETE"])
def delete_favorite(title):
    global favorite_movies
    favorite_movies = [m for m in favorite_movies if m["title"] != title]
    return jsonify({"favorites": favorite_movies})

if __name__ == "__main__":
    app.run(debug=True)
