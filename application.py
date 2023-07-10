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

    supported_roles = ['user']
    supported_languages = ['English', 'German', 'French', 'Spanish']

    try:

        # Get request data
        role = request.form.get('role')
        content = request.form.get('content')
        language = request.form.get('language')

        # Check if the payload is correct

        # Empty content is not allowed
        if not content:
            response = {"content": "Error: Invalid request. Content is empty."}
            return response, 400

        # In order to protect from setting different system messages,
        # only certain roles are allowed
        if role not in supported_roles:
            response = {"content": "Error: Invalid request. Not supported role. Only 'user' is allowed."}
            return response, 400

        # Limit the possible languages
        if language not in supported_languages:
            response = {"content": "Error: Invalid request. Not supported language. Only 'English', 'German', 'French', 'Spanish' is allowed."}
            return response, 400

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

        # insert into try catch block
        # Process the request asynchronously using ThreadPoolExecutor
        with ThreadPoolExecutor() as executor:
            future = executor.submit(apicall, messages, role, content)
            messages, role, content = future.result()

        # Save the new messages array in session object
        session["messages"] = messages

        response = {"content": f"{role}: {content}"}
        
        return response, 200

    # Catch errors and return error code
    except Exception as error:
        print(error)
        return "Sorry! Something went wrong.", 500


def apicall(messages, role, content):

    # Process the request based on role and content
    messages, role, content = conversation(messages, role, content)

    # Return the result
    return messages, role, content

if __name__ == '__main__':
    app.run()
