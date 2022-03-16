from .creation_date import CreationDate
from clapy_basic_classes import BasicValue
from enum import Enum
from marshmallow import fields, post_load
from marshmallow_enum import EnumField


class IntervalUnit(Enum):
    DAY = 'DAY'
    MONTH = 'MONTH'
    YEAR = 'YEAR'


class PlanStatus(Enum):
    ACTIVE = 'ACTIVE'
    INACTIVE = 'INACTIVE'


class PaymentMethod(Enum):
    BOLETO = 'BOLETO'
    CREDIT_CARD = 'CREDIT_CARD'
    ALL = 'ALL'


class Interval(BasicValue):
    def __init__(self,
                 length: int = 1,
                 unit: IntervalUnit = IntervalUnit.MONTH):
        super(Interval, self).__init__()
        self.length = length
        self.unit = unit

    class Schema(BasicValue.Schema):
        length = fields.Integer(required=True, allow_none=False, default=1)
        unit = EnumField(
            IntervalUnit,
            required=True,
            allow_none=False,
            default=IntervalUnit.MONTH)

        @post_load
        def post_load(self, data, many, partial):
            return Interval(**data)


class Trial(BasicValue):
    def __init__(self,
                 days: int,
                 enabled: bool = False,
                 hold_setup_fee: bool = False):
        super(Trial, self).__init__()
        self.days = days
        self.enabled = enabled
        self.hold_setup_fee = hold_setup_fee

    class Schema(BasicValue.Schema):
        days = fields.Integer(required=True, allow_none=False)
        enabled = fields.Boolean(
            required=True,
            allow_none=False,
            default=False)
        hold_setup_fee = fields.Boolean(
            required=False,
            allow_none=True,
            default=False)

        @post_load
        def post_load(self, data, many, partial):
            return Trial(**data)


class Plan(BasicValue):
    def __init__(self,
                 code: str,
                 name: str = None,
                 id: str = None,
                 amount: int = None,
                 interval: Interval = None,
                 status: PlanStatus = None,
                 payment_method: PaymentMethod = None,
                 description: str = None,
                 setup_fee: int = None,
                 max_qty: int = None,
                 billing_cycles: int = None,
                 trial: Trial = None,
                 creation_date: CreationDate = None):
        super(Plan, self).__init__()
        self.code = code
        self.name = name
        self.id = id
        self.description = description
        self.amount = amount
        self.setup_fee = setup_fee
        self.max_qty = max_qty
        self.interval = interval
        self.billing_cycles = billing_cycles
        self.trial = trial
        self.payment_method = payment_method
        self.status = status
        self.creation_date = creation_date

    @classmethod
    def object_name(cls):
        return 'plans'

    @classmethod
    def post_params(cls):
        return None

    @classmethod
    def post_put_returns_object(cls):
        return False

    class Schema(BasicValue.Schema):
        id = fields.String(required=False, allow_none=True)
        code = fields.String(required=True, allow_none=False)
        name = fields.String(required=False, allow_none=True)
        description = fields.String(required=False, allow_none=True)
        amount = fields.Integer(required=False, allow_none=True)
        setup_fee = fields.Integer(required=False, allow_none=True)
        max_qty = fields.Integer(required=False, allow_none=True)
        interval = fields.Nested(
            Interval.Schema,
            required=False,
            allow_none=True)
        billing_cycles = fields.Integer(required=False, allow_none=True)
        trial = fields.Nested(Trial.Schema, required=False, allow_none=True)
        payment_method = EnumField(
            PaymentMethod,
            required=False,
            allow_none=True)
        status = EnumField(
            PlanStatus,
            required=False,
            allow_none=True)
        creation_date = fields.Nested(
            CreationDate.Schema,
            required=False,
            allow_none=True)

        @post_load
        def post_load(self, data, many, partial):
            return Plan(**data)
