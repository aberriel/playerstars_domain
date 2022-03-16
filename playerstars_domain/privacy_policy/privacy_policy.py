from clapy_basic_classes import BasicEntity
from marshmallow import fields, post_load


class PrivacyPolicy(BasicEntity):
    def __init__(self, privacy_policy: str, entity_id: str = None):
        super(PrivacyPolicy, self).__init__(entity_id=entity_id)
        self.privacy_policy = privacy_policy

    class Schema(BasicEntity.Schema):
        privacy_policy = fields.String(required=True, allow_none=False)

        @post_load
        def post_load(self, data, many, partial):
            return PrivacyPolicy(**data)
