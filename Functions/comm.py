from flask import Flask, request, jsonify
from flask_cors import CORS
from mainCOMM import main

app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

@app.route("/process-data", methods=["POST"])
def process_data():
    data = request.get_json()

    required_fields = [
        "problemType", "objectiveCoefficients", "objectiveType", "technique",
        "constraints", "goals", "unrestrictedVariables",
        "goalPriorityType", "goalPriorities", "goalWeights"
    ]
    
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return jsonify({"error": "Missing fields", "missing": missing_fields}), 400
    
    # response = main(data)
    main(data)
    response = {
        "message": "Approval granted",
        "status": "approved",
        "receivedData": data
    }
    return jsonify(response), 200


if __name__ == "__main__":
    app.run(debug=True)
