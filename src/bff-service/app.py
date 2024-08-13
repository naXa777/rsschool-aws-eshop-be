from flask import Flask, request, Response, stream_with_context
import requests
from os import getenv
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

@app.route('/<service_name>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy(service_name):
    service_url = getenv(service_name)
    if not service_url:
        return Response("Cannot process request", status=502)

    full_url = f"{service_url}?{request.query_string.decode()}"
    response = requests.get(full_url, stream=True)

    def generate():
        for chunk in response.iter_content(chunk_size=4096):
            yield chunk
    return Response(stream_with_context(generate()), status=response.status_code, content_type=response.headers['Content-Type'])

if __name__ == '__main__':
    app.run(debug=True, port=3000)
