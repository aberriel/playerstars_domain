from abc import abstractmethod
from clapy_basic_classes import BasicValue
from datetime import datetime
from enum import Enum
from marshmallow import fields, post_load
from marshmallow_enum import EnumField
from operator import attrgetter
from playerstars_domain.product import ProductPurchased
from typing import List


class PaymentGateway(Enum):
    PAYPAL = 'PAYPAL'
    PAGSEGURO = 'PAGSEGURO'
    WIRECARD = 'WIRECARD'
    GOOGLE = 'GOOGLE'
    IOS = 'IOS'


class PagSeguroStatus(Enum):
    AWAITING_PAYMENT = 'AWAITING_PAYMENT'
    UNDER_REVIEW = 'UNDER_REVIEW'
    PAID = 'PAID'
    AVAILABLE = 'AVAILABLE'
    IN_DISPUTE = 'IN_DISPUTE'
    RETURNED = 'RETURNED'
    CANCELED = 'CANCELED'
    DEBITED = 'DEBITED'
    TEMPORARY_RETENTION = 'TEMPORARY_RETENTION'
    PROCESSING_CHARGEBACK = 'PROCESSING_CHARGEBACK'
    PRE_AUTHORIZED = 'PRE_AUTHORIZED'
    BLOCKED = 'BLOCKED'

    @staticmethod
    def get_from_int(x: int):
        tuples_list = {
            1: PagSeguroStatus.AWAITING_PAYMENT,
            2: PagSeguroStatus.UNDER_REVIEW,
            3: PagSeguroStatus.PAID,
            4: PagSeguroStatus.AVAILABLE,
            5: PagSeguroStatus.IN_DISPUTE,
            6: PagSeguroStatus.RETURNED,
            7: PagSeguroStatus.CANCELED,
            8: PagSeguroStatus.DEBITED,
            9: PagSeguroStatus.TEMPORARY_RETENTION,
            10: PagSeguroStatus.PROCESSING_CHARGEBACK,
            11: PagSeguroStatus.PRE_AUTHORIZED,
            12: PagSeguroStatus.BLOCKED,
        }
        return tuples_list[x]


class PurchaseType(Enum):
    SUBSCRIPTION = 'SUBSCRIPTION'
    GOLDEN_STAR_PURCHASE = 'GOLDEN_STAR_PURCHASE'


class Payment(BasicValue):
    payment_datetime = None
    code = None
    payment_type = None

    def __init__(self,
                 code: str,
                 payment_datetime: datetime = datetime.utcnow(),
                 payment_type: PaymentGateway = PaymentGateway.PAGSEGURO):
        super(Payment, self).__init__()
        self.payment_datetime = payment_datetime
        self.code = code
        self.payment_type = payment_type

    @abstractmethod
    def get_last_transaction(self):
        pass

    class Schema(BasicValue.Schema):
        payment_datetime = fields.DateTime(
            format='iso',
            required=True,
            allow_none=False)
        code = fields.String(required=True, allow_none=False)
        payment_type = EnumField(
            PaymentGateway,
            required=True,
            allow_none=False,
            default=PaymentGateway.PAGSEGURO)

        @post_load
        def post_load(self, data, many, partial):
            return Payment(**data)


class PagSeguroPaymentTransaction(BasicValue):

    def __init__(self,
                 code: str,
                 status: PagSeguroStatus = PagSeguroStatus.AWAITING_PAYMENT,
                 transaction_datetime: datetime = datetime.utcnow()):
        super(PagSeguroPaymentTransaction, self).__init__()
        self.code = code
        self.status = status
        self.transaction_datetime = transaction_datetime

    class Schema(BasicValue.Schema):
        code = fields.String(required=True, allow_none=False)
        status = EnumField(
            PagSeguroStatus,
            required=True,
            allow_none=False,
            by_value=True,
            default=PagSeguroStatus.AWAITING_PAYMENT)
        transaction_datetime = fields.DateTime(
            format='iso',
            required=True,
            allow_none=False)

        @post_load
        def post_load(self, data, many, partial):
            return PagSeguroPaymentTransaction(**data)


class PagSeguroPayment(Payment):
    transactions = []

    def __init__(self,
                 code: str,
                 payment_datetime: datetime = datetime.utcnow(),
                 transactions: List[PagSeguroPaymentTransaction] = None,
                 payment_type: PaymentGateway = PaymentGateway.PAGSEGURO):
        super(Payment, self).__init__()
        self.payment_type = payment_type
        self.code = code
        self.payment_datetime = payment_datetime
        self.transactions = transactions or []

    def get_last_transaction(self):
        return max(self.transactions,
                   key=attrgetter('transaction_datetime')) \
            if self.transactions else None

    def add_transaction(self, status, transaction_datetime, code):
        transaction = PagSeguroPaymentTransaction(
            transaction_datetime=transaction_datetime,
            code=code,
            status=status
        )
        self.transactions.append(transaction)

    def find_transaction_by_code(self, code):
        transaction_found = next((x for x in self.transactions
                                  if x.code == code),
                                 None)
        return transaction_found

    class Schema(Payment.Schema):
        transactions = fields.Nested(
            PagSeguroPaymentTransaction.Schema,
            many=True,
            default=list(),
            missing=list())

        @post_load
        def post_load(self, data, many, partial):
            return PagSeguroPayment(**data)


class Purchase(BasicValue):
    purchase_datetime = None
    purchase_type = None
    value: int = None
    star_value: int = None
    payment = None

    def __init__(self,
                 product: ProductPurchased,
                 payment: Payment,
                 purchase_datetime: datetime = datetime.utcnow(),
                 purchase_type: PurchaseType =
                 PurchaseType.GOLDEN_STAR_PURCHASE):
        super(Purchase, self).__init__()
        self.product = product
        self.payment = payment
        self.purchase_type = purchase_type
        self.purchase_datetime = purchase_datetime

    def get_last_status(self):
        if self.payment.get_last_transaction():
            return self.payment.get_last_transaction().status
        return None

    class Schema(BasicValue.Schema):
        purchase_datetime = fields.DateTime(
            format='iso',
            required=True,
            allow_none=False)
        purchase_type = EnumField(
            PurchaseType,
            required=True,
            allow_none=False,
            default=PurchaseType.GOLDEN_STAR_PURCHASE)
        product = fields.Nested(
            ProductPurchased.Schema,
            many=False,
            required=True,
            allow_none=False)
        payment = fields.Nested(PagSeguroPayment.Schema, many=False)

        @post_load
        def post_load(self, data, many, partial):
            return Purchase(**data)
