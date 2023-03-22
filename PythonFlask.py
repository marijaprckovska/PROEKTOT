import sqlite3
import pymongo
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/companies", methods = ["GET"])
def read_companies():
    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    c.execute("SELECT * FROM companies LIMIT 5")
    companies = []
    for row in c.fetchall():
        company = {
            "id": row[0],
            "name": row[1],
            "country_iso": row[2],
            "city": row[3],
            "nace": row[4],
            "website": row[5]
        }
        companies.append(company)
    c.close()
    conn.close()
    return jsonify({"companies": companies})

@app.route("/companies", methods=["POST"])
def add_company():
    conn = pymongo.MongoClient()
    db = conn["mongodata"]
    collection = db["cleanedCompanies"]
    data = request.get_json()
    result = collection.insert_one(data)

    if result.inserted_id:
        return jsonify({"success": True}), 201
    else:
        return jsonify({"success": False}), 400


if __name__ == "__main__":
    app.run(debug=True)