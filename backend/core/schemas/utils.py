from apiflask import fields, Schema
from marshmallow import EXCLUDE


class BaseSchema(Schema):
    class Meta:
        unknown = EXCLUDE


class Pagination(Schema):
    search = fields.String(load_default='')
    page = fields.Integer(load_default=1)
    per_page = fields.Integer(data_key='perPage', load_default=15)


class Message(Schema):
    message = fields.String()
