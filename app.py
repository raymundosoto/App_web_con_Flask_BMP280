
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

datos_recibidos = []

@app.route('/datos', methods=['POST'])
def recibir_datos():
    data = request.get_json()
    print("Datos recibidos:", data)

    datos_recibidos.append(data)  # Agregar los datos al registro

    return jsonify({"mensaje": "Datos recibidos correctamente"})

@app.route('/grafica')
def obtener_datos_grafica():
    # Obtener los últimos datos enviados desde el ESP32
    if datos_recibidos:
        ultimo_dato = datos_recibidos[-1]
        return jsonify(ultimo_dato)
    else:
        return jsonify({})

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
