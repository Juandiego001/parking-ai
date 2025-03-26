from apiflask import Schema, fields
from marshmallow import post_load
from core.models import Tower
from core.schemas.utils import BaseSchema


class TowerIn(BaseSchema):
    id = fields.Integer(required=False)
    unit = fields.String()
    floors = fields.Integer()
    status = fields.String(load_default='ACTIVE')

    @post_load
    def make_object(self, data, **kwargs):
        return Tower(**data)


class TowerOut(BaseSchema):
    id = fields.Integer()
    unit = fields.String()
    floors = fields.Integer()
    status = fields.String()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()


class TowersOut(Schema):
    items = fields.List(fields.Nested(TowerOut))
