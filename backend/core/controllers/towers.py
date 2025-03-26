from core.app import db
from core.models import Tower
from core.services import towers
from apiflask import APIBlueprint, abort
from core.schemas.utils import Message, Pagination
from core.schemas.towers import TowerIn, TowerOut, TowersOut


bp = APIBlueprint('towers', __name__)


@bp.get('/')
@bp.input(Pagination, location='query')
@bp.output(TowersOut)
def get_towers(query_data):
    '''Get towers'''

    try:
        return {'items': towers.get_towers(query_data['search'], 
                                         query_data['page'],
                                         query_data['per_page'])}
    except Exception as ex:
        abort(str(ex))


@bp.get('/<int:tower_id>')
@bp.output(TowerOut)
def get_tower(tower_id):
    '''Get tower'''

    try:
        return towers.get_tower(tower_id)
    except Exception as ex:
        abort(str(ex))


@bp.post('/')
@bp.input(TowerIn, arg_name='tower')
@bp.output(Message)
def create_tower(tower):
    '''Create tower'''

    try:
        db.session.add(tower)
        db.session.commit()
        return {'message': 'Tower created successfuly'}
    except Exception as ex:
        print(str(ex))
        abort(str(ex))


@bp.put('/<int:tower_id>')
@bp.input(TowerIn)
@bp.output(Message)
def update_towers(tower_id, json_data):
    '''Update tower'''

    try:
        towers.update_tower(tower_id, json_data)
        return {'message': 'Tower updated successfuly'}
    except Exception as ex:
        print(str(ex))
        abort(str(ex))


@bp.delete('/<int:tower_id>')
@bp.output(Message)
def delete_towers(tower_id):
    '''Delete towers'''

    try:
        towers.delete_tower(tower_id)
        return {'message': 'Tower deleted successfuly'}
    except Exception as ex:
        print(str(ex))
        abort(str(ex))
