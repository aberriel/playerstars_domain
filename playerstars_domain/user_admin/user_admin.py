from clapy_basic_classes import BasicEntity
from marshmallow import fields, post_load


class UserAdmin(BasicEntity):
    def __init__(self,
                 name: str,
                 email: str,
                 entity_id: str = None):
        super(UserAdmin, self).__init__(entity_id=entity_id)
        self.name = name
        self.email = email

    class Schema(BasicEntity.Schema):
        email = fields.Email(required=True, allow_none=False)
        name = fields.String(required=True, allow_none=False)

        @post_load
        def post_load(self, data, many, partial):
            return UserAdmin(**data)
