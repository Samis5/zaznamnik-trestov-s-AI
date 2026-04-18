from flask import Flask, jsonify, request
from flask_cors import CORS
from groq import Groq
import json

app = Flask(__name__)
CORS(app)

# Zadaj sem platný API kľúč
client = Groq(api_key="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")

# Načítanie dát s UTF-8
with open("data.json", encoding="utf-8") as f:
    data = json.load(f)

@app.route("/students")
def students():
    return jsonify(data["students"])

@app.route("/chat", methods=["POST"])
def chat():
    try:
        body = request.json
        msg = body["message"]
        sid = int(body["id"])

        student = next(p for p in data["students"] if p["id"] == sid)

        prompt = f"""
Ja som {student['name']}. Mám {student['age']} rokov a chcem ti úprimne povedať, ako som sa dostala do väzenia.

Otázka: {msg}
"""
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",  # Použi odporúčaný model
            messages=[{"role": "user", "content": prompt}]
        )

        return jsonify({
            "reply": response.choices[0].message.content
        })

    except Exception as e:
        print("AI ERROR:", e)
        return jsonify({
            "reply": str(e)
        })

if __name__ == "__main__":
    print("Backend beží na http://127.0.0.1:5000")
    app.run(debug=True)
