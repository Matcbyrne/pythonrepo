import os
from pydantic import BaseModel, Field
from typing import List
from groq import Groq
import instructor

class Character(BaseModel):
    name: str
    facts: List[str] = Field(..., description="A list of facts about the subject")

def get_groq_response(subject: str):
    # Initialize Groq client with API key
    client = Groq(
        api_key=os.environ.get('GROQ_API_KEY'),
    )

    # Enable instructor integration
    client = instructor.from_groq(client, mode=instructor.Mode.TOOLS)

    # Make the API call
    resp = client.chat.completions.create(
        model="mixtral-8x7b-32768",
        messages=[
            {
                "role": "user",
                "content": f"Tell me about {subject}",
            }
        ],
        response_model=Character,
    )
    return resp

def main():
    # Make sure GROQ_API_KEY is set
    if not os.environ.get('GROQ_API_KEY'):
        print("Please set your GROQ_API_KEY environment variable")
        return

    # Get input from user
    subject = input("What would you like to learn about? ")
    
    try:
        response = get_groq_response(subject)
        print("\nResults:")
        print(response.model_dump_json(indent=2))
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
