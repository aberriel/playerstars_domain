from playerstars_domain.wirecard import Invoice
from .basic_webhook import BasicWebhook
from marshmallow import fields, post_load


class InvoiceWebhook(BasicWebhook):
    def __init__(self, date, env, event, resource: Invoice):
        super(InvoiceWebhook, self).__init__(date, env, event)
        self.resource = resource

    class Schema(BasicWebhook.Schema):
        resource = fields.Nested(
            Invoice.Schema,
            required=True,
            allow_none=False)

        @post_load
        def post_load(self, data, many, partial):
            return InvoiceWebhook(**data)
