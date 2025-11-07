from flask import Flask, request, jsonify
import numpy as np
import pickle

app = Flask(__name__)

# Cargar modelo entrenado
with open('modelo_scoring.pkl', 'rb') as f:
    modelo = pickle.load(f)

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "message": "¡API funcionando correctamente en Render!",
        "status": "success"
    })

@app.route('/predict', methods=['POST'])
def predict_score():
    data = request.get_json()

    # Campos esperados
    required_fields = ['edad','gastos_mensuales','ingresos_mensuales',
                       'antiguedad_laboral','ocupacion','estado_civil',
                       'monto_solicitado','plazo_meses']
    
    # Validar campos faltantes
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Faltan campos requeridos"}), 400

    # Convertir los valores
    edad = float(data['edad'])
    gastos = float(data['gastos_mensuales'])
    ingresos = float(data['ingresos_mensuales'])
    antiguedad = float(data['antiguedad_laboral'])
    monto = float(data['monto_solicitado'])
    plazo = float(data['plazo_meses'])

    # Variables derivadas
    tasa = 0.02
    cuota = (monto * tasa) / (1 - (1 + tasa) ** (-plazo))
    RCD = cuota / ingresos
    Monto_Ingreso_Ratio = monto / ingresos
    Anios_Plazo = plazo / 12

    X_input = np.array([[edad, ingresos, gastos, antiguedad,
                         monto, plazo, cuota, RCD, Monto_Ingreso_Ratio, Anios_Plazo]])

    score_pred = modelo.predict(X_input)[0]
    score_pred = int(np.clip(score_pred, 1, 999))

    # Categoría del puntaje
    if score_pred >= 877:
        categoria = "Excelente Puntaje"
    elif score_pred >= 722:
        categoria = "Buen Puntaje"
    elif score_pred >= 598:
        categoria = "Puntaje Medio"
    elif score_pred >= 477:
        categoria = "Puntaje Bajo"
    else:
        categoria = "Puntaje Muy Bajo"

    return jsonify({
        "score": score_pred,
        "categoria": categoria
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
