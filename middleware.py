
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

def conversation(role = "system", content = "Start the conversation.", temperature = 0.5):

    messages.append(
        {"role": role, "content": content}
    ) 

    try:
        response = get_completion_from_messages(messages, temperature=temperature)

        role = response.choices[0].message.role
        content = response.choices[0].message.content
        #print(role)
        #print(content)

        messages.append(
            {"role": role, "content": content}
        )
        return(role, content, messages)

    except Exception as error:
        print(f"Error: {error}. \nPlease try again")
        print(error)
        # Remove the last user request, since the communication had an error. 
        # The user request needs to be repeated
        messages.pop()

# Describe context
context = [ {'role':'system', 'content':"""
You are OrderBot, an automated service to collect orders for a pizza restaurant. \
You first greet the customer, then collects the order, \
and then asks if it's a pickup or delivery. \
You wait to collect the entire order, then summarize it and check for a final \
time if the customer wants to add anything else. \
If it's a delivery, you ask for an address. \
Finally you collect the payment.\
Make sure to clarify all options, extras and sizes to uniquely \
identify the item from the menu.\
You respond in a short, very conversational friendly style. \
The menu includes \
pepperoni pizza  12.95, 10.00, 7.00 \
cheese pizza   10.95, 9.25, 6.50 \
eggplant pizza   11.95, 9.75, 6.75 \
fries 4.50, 3.50 \
greek salad 7.25 \
Toppings: \
extra cheese 2.00, \
mushrooms 1.50 \
sausage 3.00 \
canadian bacon 3.50 \
AI sauce 1.50 \
peppers 1.00 \
Drinks: \
coke 3.00, 2.00, 1.00 \
sprite 3.00, 2.00, 1.00 \
bottled water 5.00 \
"""} ]

# Setup the context
messeges = []
messages =  context.copy()

"""
Code below for python middleware run on Flask
"""

from flask import Flask, request
import requests
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)
executor = ThreadPoolExecutor()

DEBUG = False

@app.route('/api', methods=['POST'])
def api_handler():
    role = request.form.get('role')
    content = request.form.get('content')

    if role not in ['system', 'user'] or not content:
        return 'Invalid request', 400

    # Process the request asynchronously using ThreadPoolExecutor
    with ThreadPoolExecutor() as executor:
        future = executor.submit(apicall, role, content)
        role, content, messages = future.result()

    # If DEBUG than return also the role and messages object to the user
    # Otherwise return only the content to the user
    if DEBUG:
        return({"role":role, "content":content, "messages": messages})
    else:
        return({"content":content})

def apicall(role, content):

    # Process the request based on role and content
    role, content, messages = conversation(role, content)

    # Return the result
    return role, content, messages

if __name__ == '__main__':
    app.run(threaded=True)
