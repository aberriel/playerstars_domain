from .basic_webhook import BasicWebhook
from ..subscriber import Subscriber
from marshmallow import fields, post_load


class SubscriberWebhook(BasicWebhook):
    def __init__(self, date, env, event, resource: Subscriber):
        super(SubscriberWebhook, self).__init__(date, env, event)
        self.resource = resource

    class Schema(BasicWebhook.Schema):
        resource = fields.Nested(
            Subscriber.Schema,
            required=True,
            allow_none=False)

        @post_load
        def post_load(self, data, many, partial):
            return SubscriberWebhook(**data)
