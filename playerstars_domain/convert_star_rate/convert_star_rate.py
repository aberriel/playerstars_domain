from clapy_basic_classes import BasicEntity
from marshmallow import fields, post_load


class ConvertStarRate(BasicEntity):
    def __init__(self, convert_rate: int, entity_id: str = None):
        super(ConvertStarRate, self).__init__(entity_id=entity_id)
        self.convert_rate = convert_rate

    class Schema(BasicEntity.Schema):
        convert_rate = fields.Integer(required=True, allow_none=False)

        @post_load
        def post_load(self, data, many, partial):
            return ConvertStarRate(**data)
