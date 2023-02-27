from marshmallow import Schema, fields, INCLUDE, validate
from flask import Flask

app = Flask(__name__)


class JoinSchema(Schema):
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    email = fields.Str(required=True, validate=validate.Email(
        error="Noat a valid email address"))
    password = fields.Str(required=True, validate=[
                          validate.Length(min=6, max=36)])
    created_at = fields.DateTime(dump_only=True)
