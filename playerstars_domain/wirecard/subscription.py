from .api_response_info import InfoDetail
from .invoice import CreationDate, Invoice, NextInvoiceDate
from .plan import PaymentMethod, Plan
from .subscriber import Subscriber
from clapy_basic_classes import BasicValue
from enum import Enum
from marshmallow import fields, post_load
from marshmallow_enum import EnumField
from typing import List


class SubscriptionStatus(Enum):
    ACTIVE = 'ACTIVE'
    SUSPENDED = 'SUSPENDED'
    EXPIRED = 'EXPIRED'
    OVERDUE = 'OVERDUE'
    CANCELED = 'CANCELED'


class Subscription(BasicValue):
    def __init__(self,
                 code: str,
                 amount: int,
                 plan: Plan,
                 customer: Subscriber = None,
                 payment_method: PaymentMethod = None,
                 id: str = None,
                 moip_account: str = None,
                 creation_date: CreationDate = None,
                 message: str = None,
                 invoice: Invoice = None,
                 next_invoice_date: NextInvoiceDate = None,
                 errors: List[InfoDetail] = None,
                 alerts: List[InfoDetail] = None,
                 status: SubscriptionStatus = None):
        super(Subscription, self).__init__()
        self.id = id
        self.code = code
        self.amount = amount
        self.plan = plan
        self.customer = customer
        self.payment_method = payment_method
        self.moip_account = moip_account
        self.creation_date = creation_date
        self.message = message
        self.invoice = invoice
        self.next_invoice_date = next_invoice_date
        self.status = status
        self.errors = errors
        self.alerts = alerts

    @classmethod
    def object_name(cls):
        return 'subscriptions'

    @classmethod
    def post_params(cls, new_customer=False):
        return {
            'new_customer': str(new_customer).lower()
        }

    @classmethod
    def post_put_returns_object(cls):
        return True

    class Schema(BasicValue.Schema):
        code = fields.String(required=True, allow_none=False)
        amount = fields.Integer(required=True, allow_none=False)
        plan = fields.Nested(Plan.Schema, required=True, allow_none=False)
        customer = fields.Nested(
            Subscriber.Schema,
            required=False,
            allow_none=True)
        payment_method = EnumField(
            PaymentMethod,
            required=False,
            allow_none=True,
            default=PaymentMethod.CREDIT_CARD)
        id = fields.String(required=False, allow_none=True)
        moip_account = fields.String(required=False, allow_none=True)
        creation_date = fields.Nested(
            CreationDate.Schema,
            required=False,
            allow_none=True)
        message = fields.String(required=False, allow_none=True)
        invoice = fields.Nested(
            Invoice.Schema,
            required=False,
            allow_none=True)
        next_invoice_date = fields.Nested(
            NextInvoiceDate.Schema,
            required=False,
            allow_none=True)
        status = EnumField(
            SubscriptionStatus,
            required=False,
            allow_none=True)
        errors = fields.Nested(
            InfoDetail.Schema, many=True,
            required=False,
            allow_none=True)
        alerts = fields.Nested(
            InfoDetail.Schema, many=True,
            required=False,
            allow_none=True)

        @post_load
        def post_load(self, data, many, partial):
            return Subscription(**data)
