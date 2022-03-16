from clapy_basic_classes import BasicValue
from datetime import datetime
from marshmallow import fields, post_load
from playerstars_domain.player.payment_log import PaymentLog
from playerstars_domain.player.player_subscription import \
    PlayerSubscription
from playerstars_domain.player.purchase import PaymentGateway
from playerstars_domain.utils.datetime_helper import aware_utc


class GooglePurchase(BasicValue):
    def __init__(self,
                 orderId: str,
                 productId: str,
                 purchaseTime: int,
                 expirationDateTime: datetime,
                 purchaseState: int,
                 packageName: str = None,
                 acknowledged: bool = None,
                 autoRenewing: bool = True,
                 purchaseToken: str = None):
        self.orderId = orderId
        self.productId = productId
        self.purchaseTime = purchaseTime
        self.expirationDateTime = expirationDateTime
        self.purchaseState = purchaseState
        self.packageName = packageName
        self.acknowledged = acknowledged
        self.autoRenewing = autoRenewing
        self.purchaseToken = purchaseToken

    def mount_subscription(self):
        return PlayerSubscription(
            expiration_date=self.expirationDateTime,
            payment_gateway=PaymentGateway.GOOGLE,
            plan_name=self.productId)

    def mount_payment_log(self):
        transaction_date = datetime.fromtimestamp(self.purchaseTime / 1000)
        return PaymentLog(
            transaction_date=aware_utc(transaction_date),
            payment_gateway=PaymentGateway.GOOGLE,
            raw_received_data=str(self.to_json()))

    class Schema(BasicValue.Schema):
        orderId = fields.String(required=True, allow_none=False)
        productId = fields.String(required=True, allow_none=False)
        purchaseTime = fields.Integer(required=True, allow_none=False)
        expirationDateTime = fields.AwareDateTime(
            format='iso',
            required=True,
            allow_none=False)
        purchaseState = fields.Integer(required=True, allow_none=False)
        packageName = fields.String(required=False, allow_none=True)
        acknowledged = fields.Boolean(required=False, allow_none=True)
        autoRenewing = fields.Boolean(required=False, allow_none=True)
        purchaseToken = fields.String(required=False, allow_none=True)

        @post_load
        def post_load(self, data, many, partial):
            return GooglePurchase(**data)
