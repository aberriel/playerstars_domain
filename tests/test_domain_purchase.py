from playerstars_domain import (
    Payment,
    Purchase,
    PagSeguroPayment,
    PagSeguroPaymentTransaction,
    ProductPurchased, PagSeguroStatus)

payment = Payment(code='schruvles1241')
product = ProductPurchased(
    price=1234,
    star_value=12,
    description='teste',
    star_type='gold',
    duration=0)

purchase = Purchase(product=product, payment=payment)


def test_create_payment():
    assert payment


def test_create_payment_from_json():
    assert Payment.from_json({
        'code': 'schrubles123',
        'payment_datetime': '2017-11-22T09:58:00+00:00',
        'payment_type': 'PAGSEGURO'})


def test_create_purchase():
    assert purchase


def test_get_last_status():
    assert purchase.get_last_status() is None
    purchase.payment = PagSeguroPayment(code='schrubles')
    purchase.payment.add_transaction('started', purchase.purchase_datetime, 'glubglub')
    last_status = purchase.get_last_status()
    assert last_status
    assert last_status == 'started'


def test_create_purchase_from_json():
    assert Purchase.from_json({
        'product': {
            'price': 1234,
            'star_value': 5,
            'description': 'teste',
            'star_type': 'gold',
            'duration': 0,
            'name': 'product01'
        },
        'purchase_type': 'GOLDEN_STAR_PURCHASE',
        'purchase_datetime': '2017-11-21T09:58:00+00:00',
        'payment': {
            'code': 'schrubles123',
            'payment_datetime': '2017-11-22T09:58:00+00:00',
            'payment_type': 'PAGSEGURO'
        }
    })


def test_create_pagseguro_payment_transaction_from_json():
    assert PagSeguroPaymentTransaction.from_json({
        'code': 'UQWYEQ81Y721HASBD',
        'status': 'AWAITING_PAYMENT',
        'transaction_datetime': '2017-11-22T09:58:00+00:00'
    })


def test_find_transaction_by_code():
    pagseguro_payment = PagSeguroPayment(code='glubglub')
    pagseguro_payment.add_transaction('started', purchase.purchase_datetime, 'glubglub')
    transaction = pagseguro_payment.find_transaction_by_code('glubglub')
    assert transaction
    assert transaction.status == 'started'


def test_pagseguro_payment_from_json():
    assert PagSeguroPayment.from_json({
        'code': 'schrubles123',
        'payment_datetime': '2017-11-22T09:58:00+00:00',
        'payment_type': 'PAGSEGURO'})


def test_pagseguro_status_enum():
    assert PagSeguroStatus.get_from_int(1).value == 'AWAITING_PAYMENT'
