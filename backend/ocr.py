from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials
import time
import re
import config

# Keys de Azure Vision Studio
subscription_key = config.subscription_key
endpoint = config.endpoint

computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

# Estructura para OCR extraer de la detección de YOLO
patron_placas = re.compile(r"\b[A-Z]{3}[-·.® ]?\d{3}\b")    # Vehiculos AAA-123
patron_placasm = re.compile(r"\b[A-Z]{3}[-·.® ]\d{2}[A-Z]\b")   # Motocicletas AAA-12A

def ocr_placas(image_stream):
    read_response = computervision_client.read_in_stream(image_stream, raw=True)
    read_operation_location = read_response.headers["Operation-Location"]
    operation_id = read_operation_location.split("/")[-1]
    
    while True:
        read_result = computervision_client.get_read_result(operation_id)
        if read_result.status not in ["notStarted", "running"]:
            break
        time.sleep(1)
        
    placa_vehiculo =[]
    
    if read_result.status == OperationStatusCodes.succeeded:
        for page in read_result.analyze_result.read_results:
            for line in page.lines:
                if line.words:
                    confidence_avg = sum(word.confidence for word in line.words) / len(line.words)
                else:
                    confidence_avg = 1.0
                
                placas_raw = patron_placas.findall(line.text) + patron_placasm.findall(line.text)
                placas_en_linea = [
                    (placa.replace(" ", "-").replace(".", "-").replace("-", "-").replace("·", "-").replace("®", "-"), confidence_avg)
                    for placa in placas_raw
                ]
                placa_vehiculo.extend(placas_en_linea)
                
        
    return placa_vehiculo, confidence_avg