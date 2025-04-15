# from flask import Flask, request, jsonify
# import joblib
# import os

# app = Flask(__name__)

# # Load model
# model_path = os.path.join(os.path.dirname(__file__), 'lightgbm_fraud_model.pkl')
# print("Loading model from:", model_path)
# model = joblib.load(model_path)

# # Mapping for 'type' feature
# type_mapping = {
#     "CASH_OUT": 0,
#     "TRANSFER": 1,
#     "DEBIT": 2,
#     "PAYMENT": 3,
#     "CASH_IN": 4
# }

# @app.route('/predict', methods=['POST'])
# def predict():
#     try:
#         data = request.get_json()

#         # Map 'type' to numeric
#         type_str = data.get('type')
#         if type_str not in type_mapping:
#             return jsonify({'error': f"Invalid 'type': {type_str}"}), 400

#         type_val = type_mapping[type_str]

#         input_data = [[
#             type_val,
#             float(data['amount']),
#             float(data['oldbalanceOrg']),
#             float(data['newbalanceOrig']),
#             float(data['oldbalanceDest']),
#             float(data['newbalanceDest'])
#         ]]

#         # Predict
#         prediction = model.predict(input_data)[0]
#         result = "Fraud" if prediction == 1 else "Not Fraud"

#         return jsonify({'prediction': result})

#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# if __name__ == '__main__':
#     app.run(debug=True)

from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load model
model_path = os.path.join(os.path.dirname(__file__), 'lightgbm_fraud_model.pkl')
model = joblib.load(model_path)

# Mapping for 'type' feature
type_mapping = {
    "CASH_OUT": 0,
    "TRANSFER": 1,
    "DEBIT": 2,
    "PAYMENT": 3,
    "CASH_IN": 4
}

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()

        # Map 'type' to numeric
        type_str = data.get('type')
        if type_str not in type_mapping:
            return jsonify({'error': f"Invalid 'type': {type_str}"}), 400

        type_val = type_mapping[type_str]

        input_data = [[
            type_val,
            float(data['amount']),
            float(data['oldbalanceOrg']),
            float(data['newbalanceOrig']),
            float(data['oldbalanceDest']),
            float(data['newbalanceDest'])
        ]]  # Ensure data format is valid for the model

        # Predict
        prediction = model.predict(input_data)[0]
        result = "Fraud" if prediction == 1 else "Not Fraud"

        return jsonify({'prediction': result})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
