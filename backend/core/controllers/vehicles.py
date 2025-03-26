from core.app import db
from core.models import Vehicle
from core.services import vehicles
from apiflask import APIBlueprint, abort
from core.schemas.utils import Message, Pagination
from core.schemas.vehicles import VehicleIn, VehicleOut, VehiclesOut


bp = APIBlueprint('vehicles', __name__)


@bp.get('/')
@bp.input(Pagination, location='query')
@bp.output(VehiclesOut)
def get_vehicles(query_data):
    '''Get vehicles'''

    try:
        return {'items': vehicles.get_vehicles(query_data['search'], 
                                         query_data['page'],
                                         query_data['per_page'])}
    except Exception as ex:
        abort(str(ex))


@bp.get('/<int:vehicle_id>')
@bp.output(VehicleOut)
def get_vehicle(vehicle_id):
    '''Get vehicle'''

    try:
        return vehicles.get_vehicle(vehicle_id)
    except Exception as ex:
        abort(str(ex))


@bp.post('/')
@bp.input(VehicleIn, arg_name='vehicle')
@bp.output(Message)
def create_vehicle(vehicle):
    '''Create vehicle'''

    try:
        db.session.add(vehicle)
        db.session.commit()
        return {'message': 'Vehicle created successfuly'}
    except Exception as ex:
        print(str(ex))
        abort(str(ex))


@bp.put('/<int:vehicle_id>')
@bp.input(VehicleIn)
@bp.output(Message)
def update_vehicles(vehicle_id, json_data):
    '''Update vehicle'''

    try:
        vehicles.update_vehicle(vehicle_id, json_data)
        return {'message': 'Vehicle updated successfuly'}
    except Exception as ex:
        print(str(ex))
        abort(str(ex))


@bp.delete('/<int:vehicle_id>')
@bp.output(Message)
def delete_vehicles(vehicle_id):
    '''Delete vehicles'''

    try:
        vehicles.delete_vehicle(vehicle_id)
        return {'message': 'vehicle deleted successfuly'}
    except Exception as ex:
        print(str(ex))
        abort(str(ex))
