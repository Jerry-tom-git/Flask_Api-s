from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# In-memory storage for last 5 conversions
conversion_history = []

# Home page
@app.route("/")
def home():
    return render_template("index.html", history=conversion_history)

# ---------------------------
# Fetch conversion
# ---------------------------
@app.route("/convert", methods=["POST"])
def convert_currency():
    data = request.json
    amount = float(data.get("amount", 0))
    from_currency = data.get("from")
    to_currency = data.get("to")

    # Fetch exchange rates
    url = f"https://api.exchangerate.host/latest?base={from_currency}&symbols={to_currency}"
    res = requests.get(url).json()
    rate = res["rates"].get(to_currency)

    if rate is None:
        return jsonify({"error": "Invalid currency code"}), 400

    converted = round(amount * rate, 2)

    # Save to history
    conversion_entry = {
        "amount": amount,
        "from": from_currency,
        "to": to_currency,
        "converted": converted
    }
    conversion_history.insert(0, conversion_entry)
    if len(conversion_history) > 5:
        conversion_history.pop()

    return jsonify(conversion_entry)

# ---------------------------
# Get history
# ---------------------------
@app.route("/history", methods=["GET"])
def get_history():
    return jsonify(conversion_history)

if __name__ == "__main__":
    app.run(debug=True)
