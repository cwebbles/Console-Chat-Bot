
# Start program

# Wait for user input

# Read user input and send to AWS Lambda

# Get response from AWS Lambda

# Print response

def main():
    print("Hello, I am a chat bot. How can I help you today?\nAsk me anything! Press Q to quit.")

    cont = True

    while cont:
        user_input = input("You: ")

        if user_input == "Q":
            cont = False
            break

        # Send user input to AWS Lambda

        # Get response from AWS Lambda

        # Print response
