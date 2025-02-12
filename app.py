from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "Groq Chatbot is running!"

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "")
    if not user_input:
        return jsonify({"error": "Message is required"}), 400

    # Simulating a response from Groq (Replace with real API logic)
    response = {"response": f"Groq says: '{user_input}'"}
    return jsonify(response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

from flask import render_template

@app.route("/ui")
def ui():
    return render_template("index.html")

