from flask import Flask, jsonify
import requests

app = Flask(__name__)

@app.route("/api/forward")
def forward_request():
    try:
        backend_response = requests.get("http://backend-service:5000/api/data")
        backend_json = backend_response.json()
        return jsonify(backend_json)
    except Exception as e:
        return jsonify(error=str(e)), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

