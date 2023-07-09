from flask import Flask, request, session, render_template
from concurrent.futures import ThreadPoolExecutor
from api_call_openai import conversation
from context import contexts
#from context import delivery

app = Flask(__name__)
app.secret_key = 'super-secret-key'
app.config['PERMANENT_SESSION_LIFETIME'] = 900

executor = ThreadPoolExecutor()

@app.route('/', methods=['GET'])
def home():
    return render_template("home.html")

@app.route('/api/v1/pizza', methods=['POST'])
def pizza_handler_v1():

    # Pass the get_context_pizza function to handler
    return handler(contexts.get_context_pizza)

@app.route('/api/v1/delivery', methods=['POST'])
def delivery_handler_v1():

    # Pass the get_context_delivery function to handler
    return handler(contexts.get_context_delivery)

def handler(get_context):

    # Get request data
    role = request.form.get('role')
    content = request.form.get('content')
    language = request.form.get('language')

    # First call, session is empty
    if not session:
        print("First call")
        # There is no existing session.
        # Set messages to the context
        # Call the passed function to receive context in given language
        messages =  get_context(language)

    # Consecutive call, session is not empty
    else:
        print("Consecutive call")
        # There is an existing session.
        # Retrieve the messages from that session
        messages = session.get("messages")


    # In order to protect from setting different system messages,
    # only requests with role 'user' are allowed
    if role not in ['user'] or not content:
        response = {"content": "Website: Invalid request. Either the content was empty or the role was not 'user'"}
        return response, 400

    # insert into try catch block
    # Process the request asynchronously using ThreadPoolExecutor
    with ThreadPoolExecutor() as executor:
        future = executor.submit(apicall, messages, role, content, language)
        messages, role, content = future.result()

    # Save the new messages array in session object
    session["messages"] = messages

    response = {"content": f"{role}: {content}"}
    
    return response, 200
    
    # catch
    # return 400

def apicall(messages, role, content, language):

    # Process the request based on role and content
    messages, role, content = conversation(messages, role, content)

    # Return the result
    return messages, role, content

if __name__ == '__main__':
    app.run()
