from ..subscription import Subscription
from .basic_webhook import BasicWebhook
from marshmallow import fields, post_load


class SubscriptionWebhook(BasicWebhook):
    def __init__(self, date, env, event, resource: Subscription):
        super(SubscriptionWebhook, self).__init__(date, env, event)
        self.resource = resource

    class Schema(BasicWebhook.Schema):
        resource = fields.Nested(
            Subscription.Schema,
            required=True,
            allow_none=False)

        @post_load
        def post_load(self, data, many, partial):
            return SubscriptionWebhook(**data)
