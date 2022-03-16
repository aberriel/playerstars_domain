from clapy_basic_classes import BasicValue
from datetime import datetime
from marshmallow import fields, post_load
from marshmallow_enum import EnumField
from playerstars_domain.player.purchase import PaymentGateway
from playerstars_domain.utils.datetime_helper import aware_now


class PlayerSubscription(BasicValue):
    def __init__(self,
                 expiration_date: datetime,
                 payment_gateway: PaymentGateway,
                 plan_name: str):
        self.expiration_date = expiration_date
        self.plan_name = plan_name
        self.payment_gateway = payment_gateway

    def is_active(self):
        return self.expiration_date > aware_now()

    class Schema(BasicValue.Schema):
        expiration_date = fields.DateTime(
            format='iso',
            required=True,
            allow_none=False)
        plan_name = fields.String(required=True, allow_none=False)
        payment_gateway = EnumField(
            PaymentGateway,
            required=True,
            allow_none=False)

        @post_load
        def post_load(self, data, many, partial):
            return PlayerSubscription(**data)
