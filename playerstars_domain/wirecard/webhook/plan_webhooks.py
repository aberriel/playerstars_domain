from .basic_webhook import BasicWebhook
from marshmallow import fields, post_load
from ..plan import Plan


class PlanWebHook(BasicWebhook):
    def __init__(self, date, env, event, resource: Plan):
        super(PlanWebHook, self).__init__(date, env, event)
        self.resource = resource

    class Schema(BasicWebhook.Schema):
        resource = fields.Nested(
            Plan.Schema,
            required=True,
            allow_none=False)

        @post_load
        def post_load(self, data, many, partial):
            return PlanWebHook(**data)
