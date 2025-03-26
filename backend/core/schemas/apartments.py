from apiflask import Schema, fields
from marshmallow import post_load
from core.models import Apartment
from core.schemas.utils import BaseSchema


class ApartmentIn(BaseSchema):
    id = fields.Integer(required=False)
    unit = fields.Integer()
    floor = fields.Integer()
    tower_id = fields.Integer(data_key='towerId')
    status = fields.String(load_default='ACTIVE')
    created_at = fields.DateTime(required=False, data_key='createdAt')
    updated_at = fields.DateTime(required=False, data_key='updatedAt')

    @post_load
    def make_object(self, data, **kwargs):
        return Apartment(**data)


class ApartmentOut(BaseSchema):
    id = fields.Integer()
    unit = fields.Integer()
    floor = fields.Integer()
    tower_id = fields.Integer(data_key='towerId')
    status = fields.String()
    created_at = fields.DateTime(data_key='createdAt')
    updated_at = fields.DateTime(data_key='updatedAt')


class ApartmentsOut(Schema):
    items = fields.List(fields.Nested(ApartmentOut))
