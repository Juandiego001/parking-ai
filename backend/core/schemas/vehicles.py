from apiflask import Schema, fields
from marshmallow import post_load
from core.models import Vehicle
from core.schemas.utils import BaseSchema


class VehicleIn(BaseSchema):
    plate = fields.String()
    apartment_id = fields.Integer(data_key='apartmentId')
    description = fields.String()
    status = fields.String(load_default='ACTIVE')

    @post_load
    def make_object(self, data, **kwargs):
        return Vehicle(**data)


class VehicleOut(BaseSchema):
    id = fields.Integer()
    plate = fields.String()
    apartment_id = fields.Integer(data_key='apartmentId')
    description = fields.String()
    status = fields.String()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()


class VehiclesOut(Schema):
    items = fields.List(fields.Nested(VehicleOut))
