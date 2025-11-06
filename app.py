from flask import Flask, request, jsonify
import pickle
import numpy as np

app = Flask(__name__)

with open('modelo.pkl', 'rb') as f:
    model = pickle.load(f)

@app.route('/')
def home():
    return "API de Scoring funcionando 🚀"

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    features = np.array([
        data['edad'],
        data['ingresos_mensual'],
        data['gastos_mensual'],
        data['antiguedad_laboral'],
        data['num_referencias'],
        data['cuota_mensual'],
        data['rcd'],
        data['monto_ingreso_ratio']
    ]).reshape(1, -1)
    prob = model.predict_proba(features)[0][1]
    score = int((1 - prob) * 999)
    return jsonify({
        "probabilidad_incumplimiento": round(prob, 3),
        "score": score,
        "riesgo": "ALTO" if score < 400 else "BAJO"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
