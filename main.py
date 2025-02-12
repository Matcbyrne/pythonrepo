import os
import requests

# Ensure GROQ_API_KEY is set
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    print("Error: Please set your GROQ_API_KEY environment variable.")
    exit(1)

API_URL = "https://api.groq.com/v1/chat/completions"

def ask_groq(question):
    """ Send a question to Groq API and return the response. """
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "mixtral-8x7b-32768",  # Change model if needed
        "messages": [{"role": "user", "content": question}],
        "temperature": 0.7
    }

    response = requests.post(API_URL, json=data, headers=headers)
    
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"Error: {response.json()}"

# Run chatbot loop
print("Welcome to Groq Chat! Type 'quit' to exit.")
while True:
    user_input = input("You: ")
    if user_input.lower() == "quit":
        break

    response = ask_groq(user_input)
    print(f"Groq: {response}")
