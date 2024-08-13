from flask import Flask, request, jsonify
import requests
from os import getenv
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

@app.route('/<service_name>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy(service_name):
    # Fetch the service URL from the environment variables
    service_url = getenv(service_name)

    if not service_url:
        return jsonify({"error": "Cannot process request"}), 502

    # Append the original query string to the service URL
    full_url = f"{service_url}?{request.query_string.decode()}"

    # Forward the request to the actual service
    response = requests.request(
        method=request.method,
        url=full_url,
        headers={key: value for key, value in request.headers if key != 'Host'},
        data=request.get_data(),
        allow_redirects=False)

    # Return the response received from the service
    return (response.content, response.status_code, response.headers.items())

if __name__ == '__main__':
    app.run(debug=True, port=3000)
