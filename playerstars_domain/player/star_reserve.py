from clapy_basic_classes import BasicValue
from marshmallow import fields, post_load
from marshmallow_enum import EnumField
from playerstars_domain.player.star_transaction import CoinType


class StarReserve(BasicValue):
    def __init__(self,
                 event_id: str,
                 star_type: CoinType,
                 star_value: int):
        super(StarReserve, self).__init__()
        self.event_id = event_id
        self.star_type = star_type
        self.star_value = star_value

    def __call__(self):
        return self.to_json()

    def __repr__(self):
        return f'{self.star_type.value} - {self.star_value}'

    class Schema(BasicValue.Schema):
        event_id = fields.String(required=True, allow_none=False)
        star_type = EnumField(
            CoinType,
            required=True,
            allow_none=False,
            default=CoinType.GOLDEN_STAR)
        star_value = fields.Integer(required=True, allow_none=False)

        @post_load
        def post_load(self, data, many, partial):
            return StarReserve(**data)
