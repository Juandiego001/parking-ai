from flask import Flask, request, jsonify, send_file, abort
from flask_cors import CORS
# from flaskext.mysql import MySQL
# from flask_mysqldb import MySQL
import pymysql  # Libreria de python para interactuar con BD, me sirvió, con las de flask no
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

def DB_config():
    return pymysql.connect(
        host="localhost",
        user="lfmb0",
        password="admin_pass",
        database="parking",
        port=3306,
        cursorclass=pymysql.cursors.DictCursor
    )

# * Get all vehicles
@app.route('/vehicles', methods=["GET"])
def get_vehicles():
    cur = DB_config()
    cur = cur.cursor()
    cur.execute("SELECT * from vehicles")
    vehicles = cur.fetchall()
    return jsonify ({"Vehículos": vehicles})

# * Get a specific vehicle's information
@app.route('/vehicles/<int:vehicle_id>', methods=['GET'])
def get_vehicle_user(vehicle_id):
    cur = DB_config()
    cur = cur.cursor()
    cur.execute("SELECT * from vehicles WHERE id=%s", (vehicle_id,))
    vehicle = cur.fetchall()
    return jsonify({'vehicle': vehicle})

# * Get information about a vehicle with the plate
@app.route('/vehicles/<string:plate>', methods=['GET'])
def get_vehicle_plate(plate):
    cur = DB_config()
    cur = cur.cursor()
    cur.execute("SELECT * FROM vehicles WHERE plate=%s", (plate,))
    vehicle = cur.fetchall()
    cur.close()

    if vehicle and vehicle[0]['status'] == 'activo':
        return f"ÉXITO: El Vehículo {plate} se encuentra {vehicle[0]['status'].upper()} al conjunto {vehicle[0]['apartment_id']}"
    elif vehicle and vehicle[0]['status'] == 'inactivo':
        return f"ALERTA: El Vehículo {plate} se encuentra {vehicle[0]['status'].upper()} al conjunto {vehicle[0]['apartment_id']}"
    else:
        return "ADEVERTENCIA: El vehículo NO pertenece al conjunto"


# * Add a new user's information
@app.route('/vehicles', methods=['POST'])
def create_info_vehicle():
    if not request.json or not 'plate' in request.json:
        abort(400)
        
    plate = request.json.get('plate', "")
    apartment_id = request.json.get('apartment_id', "") # Torre # Piso #
    description = request.json.get('description', "")
    status = request.json.get("status", "") # Solo acepta activo o inactivo
    
    cur = DB_config()
    cur = cur.cursor()
    cur.execute("INSERT INTO vehicles(plate,apartment_id,description,status) VALUES(%s,%s,%s,%s)",(plate,apartment_id,description,status))
    cur.connection.commit()
    
    return jsonify({'vehicle': request.json}), 201

# * Edit a user's information vehicle
@app.route('/vehicles/<int:vehicle_id>', methods=['PUT'])
def update_info_user(vehicle_id):
    cur = DB_config()
    cur = cur.cursor()
    cur.execute("SELECT * FROM vehicles where id="+str(vehicle_id))
    vehicleUser = cur.fetchall()
    print(vehicleUser[0])
    
    plate = request.json.get('plate', vehicleUser[0]['plate'])
    apartment_id = request.json.get('apartment_id', vehicleUser[0]['apartment_id'])
    description = request.json.get('description', vehicleUser[0]['description'])
    status = request.json.get('status', vehicleUser[0]['status'])
    
    cur.execute("UPDATE vehicles SET plate =%s, apartment_id =%s ,description= %s,status= %s WHERE id=%s",(plate,apartment_id,description,status,vehicle_id))
    cur.connection.commit()
    
    return jsonify({'vehicleUser': vehicleUser})

# * Delete a user
@app.route('/vehicles/<int:vehicle_id>', methods=['DELETE'])
def delete_registry(vehicle_id):
    cur = DB_config()
    cur = cur.cursor()
    cur.execute("DELETE FROM vehicles WHERE id="+str(vehicle_id))
    cur.connection.commit()
    return jsonify({'result': True})

# * Upload image to detect and read the plate
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file has been sent"}), 400
    
    '''
     Stage for the detection of plates with YOLO
    '''
    archive = request.files['file']
    image = Image.open(archive.stream)
    image.thumbnail((1024, 1024))
    frame = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    results = detection.modeloYOLO.predict(frame)[0]
    
    '''
     Stage for plate extraction with OCR
    '''
    image_stream = BytesIO()
    image.save(image_stream, format="PNG")
    image_stream.seek(0)
        
    #* We call Azure's OCR function
    vehicle_plate = ocr_placas(image_stream)
    plate = vehicle_plate[0][0][0] # Visualizar la placa del vehiculo para luego comparar con la BD
    plate = plate.replace("-", "")
    
    #* We call YOLO function
    frame = detection_YOLO(frame, results, vehicle_plate)
    print(f"License plate to be taken to SQL {plate}")
    
    vehicle_info = get_vehicle_plate(plate)
    
    #* Convertir frame a BytesIO para enviarlo como respuesta
    _, buffer = cv2.imencode('.jpg', frame)
    image_io = BytesIO(buffer)

    response = send_file(image_io, mimetype='image/jpeg')
    response.headers["X-Vehicle-Info"] = vehicle_info

    return response
    
    
if __name__ == '__main__':
    app.run(debug=True)