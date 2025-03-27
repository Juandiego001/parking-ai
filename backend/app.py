from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from flaskext.mysql import MySQL
import time
from io import BytesIO
from PIL import Image
import cv2
import numpy as np
from detection import detection_YOLO
import detection
from ocr import ocr_placas


app = Flask(__name__)
CORS(app)

# Configurar MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'admin'
app.config['MYSQL_PASSWORD'] = 'admin'
app.config['MYSQL_DB'] = ''
app.config['MYSQL_CURSORCLASS'] = ''

mysql = MySQL(app)

@app.route('/vehicles', methods=["GET"])
def get_vehicles():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * from vehicles")
    vehicles = cur.fetchall()
    return jsonify ({"Vehículos": vehicles})
    

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No se ha enviado un archivo"}), 400
    
    '''
     Etapa para la detección de placas con YOLO
    '''
    archivo = request.files['file']
    image = Image.open(archivo.stream)
    image.thumbnail((1024, 1024))
    frame = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    results = detection.modeloYOLO.predict(frame)[0]
    
    '''
     Etapa para la extracción de placas con OCR
    '''
    image_stream = BytesIO()
    image.save(image_stream, format="PNG")
    image_stream.seek(0)
        
    #* LLamamos función de OCR Azure
    placa_vehiculo = ocr_placas(image_stream)
    placa = placa_vehiculo[0][0][0] # Visualizar la placa del vehiculo para luego comparar con la BD
    placa = placa.replace("-", "")
    
    #* Llamamos función de YOLO
    frame = detection_YOLO(frame, results, placa_vehiculo)
    print(f"Matricula que se lleva al SQL {placa}")
    
    #! Revisar esta parte
    # Convertir frame a BytesIO para enviarlo como respuesta
    _, buffer = cv2.imencode('.jpg', frame)
    image_io = BytesIO(buffer)

    return send_file(image_io, mimetype='image/jpeg')
    
if __name__ == '__main__':
    app.run(debug=True)