from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

@app.route("/api/sort", methods=["POST"])
def sort_array():
    data = request.get_json()  # Get JSON data from React
    numbers = data.get("numbers", [])  # Extract numbers array
    sorted_numbers = sorted(numbers)  # Sort the array
    return jsonify({"sorted_numbers": sorted_numbers})  # Send sorted array back

if __name__ == "__main__":
    app.run(debug=True, port=8000)
