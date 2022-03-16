from .billing_info import CreditCard
from .creation_date import CreationDate
from clapy_basic_classes import BasicValue
from marshmallow import fields, post_load


class PaymentWirecardStatus(BasicValue):
    def __init__(self, code: int, description: str):
        self.code = code
        self.description = description

    class Schema(BasicValue.Schema):
        code = fields.Integer(required=True, allow_none=False)
        description = fields.String(required=True, allow_none=False)

        @post_load
        def post_load(self, data, many, partial):
            return PaymentWirecardStatus(**data)


class PaymentType(BasicValue):
    def __init__(self,
                 code: int,
                 credit_card: CreditCard,
                 description: str = None):
        self.code = code
        self.credit_card = credit_card
        self.description = description

    class Schema(BasicValue.Schema):
        code = fields.Integer(required=True, allow_none=False)
        credit_card = fields.Nested(
            CreditCard.Schema,
            required=True,
            allow_none=False)
        description = fields.String(required=False, allow_none=True)

        @post_load
        def post_load(self, data, many, partial):
            return PaymentType(**data)


class PaymentWirecard(BasicValue):
    def __init__(self,
                 id: int,
                 status: PaymentWirecardStatus,
                 payment_method: PaymentType = None,
                 amount: int = None,
                 invoice_id: int = None,
                 subscription_code: str = None,
                 moip_id: int = None,
                 creation_date: CreationDate = None):
        super(PaymentWirecard, self).__init__()
        self.id = id
        self.status = status
        self.payment_method = payment_method
        self.amount = amount
        self.invoice_id = invoice_id
        self.subscription_code = subscription_code
        self.moip_id = moip_id
        self.creation_date = creation_date

    class Schema(BasicValue.Schema):
        id = fields.Integer(required=True, allow_none=False)
        status = fields.Nested(
            PaymentWirecardStatus.Schema,
            required=True,
            allow_none=False)
        payment_method = fields.Nested(
            PaymentType.Schema,
            required=False,
            allow_none=True)
        amount = fields.Integer(required=False, allow_none=True)
        invoice_id = fields.Integer(required=False, allow_none=True)
        subscription_code = fields.String(required=False, allow_none=True)
        moip_id = fields.Integer(required=False, allow_none=True)
        creation_date = fields.Nested(
            CreationDate.Schema,
            required=False,
            allow_none=True)

        @post_load
        def post_load(self, data, many, partial):
            return PaymentWirecard(**data)
