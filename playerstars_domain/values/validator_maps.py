from clapy_basic_classes import BasicValue
from marshmallow import fields, post_load


class ValidatorMaps(BasicValue):
    def __init__(self,
                 game_id: str,
                 class_name: str):
        self.game_id = game_id
        self.class_name = class_name

    class Schema(BasicValue.Schema):
        game_id = fields.String(
            required=True, allow_none=False)
        class_name = fields.String(required=True, allow_none=False)

        @post_load
        def post_load(self, data, many, partial):
            return ValidatorMaps(**data)
