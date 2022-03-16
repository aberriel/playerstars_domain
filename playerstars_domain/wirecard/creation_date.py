from clapy_basic_classes import BasicValue
from datetime import datetime
from marshmallow import fields, post_load
from playerstars_domain.utils.datetime_helper import aware_utc


class CreationDate(BasicValue):
    def __init__(self, year: int,
                 month: int,
                 day: int,
                 hour: int = None,
                 minute: int = None,
                 second: int = None):
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute
        self.second = second

    @property
    def creation_date_as_datetime(self):
        creation_datetime = datetime(self.year, self.month, self.day,
                                     self.hour, self.minute, self.second)
        return aware_utc(creation_datetime)

    class Schema(BasicValue.Schema):
        year = fields.Integer(required=True, allow_none=False)
        month = fields.Integer(required=True, allow_none=False)
        day = fields.Integer(required=True, allow_none=False)
        hour = fields.Integer(required=False, allow_none=True)
        minute = fields.Integer(required=False, allow_none=True)
        second = fields.Integer(required=False, allow_none=True)

        @post_load
        def post_load(self, data, many, partial):
            return CreationDate(**data)
