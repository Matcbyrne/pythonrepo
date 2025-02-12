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
    groq_client = Groq(
        api_key=os.environ.get(
            os.environ.get("GROQ_API_KEY"),
        ),
    )

    groq_client = instructor.from_groq(groq_client, mode=instructor.Mode.TOOLS)

    response = groq_client.chat.completions.create(
        model="mixtral-8x7b-32768",
        messages=[
            {
                "role": "user",
                "content": f"Tell me about {topic}",
            }
        ],
        response_model=TopicInfo,
    )
    print(response.model_dump_json(indent=2))

if __name__ == "__main__":
    while True:
        user_topic = get_topic_from_user()
        if user_topic.lower() == 'exit':
            break
        fetch_topic_details(user_topic)
