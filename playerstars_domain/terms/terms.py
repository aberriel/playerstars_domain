from clapy_basic_classes import BasicEntity
from marshmallow import fields, post_load


class Terms(BasicEntity):
    def __init__(self, terms: str, entity_id: str = None):
        super(Terms, self).__init__(entity_id=entity_id)
        self.terms = terms

    class Schema(BasicEntity.Schema):
        terms = fields.String(required=True, allow_none=False)

        @post_load
        def post_load(self, data, many, partial):
            return Terms(**data)
