from ..payment import PaymentWirecard
from .basic_webhook import BasicWebhook
from marshmallow import fields, post_load


class PaymentWebhook(BasicWebhook):
    def __init__(self, date, env, event, resource: PaymentWirecard):
        super(PaymentWebhook, self).__init__(date, env, event)
        self.resource = resource

    class Schema(BasicWebhook.Schema):
        resource = fields.Nested(
            PaymentWirecard.Schema,
            required=True,
            allow_none=False)

        @post_load
        def post_load(self, data, many, partial):
            return PaymentWebhook(**data)
