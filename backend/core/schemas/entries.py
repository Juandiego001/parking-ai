from apiflask import Schema, fields
from marshmallow import post_load
from core.models import Entry
from core.schemas.utils import BaseSchema


class PhotoIn(BaseSchema):
    photo = fields.String()


class PhotoOut(BaseSchema):
    message = fields.String()
    plate = fields.String()
    is_owner = fields.Boolean(data_key='isOwner')


class EntryIn(BaseSchema):
    id = fields.Integer(required=False)
    plate = fields.String()
    is_owner = fields.Boolean(data_key='isOwner')
    apartment_id = fields.Integer(data_key='apartmentId')
    description = fields.String(required=False)
    status = fields.String(load_default='ACTIVE')

    @post_load
    def make_object(self, data, **kwargs):
        return Entry(**data)


class EntryOut(BaseSchema):
    id = fields.Integer()
    plate = fields.String()
    is_owner = fields.Boolean(data_key='isOwner')
    apartment_id = fields.Integer(data_key='apartmentId')
    description = fields.String()
    status = fields.String()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()


class EntriesOut(Schema):
    items = fields.List(fields.Nested(EntryOut))
