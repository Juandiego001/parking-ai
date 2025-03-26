from core.app import db
from core.models import Tower
from sqlalchemy import or_, and_
from werkzeug.exceptions import HTTPException


def get_towers(search: str, page: int, per_page: int):
    '''Get towers'''

    query = Tower.status == 'ACTIVE'
    if search:
        query = and_(Tower.status == 'ACTIVE', Tower.unit.ilike(f'%{search}%'))

    return db.paginate(db.session.query(Tower).filter(query),
                       page=page, per_page=per_page)


def get_tower(tower_id: int):
    '''Get tower by tower id'''

    return db.session.query(Tower).filter(Tower.id == tower_id).first()


def check_tower_exists(tower_id: int):
    '''Check if tower exists'''

    return db.session.query(Tower).filter(Tower.id == tower_id).first()


def update_tower(tower_id: int, tower_load):
    '''Update tower'''

    if not check_tower_exists(tower_id):
        raise HTTPException('Tower not found')

    db.session.merge(tower_load)
    db.session.commit()


def delete_tower(tower_id: int):
    '''Delete tower'''

    db.session.merge(Tower(id=tower_id, status='INACTIVE'))
    db.session.commit()
