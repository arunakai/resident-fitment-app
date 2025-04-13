from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import pickle

# Load your trained ML model from the .pkl file
with open("fitment_model.pkl", "rb") as f:
    model = pickle.load(f)

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Health check route (optional)
@app.route('/')
def home():
    return "✅ Fitment Prediction API is running."

# Prediction endpoint
@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        features = np.array(data["features"]).reshape(1, -1)

        # Predict fitment score
        score = model.predict_proba(features)[0][1]
        label = "potential fit" if score >= 0.5 else "potential misfit"

        return jsonify({
            "message": f"This applicant is a {label} and the fitment score is {score:.2f}"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run the Flask app
if __name__ == "__main__":
    app.run(port=5000)
