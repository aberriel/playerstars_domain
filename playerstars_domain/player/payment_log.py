from clapy_basic_classes import BasicValue
from datetime import datetime
from marshmallow import fields, post_load
from marshmallow_enum import EnumField
from playerstars_domain.player.purchase import PaymentGateway


class PaymentLog(BasicValue):
    def __init__(self,
                 transaction_date: datetime,
                 payment_gateway: PaymentGateway,
                 raw_sent_data: str = None,
                 raw_received_data: str = None):
        self.transaction_date = transaction_date
        self.raw_sent_data = raw_sent_data
        self.raw_received_data = raw_received_data
        self.payment_gateway = payment_gateway

    class Schema(BasicValue.Schema):
        transaction_date = fields.AwareDateTime(
            format='iso',
            required=True,
            allow_none=False)
        raw_sent_data = fields.String(required=False, allow_none=True)
        raw_received_data = fields.String(required=False, allow_none=True)
        payment_gateway = EnumField(
            PaymentGateway,
            required=True,
            allow_none=False)

        @post_load
        def post_load(self, data, many, partial):
            return PaymentLog(**data)
