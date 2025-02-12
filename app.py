import os
import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__, template_folder="templates")

# Load API key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("Error: Please set your GROQ_API_KEY environment variable.")

API_URL = "https://api.groq.com/v1/chat/completions"

def ask_groq(question):
    """ Debug API call to Groq """
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "mixtral-8x7b-32768",  # Ensure this model is correct
        "messages": [{"role": "user", "content": question}],
        "temperature": 0.7
    }

    print("📡 Sending request to Groq API...")
    print("Request Data:", data)

    response = requests.post(API_URL, json=data, headers=headers)

    if response.status_code == 200:
        bot_response = response.json()
        print("✅ API Response:", bot_response)  # Debugging output
        return bot_response["choices"][0]["message"]["content"]
    else:
        print("❌ Error Response:", response.json())  # Show error response
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
