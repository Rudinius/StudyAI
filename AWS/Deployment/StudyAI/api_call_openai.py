
"""
Code below for setting up the context of the chatbot and connecting to openai API.
"""

import openai

# Set the API key
API_KEY = "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"
openai.api_key  = API_KEY

def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature, # this is the degree of randomness of the model's output
    )
    #print(str(response.choices[0].message))
    return response

def conversation(messages, role = "system", content = "Start the conversation.", temperature = 0.5):

    try:

        # Append new user or system message to message stack
        messages.append({"role": role, "content": content})
        
        response = get_completion_from_messages(messages, temperature=temperature)

        role = response.choices[0].message.role
        content = response.choices[0].message.content

        # Append new answer of assistant to message stack
        messages.append({"role": role, "content": content})
        
        return(messages, role, content)

    except Exception as error:
        # Remove the last message from the message stack if an error has been thrown by openai API
        # If the error was thrown by openai API, the last message on the stack is the user or system message
        messages.pop()
        return(
            messages,
            role,
            "I am sorry. Your last message lead to an error and has not been transmitted. Please try again. "
            "Should this happen again, please contact the admin. "
            f"The error code is: {error}")
