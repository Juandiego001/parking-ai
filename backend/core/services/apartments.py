from core.app import db
from core.models import Apartment
from sqlalchemy import or_, and_
from werkzeug.exceptions import HTTPException


def get_apartments(search: str, page: int, per_page: int):
    '''Get apartments'''

    query = Apartment.status == 'ACTIVE'
    if search:
        query = and_(Apartment.status == 'ACTIVE',
                     or_(Apartment.full_name.ilike(f'%{search}%'),
                         Apartment.document.ilike(f'%{search}%'),
                         Apartment.email.ilike(f'%{search}%')))

    return db.paginate(db.session.query(Apartment).filter(query),
                       page=page, per_page=per_page)

def get_apartment(apartment_id: int):
    '''Get apartment by apartment id'''

    return db.session.query(Apartment).filter(Apartment.id == apartment_id).first()


def check_apartment_exists(apartment_id: int):
    '''Check if apartment exists'''

    return db.session.query(Apartment).filter(Apartment.id == apartment_id).first()


def update_apartment(apartment_id: int, apartment_load):
    '''Update apartment'''

    if not check_apartment_exists(apartment_id):
        raise HTTPException('Apartment not found')

    db.session.merge(apartment_load)
    db.session.commit()


def delete_apartment(apartment_id: int):
    '''Delete apartment'''

    db.session.merge(Apartment(id=apartment_id, status='INACTIVE'))
    db.session.commit()
