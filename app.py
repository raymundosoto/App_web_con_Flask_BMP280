from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route('/datos', methods=['POST'])
def recibir_datos():
    data = request.get_json()
    print("Datos recibidos:", data)
    return jsonify({"mensaje": "Datos recibidos correctamente"})

@app.route('/grafica')
def obtener_datos_grafica():
    # Datos de prueba con el formato del JSON del ESP32
    data = {
        'id_sensor': 'bmp280',
        'timestamp': '2023-12-24 20:28:04',
        'temperatura': 20.65999985,
        'presion': 773.7371826,
        'altitud': 2217.677002
    }
    return jsonify(data)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
