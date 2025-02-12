import os
import requests
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS  # Add this import

app = Flask(__name__, template_folder="templates")
CORS(app)  # Enable CORS for all routes

# Load API Key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    print("Warning: GROQ_API_KEY not set. Please set it before making API calls.")
    GROQ_API_KEY = None

API_URL = "https://api.groq.com/v1/chat/completions"

def ask_groq(question):
    """ Send user input to Groq API and return the response """
    if not GROQ_API_KEY:
        return "Error: GROQ_API_KEY not set"
        
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "mixtral-8x7b-32768",
        "messages": [{"role": "user", "content": question}],
        "temperature": 0.7
    }

    try:
        response = requests.post(API_URL, json=data, headers=headers)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as e:
        return f"Error: {str(e)}"

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
    # Get port from environment variable or default to 5000
    port = int(os.environ.get("PORT", 5000))
    
    # Run the app
    app.run(host="0.0.0.0", port=port, debug=False)  # Set debug=False for production
