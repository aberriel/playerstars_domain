from clapy_basic_classes import BasicValue
from datetime import datetime
from enum import Enum
from marshmallow import fields, post_load
from marshmallow_enum import EnumField
from playerstars_domain.utils.datetime_helper import aware_now


class ComponentResult(Enum):
    WINNER = 'WINNER'
    LOSER = 'LOSER'
    TIED = 'TIED'
    RESIGNED = 'RESIGNED'


class DuelComponentResult(BasicValue):
    def __init__(self,
                 result: ComponentResult,
                 submission_datetime: datetime = aware_now(),
                 result_image: str = None):
        super(DuelComponentResult, self).__init__()
        result_datetime = submission_datetime or aware_now()
        self.result = result
        self.submission_datetime = result_datetime
        self.result_image = result_image

    def to_string(self):
        return f'{self.submission_datetime.isoformat()} - {self.result.value}'

    def __repr__(self):
        return f"Result: {self.result.value} | " \
               f"Submission Datetime: " \
               f"{self.submission_datetime.isoformat()} | " \
               f"Result Image Path: " \
               f"{self.result_image if self.result_image else 'No Image'}"

    class Schema(BasicValue.Schema):
        result = EnumField(
            ComponentResult,
            required=True,
            allow_none=False)
        submission_datetime = fields.AwareDateTime(
            required=True,
            format='iso',
            default=aware_now())
        result_image = fields.String(required=False, allow_none=True)

        @post_load
        def on_load(self, data, many, partial):
            return DuelComponentResult(**data)
