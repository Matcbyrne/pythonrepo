import os
from groq import Groq

def main():
    # Initialize Groq client with API key
    client = Groq(
        api_key=os.environ.get('GROQ_API_KEY'),
    )
    
    print("Welcome to Groq Chat! Type 'quit' to exit.")
    
    while True:
        # Get user input
        question = input("\nYou: ").strip()
        
        # Check for quit command
        if question.lower() == 'quit':
            print("Goodbye!")
            break
        
        try:
            # Make API call to Groq
            response = client.chat.completions.create(
                model="mixtral-8x7b-32768",
                messages=[
                    {
                        "role": "user",
                        "content": question,
                    }
                ],
            )
            
            # Print the response
            print(f"\nGroq: {response.choices[0].message.content}")
            
        except Exception as e:
            print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
