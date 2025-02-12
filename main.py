from flask import Flask, request, render_template, jsonify
import os

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")  # Loads the chat UI

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "")
    if not user_input:
        return jsonify({"error": "Message is required"}), 400

    # Simulating a response from Groq (Replace this with actual API logic)
    response = {"response": f"Groq says: '{user_input}'"}
    return jsonify(response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
