from flask import Flask, request, session
from concurrent.futures import ThreadPoolExecutor
from api_call_openai import conversation
from contexts import context_pizza

app = Flask(__name__)
app.secret_key = 'super-secret-key'
app.config['PERMANENT_SESSION_LIFETIME'] = 900

executor = ThreadPoolExecutor()

DEBUG = False

@app.route('/', methods=['GET'])
def home():
    return("Welcome to StudyAI")

@app.route('/api/pizza', methods=['POST'])
def api_handler():

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
        return "Invalid request. Either the content was empty or the role was not 'user'", 400

    # Process the request asynchronously using ThreadPoolExecutor
    with ThreadPoolExecutor() as executor:
        future = executor.submit(apicall, messages, role, content)
        messages, role, content = future.result()

    # Save the new messages array in session object
    session["messages"] = messages
    

    # If DEBUG than return also the role and messages object to the user
    # Otherwise return only the content to the user
    if DEBUG:
        return({"role":role, "content":content, "messages": messages})
    else:
        return({"content":content})

def apicall(messages, role, content):

    # Process the request based on role and content
    messages, role, content = conversation(messages, role, content)

    # Return the result
    return messages, role, content

if __name__ == '__main__':
    app.run()
