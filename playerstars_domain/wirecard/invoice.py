from .creation_date import CreationDate
from .plan import Plan
from .subscriber import Subscriber
from clapy_basic_classes import BasicValue
from datetime import date, datetime
from marshmallow import fields, post_load
from playerstars_domain.utils.datetime_helper import aware_utc
from typing import List


class NextInvoiceDate(BasicValue):
    def __init__(self, year: int, month: int, day: int):
        self.year = year
        self.month = month
        self.day = day

    @property
    def next_invoice_as_date(self):
        return date(self.year, self.month, self.day)

    @property
    def next_invoice_as_datetime(self):
        next_datetime = datetime(
            self.year, self.month, self.day, 0, 0, 0)
        return aware_utc(next_datetime)

    class Schema(BasicValue.Schema):
        year = fields.Integer(required=True, allow_none=False)
        month = fields.Integer(required=True, allow_none=False)
        day = fields.Integer(required=True, allow_none=False)

        @post_load
        def post_load(self, data, many, partial):
            return NextInvoiceDate(**data)


class InvoiceItem(BasicValue):
    def __init__(self, amount: int, type: str):
        self.amount = amount
        self.type = type

    class Schema(BasicValue.Schema):
        amount = fields.Integer(required=True, allow_none=False)
        type = fields.String(required=True, allow_none=False)

        @post_load
        def post_load(self, data, many, partial):
            return InvoiceItem(**data)


class InvoiceStatus(BasicValue):
    def __init__(self, code: int, description: str):
        self.code = code
        self.description = description

    class Schema(BasicValue.Schema):
        code = fields.Integer(required=True, allow_none=False)
        description = fields.String(required=True, allow_none=False)
        @post_load
        def post_load(self, data, many, partial):
            return InvoiceStatus(**data)


class Invoice(BasicValue):
    def __init__(self,
                 id: int,
                 amount: int,
                 status: InvoiceStatus,
                 creation_date: CreationDate = None,
                 plan: Plan = None,
                 items: List[InvoiceItem] = None,
                 subscription_code: str = None,
                 occurrence: int = None,
                 customer: Subscriber = None):
        super(Invoice, self).__init__()
        self.id = id
        self.amount = amount
        self.status = status
        self.creation_date = creation_date,
        self.plan = plan
        self.items = items
        self.subscription_code = subscription_code
        self.occurrence = occurrence
        self.customer = customer

    @classmethod
    def object_name(cls):
        return 'invoices'

    class Schema(BasicValue.Schema):
        id = fields.Integer(required=True, allow_none=False)
        amount = fields.Integer(required=True, allow_none=False)
        status = fields.Nested(
            InvoiceStatus.Schema,
            required=True,
            allow_none=False)
        creation_date = fields.Nested(
            CreationDate.Schema,
            required=False,
            allow_none=True)
        plan = fields.Nested(Plan.Schema, required=False, allow_none=True)
        items = fields.Nested(
            InvoiceItem.Schema,
            required=False,
            allow_none=True,
            many=True)
        subscription_code = fields.String(required=False, allow_none=True)
        occurrence = fields.Integer(required=False, allow_none=True)
        customer = fields.Nested(
            Subscriber.Schema,
            required=False,
            allow_none=True)

        @post_load
        def post_load(self, data, many, partial):
            return Invoice(**data)
