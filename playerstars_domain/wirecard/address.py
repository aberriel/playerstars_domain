from clapy_basic_classes import BasicValue
from marshmallow import fields, post_load


class Address(BasicValue):
    def __init__(self,
                 street: str,
                 number: str,
                 district: str,
                 city: str,
                 state: str,
                 zipcode: str,
                 country: str = 'BRA',
                 complement: str = None):
        self.street = street
        self.number = number
        self.complement = complement
        self.district = district
        self.city = city
        self.state = state
        self.country = country or 'BRA'
        self.zipcode = zipcode

    class Schema(BasicValue.Schema):
        street = fields.String(required=True, allow_none=False)
        number = fields.String(required=True, allow_none=False)
        complement = fields.String(required=False, allow_none=True)
        district = fields.String(required=True, allow_none=False)
        city = fields.String(required=True, allow_none=False)
        state = fields.String(required=True, allow_none=False)
        country = fields.String(
            required=True,
            allow_none=False,
            default='BRA')
        zipcode = fields.String(required=True, allow_none=False)

        @post_load
        def post_load(self, data, many, partial):
            return Address(**data)
