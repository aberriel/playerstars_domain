from playerstars_domain import (
    BasicWebhook,
    InvoiceWebhook,
    PaymentWebhook,
    PlanStatus,
    PlanWebHook,
    SubscriberWebhook,
    SubscriptionStatus,
    SubscriptionWebhook,
    WirecardNotificationEvent)


webhook_customer_created = {
    "date": "22/08/2020 18:34:50",
    "env": "sandbox",
    "event": "customer.created",
    "resource": {
        "address": {
            "city": "Rio de Janeiro",
            "complement": "Unidades 29 e 30",
            "country": "BRA",
            "district": "Barra da Tijuca",
            "number": "320",
            "state": "RJ",
            "street": "Rua José de Figueiredo",
            "zipcode": "22793-170"
        },
        "billing_info": {
            "credit_cards": [
                {
                    "brand": "VISA",
                    "expiration_month": "06",
                    "expiration_year": "22",
                    "first_six_digits": "401200",
                    "holder_name": "LUAN GARCIA",
                    "last_four_digits": "1112",
                    "vault": "CRC-6Z7AD03NPI36"
                }
            ]
        },
        "birthdate_day": 26,
        "birthdate_month": "04",
        "birthdate_year": 1980,
        "code": "cliente05",
        "document": "67923846740",
        "document_type": "CPF",
        "email": "luan.garcia@stormgroup.com.br",
        "fullname": "Luan Garcia",
        "phone_area_code": "21",
        "phone_number": "91193027"
    }
}


webhook_customer_updated = {
    "date": "24/08/2020 02:29:59",
    "env": "sandbox",
    "event": "customer.updated",
    "resource": {
        "address": {
            "city": "Rio de Janeiro",
            "complement": "Casa 134",
            "country": "BRA",
            "district": "Barra da Tijuca",
            "number": "122",
            "state": "RJ",
            "street": "Rua dos Alfeneiros",
            "zipcode": "22793170"
        },
        "billing_info": {
            "credit_cards": [
                {
                    "brand": "VISA",
                    "expiration_month": "06",
                    "expiration_year": "22",
                    "first_six_digits": "401200",
                    "holder_name": "LUAN GARCIA",
                    "last_four_digits": "1112",
                    "vault": "CRC-NZKU2AAJ3Z7P"
                }
            ]
        },
        "birthdate_day": 26,
        "birthdate_month": "04",
        "birthdate_year": 1980,
        "code": "client236",
        "document": "67923846740",
        "document_type": "CPF",
        "email": "luan.garcia@stormgroup.com.br",
        "fullname": "Luan Garcia da Silva",
        "phone_area_code": "21",
        "phone_number": "991193027"
    }
}

webhook_customer_billing_info_updated = {
    "date": "24/08/2020 02:38:14",
    "env": "sandbox",
    "event": "customer.updated",
    "resource": {
        "address": {
            "city": "Rio de Janeiro",
            "complement": "Casa 134",
            "country": "BRA",
            "district": "Barra da Tijuca",
            "number": "122",
            "state": "RJ",
            "street": "Rua dos Alfeneiros",
            "zipcode": "22793170"
        },
        "billing_info": {
            "credit_cards": [
                {
                    "brand": "ELO",
                    "expiration_month": "06",
                    "expiration_year": "22",
                    "first_six_digits": "636297",
                    "holder_name": "LUAN GARCIA SILVA",
                    "last_four_digits": "7013",
                    "vault": "CRC-Q0S73K9TGS2P"
                }
            ]
        },
        "birthdate_day": 26,
        "birthdate_month": "04",
        "birthdate_year": 1980,
        "code": "client236",
        "document": "67923846740",
        "document_type": "CPF",
        "email": "luan.garcia@stormgroup.com.br",
        "fullname": "Luan Garcia da Silva",
        "phone_area_code": "21",
        "phone_number": "991193027"
    }
}


webhook_invoice_created = {
    "date": "24/08/2020 02:45:19",
    "env": "sandbox",
    "event": "invoice.created",
    "resource": {
        "amount": 11000,
        "id": 22337447,
        "status": {"code": 1, "description": "Em aberto"},
        "subscription_code": "subscription01"
    }
}


webhook_invoice_status_updated = {
    "date": "24/08/2020 05:45:30",
    "env": "sandbox",
    "event": "invoice.status_updated",
    "resource": {
        "amount": 11000,
        "id": 22337447,
        "status": {"code": 5, "description": "Atrasada"},
        "subscription_code": "subscription01"
    }
}


webhook_payment_created = {
    "date": "24/08/2020 02:45:19",
    "env": "sandbox",
    "event": "payment.created",
    "resource": {
        "amount": 11000,
        "id": 30756970,
        "invoice_id": 22337447,
        "payment_method": {
            "code": 1,
            "credit_card": {
                "brand": "ELO",
                "first_six_digits": "636297",
                "holder_name": "LUAN GARCIA SILVA",
                "last_four_digits": "7013",
                "vault": "CRC-Q0S73K9TGS2P"
            },
            "description": "Cartão de Crédito"
        },
        "status": {"code": 2, "description": "Iniciado"},
        "subscription_code": "subscription01"
    }
}


webhook_payment_status_updated = {
    "date": "24/08/2020 05:45:30",
    "env": "sandbox",
    "event": "payment.status_updated",
    "resource": {
        "id": 30756970,
        "invoice_id": 22337447,
        "status": {"code": 5, "description": "Cancelado"},
        "subscription_code": "subscription01"
    }
}


webhook_plan_created = {
    "date": "21/08/2020 16:40:04",
    "env": "sandbox",
    "event": "plan.created",
    "resource": {
        "amount": 2000,
        "billing_cycles": 0,
        "code": "red_star_month",
        "description": "Assinatura premium mensal",
        "interval": {
            "length": 1,
            "unit": "MONTH"
        },
        "max_qty": 1,
        "name": "Red Star Mensal",
        "payment_method": "CREDIT_CARD",
        "setup_fee": 0,
        "status": "ACTIVE",
        "trial": {
            "days": 30,
            "enabled": False,
            "hold_setup_fee": True
        }
    }
}

webhook_plan_activated = {
    "date": "24/08/2020 02:15:02",
    "env": "sandbox",
    "event": "plan.activated",
    "resource": {"code": "red_star_yearly"}
}


webhook_plan_updated = {
    "date": "24/08/2020 02:18:55",
    "env": "sandbox",
    "event": "plan.updated",
    "resource": {
        "amount": 11000,
        "billing_cycles": 0,
        "code": "red_star_yearly",
        "description": "Assinatura premium anual 2",
        "interval": {"length": 1, "unit": "YEAR"},
        "max_qty": 1,
        "name": "Red Star Anual 2",
        "payment_method": "CREDIT_CARD",
        "setup_fee": 0,
        "status": "ACTIVE",
        "trial": {
            "days": 30,
            "enabled": False,
            "hold_setup_fee": True
        }
    }
}


webhook_subscription_created = {
    "date": "24/08/2020 02:45:20",
    "env": "sandbox",
    "event": "subscription.created",
    "resource": {
        "amount": 11000,
        "code": "subscription01",
        "creation_date": {
            "day": 24,
            "month": 8,
            "year": 2020
        },
        "customer": {
            "code": "client236"
        },
        "next_invoice_date": {"day": 24, "month": 8, "year": 2021},
        "payment_method": "CREDIT_CARD",
        "plan": {"code": "red_star_yearly"},
        "status": "ACTIVE"
    }
}


webhook_subscription_updated_overdue = {
    "date": "24/08/2020 05:45:30",
    "env": "sandbox",
    "event": "subscription.updated",
    "resource": {
        "amount": 11000,
        "code": "subscription01",
        "creation_date": {"day": 24, "month": 8, "year": 2020},
        "customer": {"code": "client236"},
        "next_invoice_date": {"day": 24, "month": 8, "year": 2021},
        "payment_method": "CREDIT_CARD",
        "plan": {"code": "red_star_yearly"},
        "status": "OVERDUE"
    }
}


def test_webhook_customer_created():
    webhook: SubscriberWebhook = SubscriberWebhook.from_json(webhook_customer_created)
    assert webhook
    assert webhook.event_type == WirecardNotificationEvent.CUSTOMER_CREATED
    assert webhook.resource.code == 'cliente05'
    assert webhook.resource.cpf == '67923846740'


def test_webhook_customer_updated():
    webhook: SubscriberWebhook = \
        SubscriberWebhook.from_json(webhook_customer_updated)
    assert webhook
    assert webhook.event_type == WirecardNotificationEvent.CUSTOMER_UPDATED
    assert webhook.resource.email == 'luan.garcia@stormgroup.com.br'


def test_webhook_customer_billing_info_updated():
    webhook: SubscriberWebhook = \
        SubscriberWebhook.from_json(webhook_customer_billing_info_updated)
    assert webhook
    assert webhook.event_type == WirecardNotificationEvent.CUSTOMER_UPDATED
    assert webhook.resource.cpf == '67923846740'
    assert webhook.resource.code == 'client236'


def test_webhook_invoice_created():
    webhook: InvoiceWebhook = \
        InvoiceWebhook.from_json(webhook_invoice_created)
    assert webhook
    assert webhook.event_type == WirecardNotificationEvent.INVOICE_CREATED
    assert webhook.resource.amount == 11000
    assert webhook.resource.subscription_code == 'subscription01'


def test_webhook_invoice_status_updated():
    webhook: InvoiceWebhook = \
        InvoiceWebhook.from_json(webhook_invoice_status_updated)
    assert webhook
    assert webhook.event_type == WirecardNotificationEvent.INVOICE_STATUS_UPDATED
    assert webhook.resource.id == 22337447


def test_webhook_payment_created():
    webhook: PaymentWebhook = \
        PaymentWebhook.from_json(webhook_payment_created)
    assert webhook
    assert webhook.event_type == WirecardNotificationEvent.PAYMENT_CREATED
    assert webhook.resource.invoice_id == 22337447


def test_webhook_payment_status_updated():
    webhook: PaymentWebhook = \
        PaymentWebhook.from_json(webhook_payment_status_updated)
    assert webhook
    assert webhook.event_type == WirecardNotificationEvent.PAYMENT_STATUS_UPDATED
    assert webhook.resource.id == 30756970


def test_webhok_plan_created():
    webhook: PlanWebHook = PlanWebHook.from_json(webhook_plan_created)
    assert webhook
    assert webhook.event_type == WirecardNotificationEvent.PLAN_CREATED
    assert webhook.resource.code == 'red_star_month'
    assert webhook.resource.status == PlanStatus.ACTIVE


def test_webhook_plan_activated():
    webhook: PlanWebHook = PlanWebHook.from_json(webhook_plan_activated)
    assert webhook
    assert webhook.event_type == WirecardNotificationEvent.PLAN_ACTIVATED
    assert webhook.resource.code == 'red_star_yearly'
    assert webhook.resource.id is None


def test_webhook_plan_updated():
    webhook: PlanWebHook = PlanWebHook.from_json(webhook_plan_updated)
    assert webhook
    assert webhook.event_type == WirecardNotificationEvent.PLAN_UPDATED
    assert webhook.resource.code == 'red_star_yearly'
    assert webhook.resource.status == PlanStatus.ACTIVE


def test_webhook_subscription_created():
    webhook: SubscriptionWebhook = \
        SubscriptionWebhook.from_json(webhook_subscription_created)
    assert webhook
    assert webhook.event_type == WirecardNotificationEvent.SUBSCRIPTION_CREATED
    assert webhook.resource.code == 'subscription01'
    assert webhook.resource.status == SubscriptionStatus.ACTIVE


def test_webhook_subscription_updated():
    webhook: SubscriptionWebhook = \
        SubscriptionWebhook.from_json(webhook_subscription_updated_overdue)
    assert webhook
    assert webhook.event_type == WirecardNotificationEvent.SUBSCRIPTION_UPDATED
    assert webhook.resource.code == 'subscription01'


def test_basic_webhook_from_json():
    webhook_json = {
        "date": "24/08/2020 02:15:02",
        "env": "sandbox",
        "event": "plan.activated"}
    webhook: BasicWebhook = BasicWebhook.from_json(webhook_json)
    assert webhook
    assert webhook.env == 'sandbox'
    assert webhook.event_type == WirecardNotificationEvent.PLAN_ACTIVATED
