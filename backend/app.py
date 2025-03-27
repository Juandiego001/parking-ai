from flask import Flask, request, jsonify, send_file, abort
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

# Get all vehicles
@app.route('/vehicles', methods=["GET"])
def get_vehicles():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * from vehicles")
    vehicles = cur.fetchall()
    return jsonify ({"Vehículos": vehicles})

# Get a specific vehicle's information
@app.route('/vehicles/<int:vehicle_id>', methods=['GET'])
def get_vehicle_user(vehicle_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * from vehicles WHERE id="+str(vehicle_id))
    vehicle = cur.fetchall()
    return jsonify({'vehicle': vehicle[0]})

# Add a new user's information
@app.route('/vehicles', methods=['POST'])
def create_info_vehicle():
    if not request.json or not 'plate' in request.json:
        abort(400)
    plate = request.json.get('plate', "")
    apartment_id = request.json.get('apartment_id', "")
    description = request.json.get('description', "")
    status = request.json.get("status", "")
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO vehicles(plate,apartment_id,description,status) VALUES(%s,%s,%s,%s)",(plate,apartment_id,description,status))
    mysql.connection.commit()
    return jsonify({'vehicle': request.json}), 201

# Edit a user's information vehicle
@app.route('/vehicles/<int:vehicle_id>', methods=['PUT'])
def update_book(vehicle_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM vehicles where id="+str(vehicle_id))
    vehicleUser = cur.fetchall()
    print(vehicleUser[0])
    plate = request.json.get('plate', vehicleUser[0]['plate'])
    apartment_id = request.json.get('apartment_id', vehicleUser[0]['apartment_id'])
    description = request.json.get('description', vehicleUser[0]['description'])
    status = request.json.get('status', vehicleUser[0]['status'])
    cur.execute("UPDATE vehicles SET plate =%s, apartment_id =%s ,description= %s,status= %s WHERE id=%s",(plate,apartment_id,description,status,vehicle_id))
    mysql.connection.commit()
    return jsonify({'vehicleUser': vehicleUser[0]})

# Delete a user
@app.route('/vehicles/<int:vehicle_id>', methods=['DELETE'])
def delete_registry(vehicle_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM vehicles WHERE id="+str(vehicle_id))
    mysql.connection.commit()
    return jsonify({'result': True})

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