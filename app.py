from flask import Flask, jsonify, request
import random

app = Flask(__name__)

# ✅ Endpoint principal de prueba
@app.route('/')
def home():
    return jsonify({
        "message": "¡API funcionando correctamente en Render!",
        "status": "success"
    })


# ✅ Endpoint para calcular el score crediticio
@app.route('/score', methods=['POST'])
def calcular_score():
    try:
        datos = request.get_json()

        # Obtener los valores del cuerpo JSON
        edad = datos.get("edad", 0)
        gastos = datos.get("gastosmensuales", 0)
        ingresos = datos.get("ingresosmensuales", 0)
        antiguedad = datos.get("antiguedadlaboral", 0)
        ocupacion = datos.get("ocupacion", "").lower()
        estadocivil = datos.get("estadocivil", "").lower()
        monto = datos.get("montosolicitado", 0)
        plazo = datos.get("plazomeses", 0)

        # Validación básica de campos
        if ingresos <= 0 or gastos < 0 or edad <= 0:
            return jsonify({"error": "Datos inválidos o incompletos"}), 400

        # 📊 Cálculo base del score (simulado)
        base = (ingresos - gastos) / (monto / (plazo + 1) + 1)
        base += (antiguedad * 3) + (edad * 0.6)

        # Ajuste por ocupación
        if ocupacion in ["independiente", "freelancer"]:
            base *= 0.9
        elif ocupacion in ["empleado", "profesional"]:
            base *= 1.1

        # Ajuste por estado civil
        if estadocivil in ["casado", "conviviente"]:
            base *= 1.05
        elif estadocivil == "divorciado":
            base *= 0.95

        # Normalización del score entre 1 y 999
        score = int(max(1, min(999, base + random.uniform(-40, 40))))

        # 🧠 Clasificación según el rango de score
        if 877 <= score <= 999:
            categoria = "Excelente Puntaje"
        elif 722 <= score <= 876:
            categoria = "Buen Puntaje"
        elif 598 <= score <= 721:
            categoria = "Puntaje Medio"
        elif 477 <= score <= 597:
            categoria = "Puntaje Bajo"
        else:
            categoria = "Puntaje Muy Bajo"

        # Retornar el resultado
        return jsonify({
            "score": score,
            "categoria": categoria,
            "detalle": {
                "edad": edad,
                "gastosmensuales": gastos,
                "ingresosmensuales": ingresos,
                "antiguedadlaboral": antiguedad,
                "ocupacion": ocupacion,
                "estadocivil": estadocivil,
                "montosolicitado": monto,
                "plazomeses": plazo
            }
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# 🚀 Ejecución local
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
