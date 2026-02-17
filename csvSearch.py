import pandas as pd
from flask import Flask, request, jsonify, send_file

# Stores the 2 values users may sort by
class Criteria_Class:
    def __init__(self, country, compNum):
        self.country = country
        self.compNum = compNum

    def getCountry(self):
        return self.country
    def getCompNum(self):
        return self.compNum

    def setCountry(self, country):
        self.country = country
    def setCompNum(self, compNum):
        self.compNum = compNum

# Check against the CSV if a comp number is taken
class Checker:
    def __init__(self):
        # Load once on startup
        self.df = pd.read_csv("OGN.csv")

    # Check if the comp number exists in that country
    def check_for_cn(self, criteria):
        # Normalize to string for robust matching
        country = str(criteria.getCountry()).strip()
        target_cn = str(criteria.getCompNum()).strip()

        # Filter by country
        df = self.df.copy()
        # Ensure string types for comparison
        df["COUNTRY"] = df["COUNTRY"].astype(str)
        df["CN"] = df["CN"].astype(str)

        # Case-insensitive compare for country and exact match for CN
        filtered = df[df["COUNTRY"].str.lower() == country.lower()]
        if filtered.empty:
            return False
        return any(filtered["CN"] == target_cn)

    def UI(self, cn, country):
        criteria = Criteria_Class(country, cn)
        return self.check_for_cn(criteria)

# --- Flask Web App ---
app = Flask(__name__)
checker = Checker()


@app.route("/")
def home():
    # Serve the frontend HTML
    return send_file("home.html")


@app.route("/home.js")
def home_js():
    return send_file("home.js")


@app.route("/check", methods=["POST"])
def check_endpoint():
    try:
        data = request.get_json(force=True, silent=True) or {}
        comp_num = data.get("compNum", "")
        country = data.get("country", "")
        if comp_num is None or country is None:
            return jsonify({"error": "Missing compNum or country"}), 400
        taken = checker.UI(comp_num, country)
        return jsonify({"taken": bool(taken)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    # Run the web server
    app.run(host="127.0.0.1", port=5000, debug=True)


