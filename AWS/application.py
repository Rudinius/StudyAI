from flask import Flask, request, session, render_template
from concurrent.futures import ThreadPoolExecutor
from api_call_openai import conversation
from contexts import context_pizza

app = Flask(__name__)
app.secret_key = 'super-secret-key'
app.config['PERMANENT_SESSION_LIFETIME'] = 900

executor = ThreadPoolExecutor()

@app.route('/', methods=['GET'])
def home():
    return render_template("home.html")

@app.route('/api/v1/pizza', methods=['POST'])
def pizza_handler_v1():

    # First call, session is empty
    if not session:
        print("First call")
        # There is no existing session.
        # Set messages to the context
        messages =  context_pizza.copy()
        
    # Consecutive call, session is not empty
    else:
        print("Consecutive call")
        # There is an existing session.
        # Retrieve the messages from that session
        messages = session.get("messages")
    
    role = request.form.get('role')
    content = request.form.get('content')

    # In order to protect from setting different system messages,
    # only requests with role 'user' are allowed
    if role not in ['user'] or not content:
        response = {"content": "Website: Invalid request. Either the content was empty or the role was not 'user'"}
        return response, 400

    # Process the request asynchronously using ThreadPoolExecutor
    with ThreadPoolExecutor() as executor:
        future = executor.submit(apicall, messages, role, content)
        messages, role, content = future.result()

    # Save the new messages array in session object
    session["messages"] = messages

    response = {"content": f"{role}: {content}"}
    
    return response, 200

def apicall(messages, role, content):

    # Process the request based on role and content
    messages, role, content = conversation(messages, role, content)

    # Return the result
    return messages, role, content

if __name__ == '__main__':
    app.run()
