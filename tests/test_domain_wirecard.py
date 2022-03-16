from datetime import date, datetime
from playerstars_domain.wirecard import (
    CreationDate,
    Invoice,
    NextInvoiceDate,
    Plan,
    Subscriber,
    Subscription)

import pytz


plan_json = {
    "setup_fee": 0,
    "amount": 2000,
    "code": "red_star_month",
    "description": "Assinatura premium mensal",
    "creation_date": {"month": 8, "hour": 0, "year": 2020, "day": 21, "minute": 0, "second": 0},
    "max_qty": 1,
    "trial": {
        "hold_setup_fee": True,
        "days": 30,
        "enabled": False
    },
    "name": "Red Star Mensal",
    "billing_cycles": 0,
    "interval": {"unit": "MONTH", "length": 1},
    "id": "PLA-63N1LCA9RXPK",
    "payment_method": "CREDIT_CARD",
    "status": "ACTIVE"
}


subscriber_json = {
    "code": "cliente05",
    "email": "luan.garcia@stormgroup.com.br",
    "fullname": "Luan Garcia",
    "cpf": "67923846740",
    "phone_area_code": "21",
    "phone_number": "991193027",
    "birthdate_day": "26",
    "birthdate_month": "04",
    "birthdate_year": "1980",
    "address": {
        "street": "Rua José de Figueiredo",
        "number": "320",
        "complement": "Unidades 29 e 30",
        "district": "Barra da Tijuca",
        "city": "Rio de Janeiro",
        "state": "RJ",
        "country": "BRA",
        "zipcode": "22793-170"
    },
    "billing_info": {
        "credit_card": {
            "holder_name": "LUAN GARCIA",
            "number": "4012001037141112",
            "expiration_month": "06",
            "expiration_year": "22"
        }
    }
}


subscriber_full_json = {
    "creation_time": "00:00:00",
    "code": "client002",
    "address": {
        "zipcode": "22793-170",
        "number": "320",
        "country": "BRA",
        "city": "Rio de Janeiro",
        "street": "Rua José de Figueiredo",
        "district": "Barra da Tijuca",
        "state": "RJ",
        "complement": "Unidades 29 e 30"
    },
    "birthdate_year": 1986,
    "creation_date": "21/08/2020",
    "birthdate_month": "12",
    "billing_info": {
        "credit_cards": [
            {
                "first_six_digits": "555566",
                "expiration_year": "22",
                "expiration_month": "12",
                "last_four_digits": "8884",
                "brand": "MASTERCARD",
                "vault": "CRC-RCKTEE1OO53A",
                "holder_name": "ANSELMO B LIRA"
            }
        ]
    },
    "cpf": "77956135001",
    "phone_number": "71623026",
    "id": "CUS-5VKHD2QPZLBB",
    "fullname": "Anselmo Berriel de Lira",
    "birthdate_day": 16,
    "email": "anselmo.lira1@gmail.com",
    "phone_area_code": "21"
}


invoice_json = {
    "subscription_code": "subscription002",
    "amount": 2000,
    "id": 22311479,
    "creation_date": {
        "month": 8,
        "hour": 22,
        "year": 2020,
        "day": 21,
        "minute": 0,
        "second": 3
    },
    "occurrence": 1,
    "plan": {"code": "red_star_month", "name": "Red Star Mensal"},
    "items": [
        {"amount": 2000, "type": "Valor da assinatura"},
        {"amount": 0, "type": "Taxa de contratação"}
    ],
    "customer": {
        "code": "client002",
        "fullname": "Anselmo Berriel de Lira",
        "email": "anselmo.lira1@gmail.com"
    },
    "status": {"code": 5, "description": "Atrasada"}
}


subscription_json = {
    "amount": 2000,
    "code": "subscription002",
    "moip_account": "MPA-F646F68B8B46",
    "id": "SUB-YGP6Q91SDG8B",
    "creation_date": {
        "month": 8,
        "hour": 22,
        "year": 2020,
        "day": 21,
        "minute": 0,
        "second": 3
    },
    "invoice": {
        "amount": 2000,
        "id": 22311479,
        "status": {
            "code": 5,
            "description": "Atrasada"
        }
    },
    "plan": {
        "code": "red_star_month",
        "name": "Red Star Mensal",
        "id": "PLA-63N1LCA9RXPK"
    },
    "next_invoice_date": {
        "month": 9,
        "year": 2020,
        "day": 21
    },
    "payment_method": "CREDIT_CARD",
    "status": "OVERDUE",
    "customer": {
        "code": "client002",
        "billing_info": {
            "credit_card": {
                "first_six_digits": "555566",
                "expiration_year": "22",
                "expiration_month": "12",
                "last_four_digits": "8884",
                "brand": "MASTERCARD",
                "vault": "CRC-RCKTEE1OO53A",
                "holder_name": "ANSELMO B LIRA"
            }
        },
        "fullname": "Anselmo Berriel de Lira",
        "id": "CUS-5VKHD2QPZLBB",
        "email": "anselmo.lira1@gmail.com"
    }
}

subscription_json_2 = {
    "amount": 2000,
    "code": "assinatura223",
    "creation_date": {
        "month": 8,
        "hour": 20,
        "year": 2020,
        "day": 25,
        "minute": 44,
        "second": 55
    },
    "message": "Assinatura criada com sucesso",
    "alerts": [],
    "moip_account": "MPA-F646F68B8B46",
    "id": "SUB-LLW9JWC0YBC5",
    "invoice": {
        "amount": 2000,
        "id": 22366385,
        "status": {"code": 1, "description": "Em aberto"}
    },
    "plan": {
        "code": "red_star_month",
        "name": "Red Star Mensal",
        "id": "PLA-63N1LCA9RXPK"
    },
    "next_invoice_date": {"month": 9, "year": 2020, "day": 25},
    "errors": [],
    "payment_method": "CREDIT_CARD",
    "status": "ACTIVE",
    "customer": {
        "code": "client236",
        "billing_info": {
            "credit_card": {
                "first_six_digits": "376449",
                "expiration_year": "22",
                "expiration_month": "06",
                "last_four_digits": "3005",
                "brand": "AMEX",
                "vault": "CRC-0OVEMLBVIK4N",
                "holder_name": "LUAN GARCIA SILVA"
            }
        },
        "fullname": "Luan Garcia da Silva",
        "id": "CUS-LMEJVKTXDJ1Q",
        "email": "luan.garcia@stormgroup.com.br"
    }
}


def test_plan_from_json():
    entity: Plan = Plan.from_json(plan_json)
    assert entity.id == 'PLA-63N1LCA9RXPK'
    assert entity.code == 'red_star_month'
    assert entity.amount == 2000


def test_subscriber_from_json():
    entity: Subscriber = Subscriber.from_json(subscriber_json)
    assert entity.code == 'cliente05'
    assert entity.cpf == '67923846740'
    assert entity.billing_info.credit_card.number == '4012001037141112'


def test_subscriber_with_birthdate_object():
    subscriber = Subscriber(
        code='client01',
        fullname='Anselmo Lira',
        birthdate=date(1986, 12, 16))

    assert subscriber
    assert subscriber.birthdate_day == '16'
    assert subscriber.birthdate_month == '12'
    assert subscriber.birthdate_year == '1986'


def test_subscriber_full_from_json():
    entity: Subscriber = Subscriber.from_json(subscriber_full_json)
    assert entity.code == 'client002'
    assert entity.cpf == '77956135001'
    assert not entity.billing_info.credit_card
    assert entity.billing_info.credit_cards
    assert len(entity.billing_info.credit_cards) == 1

    card_info = entity.billing_info.credit_cards[0]
    assert card_info.first_six_digits == '555566'
    assert card_info.brand == 'MASTERCARD'


def test_subscriber_prepate_to_update():
    entity: Subscriber = Subscriber.from_json(subscriber_full_json)
    assert entity.id == 'CUS-5VKHD2QPZLBB'

    entity.prepate_to_update_customer()
    assert not entity.id


def test_invoice_from_json():
    entity: Invoice = Invoice.from_json(invoice_json)
    assert entity.id == 22311479
    assert entity.amount == 2000
    assert entity.subscription_code == 'subscription002'


def test_subscription_from_json():
    entity: Subscription = Subscription.from_json(subscription_json)
    assert entity.code == 'subscription002'
    assert entity.moip_account == 'MPA-F646F68B8B46'
    assert entity.id == 'SUB-YGP6Q91SDG8B'
    assert entity.amount == 2000


def test_subscription_from_json_2():
    entity: Subscription = Subscription.from_json(subscription_json_2)
    assert entity.code == 'assinatura223'


def test_object_names():
    assert Invoice.object_name() == 'invoices'
    assert Plan.object_name() == 'plans'
    assert Subscriber.object_name() == 'customers'
    assert Subscription.object_name() == 'subscriptions'


def test_plan_post_params():
    post_params = Plan.post_params()
    assert post_params is None


def test_plan_post_put_returns_object():
    check = Plan.post_put_returns_object()
    assert not check


def test_subscriber_post_put_returns_object():
    check = Subscriber.post_put_returns_object()
    assert not check


def test_subscription_post_put_returns_object():
    check = Subscription.post_put_returns_object()
    assert check


def test_next_invoice_as_date():
    next_invoice_date = NextInvoiceDate(2020, 8, 10)
    assert next_invoice_date.next_invoice_as_date == date(2020, 8, 10)


def test_next_invoice_as_datetime():
    next_invoice_datetime = NextInvoiceDate(2020, 8, 10)
    assert next_invoice_datetime.next_invoice_as_datetime == \
        datetime(2020, 8, 10, 0, 0, 0, tzinfo=pytz.utc)


def test_creation_date_as_datetime():
    creation_date = CreationDate(2020, 8, 10, 12, 13, 14)
    assert creation_date.creation_date_as_datetime == \
        datetime(2020, 8, 10, 12, 13, 14, tzinfo=pytz.utc)
