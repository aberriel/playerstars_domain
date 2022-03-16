from clapy_basic_classes import BasicValue
from enum import Enum
from marshmallow import fields, post_load


class WirecardNotificationEvent(Enum):
    PLAN_CREATED = 'plan.created'
    PLAN_UPDATED = 'plan.updated'
    PLAN_ACTIVATED = 'plan.activated'
    PLAN_INACTIVATED = 'plan.inactivated'

    CUSTOMER_CREATED = 'customer.created'
    CUSTOMER_UPDATED = 'customer.updated'

    SUBSCRIPTION_CREATED = 'subscription.created'
    SUBSCRIPTION_UPDATED = 'subscription.updated'
    SUBSCRIPTION_ACTIVATED = 'subscription.activated'
    SUBSCRIPTION_SUSPENDED = 'subscription.suspended'
    SUBSCRIPTION_CANCELED = 'subscription.canceled'
    SUBSCRIPTION_MIGRATED = 'subscription.migrated'

    INVOICE_CREATED = 'invoice.created'
    INVOICE_STATUS_UPDATED = 'invoice.status_updated'

    PAYMENT_CREATED = 'payment.created'
    PAYMENT_STATUS_UPDATED = 'payment.status_updated'


class BasicWebhook(BasicValue):
    def __init__(self,
                 date: str,
                 env: str,
                 event: str):
        self.date = date
        self.env = env
        self.event = event

    @property
    def event_type(self):
        return WirecardNotificationEvent(self.event)

    class Schema(BasicValue.Schema):
        date = fields.String(required=True, allow_none=False)
        env = fields.String(required=True, allow_none=False)
        event = fields.String(required=True, allow_none=False)

        @post_load
        def post_load(self, data, many, partial):
            return BasicWebhook(**data)
