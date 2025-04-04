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
        "goalPriorities", "goalType", "goalWeights"
    ]
        
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return jsonify({"error": "Missing fields", "missing": missing_fields}), 400
    
    # response = main(data)
    status,optimalZ, xValues, tableaux  = main(data)
    response = {
        "status":status,
        "optimalZ": optimalZ,
        "xValues": xValues,
        "tableau": tableaux
    }
    return jsonify(response), 200


if __name__ == "__main__":
    app.run(debug=True)
