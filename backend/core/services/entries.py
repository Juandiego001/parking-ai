import cv2
import base64
import numpy as np
from PIL import Image
from io import BytesIO
from core.app import db, model
from core.models import Entry
from sqlalchemy import or_, and_
from werkzeug.exceptions import HTTPException
from core.implements.detection import do_detection
from core.implements.ocr import ocr_placas


def get_entries(search: str, page: int, per_page: int):
    '''Get entries'''

    query = Entry.status == 'ACTIVE'
    if search:
        query = and_(Entry.status == 'ACTIVE', Entry.unit.ilike(f'%{search}%'))

    return db.paginate(db.session.query(Entry).filter(query),
                       page=page, per_page=per_page)


def get_entry(entry_id: int):
    '''Get entry by entry id'''

    return db.session.query(Entry).filter(Entry.id == entry_id).first()


def check_entry_exists(entry_id: int):
    '''Check if entry exists'''

    return db.session.query(Entry).filter(Entry.id == entry_id).first()


def update_entry(entry_id: int, entry_load):
    '''Update entry'''

    if not check_entry_exists(entry_id):
        raise HTTPException('Entry not found')

    db.session.merge(entry_load)
    db.session.commit()


def delete_entry(entry_id: int):
    '''Delete entry'''

    db.session.merge(Entry(id=entry_id, status='INACTIVE'))
    db.session.commit()


def validate(photo: str):
    '''Check if plate exists. If exists, return it'''

    '''
    Etapa para la detección de placas con YOLO
    '''
    img_bytes = BytesIO(base64.b64decode(photo))
    image = Image.open(img_bytes)
    image.thumbnail((1024, 1024))
    frame = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    results = model.predict(frame)[0]
    image.save('result_prediction.png', format='png')
    # print('RESULTS: ')
    # print(results)

    '''
    Etapa para la extracción de placas con OCR
    '''
    image_stream = BytesIO()
    image.save(image_stream, format='png')
    image_stream.seek(0)

    '''
    Llamamos función de OCR Azure
    '''
    return ocr_placas(image_stream)
