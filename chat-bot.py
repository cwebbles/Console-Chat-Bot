import os
import requests
from dotenv import load_dotenv

load_dotenv()

def main():
    print("Hello, I am a chat bot. How can I help you today?\nAsk me anything! Press Q to quit.")

    cont = True

    while cont:
        user_input = input("You: ")

        if user_input == "Q":
            cont = False
            break

        # Send user input to AWS Lambda
        response = chat(user_input)

        # Print response
        print("Bot: " + response)


def chat(message):
    api = os.getenv('CHAT_ENDPOINT')

    # Send user input to AWS Lambda
    headers = {
        'Content-Type': 'application/json'
    }

    try:
        response = requests.post(api, headers=headers, json={"message": message})
        response.raise_for_status()
        return response.json().response # This returns response generated by chat
    except requests.exceptions.HTTPError as e:
        print(e)
        return None

main()