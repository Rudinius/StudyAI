from flask import Flask, request
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)
executor = ThreadPoolExecutor()

@app.route('/api', methods=['POST'])
def api_handler():
    role = request.form.get('role')
    content = request.form.get('content')

    if role not in ['system', 'user'] or not content:
        return 'Invalid request', 400

    # Process the request asynchronously
    executor.submit(apicall, role, content)

    return 'Request received and queued for processing', 200

def apicall(role, content):
    # Process the request here based on role and content
    # Replace this with your actual logic
    print(f'Processing request with role: {role} and content: {content}')

if __name__ == '__main__':
    app.run(threaded=True)
