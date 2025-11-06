from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        "status": "success",
        "message": "¡API funcionando correctamente en Render!"
    })

@app.route('/saludo/<nombre>')
def saludo(nombre):
    return jsonify({
        "saludo": f"Hola, {nombre}! Bienvenido a mi API."
    })

if __name__ == '__main__':
    # host 0.0.0.0 permite acceso externo en Render
    app.run(host='0.0.0.0', port=5000)
