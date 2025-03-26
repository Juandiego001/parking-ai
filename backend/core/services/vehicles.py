from core.app import db
from core.models import Vehicle
from sqlalchemy import or_, and_
from werkzeug.exceptions import HTTPException


def get_vehicles(search: str, page: int, per_page: int):
    '''Get vehicles'''

    query = Vehicle.status == 'ACTIVE'
    if search:
        query = and_(Vehicle.status == 'ACTIVE',
                     or_(Vehicle.full_name.ilike(f'%{search}%'),
                         Vehicle.document.ilike(f'%{search}%'),
                         Vehicle.email.ilike(f'%{search}%')))

    return db.paginate(db.session.query(Vehicle).filter(query),
                       page=page, per_page=per_page)

def get_vehicle(vehicle_id: int):
    '''Get vehicle by vehicle id'''

    return db.session.query(Vehicle).filter(Vehicle.id == vehicle_id).first()


def check_vehicle_exists(vehicle_id: int):
    '''Check if vehicle exists'''

    return db.session.query(Vehicle).filter(Vehicle.id == vehicle_id).first()


def update_vehicle(vehicle_id: int, user_load):
    '''Update vehicle'''

    if not check_vehicle_exists(vehicle_id):
        raise HTTPException('Vehicle not found')

    db.session.merge(user_load)
    db.session.commit()


def delete_vehicle(vehicle_id: int):
    '''Delete vehicle'''

    db.session.merge(Vehicle(id=vehicle_id, status='INACTIVE'))
    db.session.commit()
