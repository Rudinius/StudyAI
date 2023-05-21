from flask import Flask, request, jsonify, make_response
from concurrent.futures import ThreadPoolExecutor

import openai
API_KEY = "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"
openai.api_key  = API_KEY

app = Flask(__name__)
executor = ThreadPoolExecutor()

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
        return(role, content)

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

@app.route('/api', methods=['POST'])
async def api_handler():
    role = request.form.get('role')
    content = request.form.get('content')

    if role not in ['system', 'user'] or not content:
        return 'Invalid request', 400

    # Process the request asynchronously
    #future = executor.submit(apicall, role, content)
    #future.add_done_callback(handle_result)
    response = await executor.submit(apicall, role, content)
    print(response)
    return(response)

    #return 'Request received and queued for processing', 200

def apicall(role, content):
    # Process the request based on role and content
    role, content = conversation(role, content)

    # Return the result
    return jsonify({'role': role, 'content': content})

if __name__ == '__main__':
    app.run(threaded=True)
