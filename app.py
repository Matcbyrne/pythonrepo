import os
import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__, template_folder="templates")

# Load API Key
GROQ_API_KEY = os.getenv("gsk_HhY1Blpo7mcOXlsBLCYLWGdyb3FYLcFBGtpGkQIicJ3qcklbF54")
if not GROQ_API_KEY:
    raise ValueError("Error: Please set your GROQ_API_KEY environment variable.")

# ✅ Correct API URL
API_URL = "https://api.groq.com/openai/v1/chat/completions"

def ask_groq(question):
    """ Send user input to Groq API and return the response """
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "mixtral-8x7b-32768",  # Use the correct model name
        "messages": [{"role": "user", "content": question}],
        "temperature": 0.7
    }

    response = requests.post(API_URL, json=data, headers=headers)

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"Error: {response.json()}"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "")
    if not user_input:
        return jsonify({"error": "Message is required"}), 400

    response = ask_groq(user_input)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
