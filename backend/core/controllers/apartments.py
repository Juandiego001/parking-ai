from core.app import db
from core.models import Apartment
from core.services import apartments
from apiflask import APIBlueprint, abort
from core.schemas.utils import Message, Pagination
from core.schemas.apartments import ApartmentIn, ApartmentOut, ApartmentsOut


bp = APIBlueprint('apartments', __name__)


@bp.get('/')
@bp.input(Pagination, location='query')
@bp.output(ApartmentsOut)
def get_apartments(query_data):
    '''Get apartments'''

    try:
        return {'items': apartments.get_apartments(query_data['search'], 
                                         query_data['page'],
                                         query_data['per_page'])}
    except Exception as ex:
        abort(str(ex))


@bp.get('/<int:apartment_id>')
@bp.output(ApartmentOut)
def get_apartment(apartment_id):
    '''Get apartment'''

    try:
        return apartments.get_apartment(apartment_id)
    except Exception as ex:
        abort(str(ex))


@bp.post('/')
@bp.input(ApartmentIn, arg_name='apartment')
@bp.output(Message)
def create_apartment(apartment):
    '''Create apartment'''

    try:
        db.session.add(apartment)
        db.session.commit()
        return {'message': 'Apartment created successfuly'}
    except Exception as ex:
        print(str(ex))
        abort(str(ex))


@bp.put('/<int:apartment_id>')
@bp.input(ApartmentIn)
@bp.output(Message)
def update_apartments(apartment_id, json_data):
    '''Update apartment'''

    try:
        apartments.update_apartment(apartment_id, json_data)
        return {'message': 'Apartment updated successfuly'}
    except Exception as ex:
        print(str(ex))
        abort(str(ex))


@bp.delete('/<int:apartment_id>')
@bp.output(Message)
def delete_apartments(apartment_id):
    '''Delete apartments'''

    try:
        apartments.delete_apartment(apartment_id)
        return {'message': 'Apartment deleted successfuly'}
    except Exception as ex:
        print(str(ex))
        abort(str(ex))
