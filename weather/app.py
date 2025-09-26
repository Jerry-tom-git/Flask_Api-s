from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# In-memory storage for favorite cities
favorite_cities = []

# Home page
@app.route("/")
def home():
    return render_template("index.html", favorites=favorite_cities)

# ---------------------------
# Fetch weather data
# ---------------------------
@app.route("/weather", methods=["GET"])
def get_weather():
    city = request.args.get("city")
    if not city:
        return jsonify({"error": "City parameter is required"}), 400

    # Get city coordinates using Open-Meteo Geocoding API
    geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}"
    geo_res = requests.get(geo_url).json()
    if "results" not in geo_res or not geo_res["results"]:
        return jsonify({"error": "City not found"}), 404

    lat = geo_res["results"][0]["latitude"]
    lon = geo_res["results"][0]["longitude"]

    # Fetch weather using Open-Meteo API
    weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    weather_res = requests.get(weather_url).json()

    current = weather_res.get("current_weather", {})
    return jsonify({
        "city": city,
        "temperature": current.get("temperature"),
        "windspeed": current.get("windspeed"),
        "weathercode": current.get("weathercode")
    })

# ---------------------------
# Add favorite city
# ---------------------------
@app.route("/favorites", methods=["POST"])
def add_favorite():
    data = request.json
    city = data.get("city")
    if city and city not in favorite_cities:
        favorite_cities.append(city)
    return jsonify({"favorites": favorite_cities})

# ---------------------------
# Delete favorite city
# ---------------------------
@app.route("/favorites/<string:city>", methods=["DELETE"])
def delete_favorite(city):
    if city in favorite_cities:
        favorite_cities.remove(city)
    return jsonify({"favorites": favorite_cities})

if __name__ == "__main__":
    app.run(debug=True)
