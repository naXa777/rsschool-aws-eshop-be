from flask import Flask, request, Response, stream_with_context
import requests
from os import getenv
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

@app.route('/<service_name>', defaults={'subpath': ''}, methods=['GET', 'POST', 'PUT', 'DELETE'])
@app.route('/<service_name>/', defaults={'subpath': ''}, methods=['GET', 'POST', 'PUT', 'DELETE'])
@app.route('/<service_name>/<path:subpath>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy(service_name, subpath):
    service_url = getenv(service_name)
    if not service_url:
        return Response("Cannot process request", status=502)

    full_url = f"{service_url}/{subpath}?{request.query_string.decode()}"

    response = requests.request(
        method=request.method,
        url=full_url,
        headers={key: value for key, value in request.headers if key != 'Host'},
        data=request.get_data(),
        allow_redirects=False,
        stream=True
    )

    def generate():
        for chunk in response.iter_content(chunk_size=4096):
            yield chunk
    return Response(stream_with_context(generate()), status=response.status_code, content_type=response.headers.get('Content-Type', 'application/json'))

if __name__ == '__main__':
    app.run(debug=True, port=3000)
