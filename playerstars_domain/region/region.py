from clapy_basic_classes import BasicEntity
from marshmallow import fields, post_load
from typing import List


class CountryRegion(BasicEntity):
    def __init__(self,
                 name: str,
                 minimum_bet: int,
                 countries: list,
                 entity_id: str = None):
        super(CountryRegion, self).__init__(entity_id=entity_id)
        self.name = name
        self.minimum_bet = minimum_bet
        self.countries: List[str] = countries if countries else []

    class Schema(BasicEntity.Schema):
        name = fields.Str(required=True, allow_none=False)
        minimum_bet = fields.Integer(required=True,
                                     allow_none=False,
                                     default=1)
        countries = fields.List(fields.String(), many=True)

        @post_load
        def post_load(self, data, many, partial):
            return CountryRegion(**data)


class StateRegion(BasicEntity):
    def __init__(self, name: str,
                 minimum_bet: int,
                 states: list,
                 entity_id: str = None):
        super(StateRegion, self).__init__(entity_id=entity_id)
        self.name = name
        self.minimum_bet = minimum_bet
        self.states: List[str] = states if states else []

    class Schema(BasicEntity.Schema):
        name = fields.Str(required=True, allow_none=False)
        minimum_bet = fields.Integer(
            required=True,
            allow_none=False,
            default=1)
        states = fields.List(fields.String(), many=True)

        @post_load
        def post_load(self, data, many, partial):
            return StateRegion(**data)
