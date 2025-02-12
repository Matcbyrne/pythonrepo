import os
from pydantic import BaseModel, Field
from typing import List
from groq import Groq
import instructor

class TopicInfo(BaseModel):
    title: str
    details: List[str] = Field(..., description="A list of details about the topic")

def get_topic_from_user():
    return input("Enter a topic to learn about (or 'exit' to quit): ")

def fetch_topic_details(topic):
    api_key = os.environ.get("GROQ_API_KEY")

    # Debugging step: Print the API key (remove in production)
    if api_key is None:
        print("Error: The GROQ_API_KEY environment variable is not set.")
        print("Make sure to set it using 'export GROQ_API_KEY=your_api_key_here' or 'set GROQ_API_KEY=your_api_key_here' for Windows.")
        return

    groq_client = Groq(api_key=api_key)
    groq_client = instructor.from_groq(groq_client, mode=instructor.Mode.TOOLS)

    response = groq_client.chat.completions.create(
        model="mixtral-8x7b-32768",
        messages=[{"role": "user", "content": f"Tell me about {topic}"}],
        response_model=TopicInfo,
    )
    print(response.model_dump_json(indent=2))

if __name__ == "__main__":
    while True:
        user_topic = get_topic_from_user()
        if user_topic.lower() == 'exit':
            break
        fetch_topic_details(user_topic)
