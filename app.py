from flask import Flask, request, jsonify, render_template
import json

app = Flask(__name__)

temperaturas = []
presiones = []
altitudes = []

@app.route('/datos', methods=['POST'])
def recibir_datos():
    data = request.get_json()
    print("Datos recibidos:", data)
    
    id_sensor = data['id_sensor']
    timestamp = data['timestamp']
    temperatura = data['temperatura']
    presion = data['presion']
    altitud = data['altitud']

    # Guardar datos para la gráfica
    temperaturas.append(temperatura)
    presiones.append(presion)
    altitudes.append(altitud)

    return jsonify({"mensaje": "Datos recibidos correctamente"})

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
