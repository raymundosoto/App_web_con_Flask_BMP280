from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

temperaturas = []
presiones = []

@app.route('/datos', methods=['POST'])
def recibir_datos():
    data = request.get_json()
    print("Datos recibidos:", data)
    
    temperatura = data.get('temperatura')
    presion = data.get('presion')

    # Guardar datos para la gráfica
    if temperatura is not None and presion is not None:
        temperaturas.append(temperatura)
        presiones.append(presion)

    return jsonify({"mensaje": "Datos recibidos correctamente"})

@app.route('/grafica')
def obtener_datos_grafica():
    # Aquí puedes proporcionar los datos almacenados en temperaturas y presiones
    # En este ejemplo, se devuelven los últimos 10 valores de temperatura y presión
    datos_grafica = {
        "temperatura": temperaturas[-10:],
        "presion": presiones[-10:]
    }
    return jsonify(datos_grafica)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
