from core.app import db
from core.services import entries, vehicles
from apiflask import APIBlueprint, abort
from core.schemas.utils import Message, Pagination
from core.schemas.entries import EntryIn, EntryOut, EntriesOut, PhotoIn, PhotoOut
from werkzeug.exceptions import HTTPException


bp = APIBlueprint('entries', __name__)


@bp.get('/')
@bp.input(Pagination, location='query')
@bp.output(EntriesOut)
def get_entries(query_data):
    '''Get entries'''

    try:
        return {'items': entries.get_entries(query_data['search'], 
                                         query_data['page'],
                                         query_data['per_page'])}
    except Exception as ex:
        abort(str(ex))


@bp.get('/<int:entry_id>')
@bp.output(EntryOut)
def get_entry(entry_id):
    '''Get entry'''

    try:
        return entries.get_entry(entry_id)
    except Exception as ex:
        abort(str(ex))


@bp.post('/')
@bp.input(EntryIn, arg_name='entry')
@bp.output(Message)
def create_entry(entry):
    '''Create entry'''

    try:
        db.session.add(entry)
        db.session.commit()
        return {'message': 'Entry created successfuly'}
    except Exception as ex:
        print(str(ex))
        abort(str(ex))


@bp.post('/validate/photo')
@bp.input(PhotoIn)
@bp.output(PhotoOut)
def validate_photo(json_data):
    '''Validate photo'''
  
    try:
        plate = entries.validate(json_data['photo'].split(',')[1])
        if not plate:
            return {'message': 'Could detect if there were any plate in the photo', 'plate': None, 'type': None}
        is_owner = True if vehicles.get_vehicle_by_plate(plate) else False
        return {'message': 'Photo validated', 'plate': plate, 'is_owner': is_owner}
    except HTTPException as ex:
        print(str(ex))
        abort(str(ex))
    except Exception as ex:
        print(str(ex))
        abort(str(ex))


@bp.put('/<int:entry_id>')
@bp.input(EntryIn)
@bp.output(Message)
def update_entries(entry_id, json_data):
    '''Update entry'''

    try:
        entries.update_entry(entry_id, json_data)
        return {'message': 'Entry updated successfuly'}
    except Exception as ex:
        print(str(ex))
        abort(str(ex))


@bp.delete('/<int:entry_id>')
@bp.output(Message)
def delete_entries(entry_id):
    '''Delete entries'''

    try:
        entries.delete_entry(entry_id)
        return {'message': 'Entry deleted successfuly'}
    except Exception as ex:
        print(str(ex))
        abort(str(ex))
