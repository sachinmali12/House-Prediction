from flask import Flask, render_template, request, jsonify
import pickle
import pandas as pd
import numpy as np
import os

app = Flask(__name__)

# Load model
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "house_price_model.pkl")

model = pickle.load(open(MODEL_PATH, "rb"))

def format_price(price):
    if price >= 10000000:
        return f"{round(price/10000000, 2)} Cr"
    else:
        return f"{round(price/100000, 2)} Lakh"

def predict_price(data):
    df = pd.DataFrame([data])

    # Feature Engineering
    df['total_rooms'] = df['bedrooms'] + df['bathrooms']
    df['area_bedrooms'] = df['area'] * df['bedrooms']
    df['is_luxury'] = (df['area'] > 4000).astype(int)

    pred_log = model.predict(df)
    price = np.exp(pred_log)[0]

    return format_price(price)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json

        # Convert numeric fields
        numeric_fields = [
            'area','bedrooms','bathrooms','stories','parking',
            'mainroad','guestroom','basement',
            'hotwaterheating','airconditioning','prefarea'
        ]

        for field in numeric_fields:
            data[field] = int(data[field])

        result = predict_price(data)

        return jsonify({"price": result})

    except Exception as e:
        return jsonify({"error": str(e)})


if __name__ == '__main__':
    app.run(debug=True)