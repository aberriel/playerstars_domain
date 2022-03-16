from clapy_basic_classes import BasicEntity
from marshmallow import fields, post_load
from typing import List


class Lists(BasicEntity):
    def __init__(self,
                 countries=None,
                 states: list = None,
                 entity_id: str = None):
        super(Lists, self).__init__(entity_id)
        self.states: List[str] = states if states else []
        self.countries: List[str] = countries if countries else []
        self.state_list = ", ".join([str(x) for x in self.states])
        self.country_list = ", ".join([str(x) for x in self.countries])

    def __repr__(self):
        return f'Countries: {self.country_list} / States: {self.state_list}'

    class Schema(BasicEntity.Schema):
        states = fields.List(fields.String())
        countries = fields.List(fields.String())

        @post_load
        def post_load(self, data, many, partial):
            return Lists(**data)
