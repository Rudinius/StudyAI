import os
from openai import OpenAI

# Get API key from environment variables
# Set the API key
API_KEY = os.environ.get('STUDYAI_API_KEY')
client = OpenAI(api_key=API_KEY)

def get_completion_from_messages(messages, temperature, model="gpt-3.5-turbo"):
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
    )
    return response

def conversation(messages, role = "system", content = "Start the conversation.", temperature = 0.5):

    try:

        # Append new user or system message to message stack
        messages.append({"role": role, "content": content})
        
        response = get_completion_from_messages(messages, temperature)

        role = response.choices[0].message.role
        content = response.choices[0].message.content

        # Append new answer of assistant to message stack
        messages.append({"role": role, "content": content})
        
        return(messages, role.capitalize(), content)

    except Exception as error:
        # Remove the last message from the message stack if an error has been thrown by openai API
        # If the error was thrown by openai API, the last message on the stack is the user or system message
        messages.pop()
        # reraise an exception for passing it further down
        raise
