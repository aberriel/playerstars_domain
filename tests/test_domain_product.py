from playerstars_domain.product import (
    Product,
    ProductPurchased,
    RecurrenceInterval,
    TrialInfo)
from tests.util import generic_serialize_roundtrip_test

product = Product(
    name='product1',
    price=1234,
    description='schrubles',
    star_value=5,
    star_type='red')


def test_create_product():
    assert product


def test_product_from_json():
    assert Product.from_json({
        'price': 1234,
        'description': 'gluglu',
        'entity_id': 'idaisuas',
        'star_value': 5,
        'star_type': 'gold',
        'duration': 3,
        'name': 'Product1'
    })


def test_product_roundtrip():
    generic_serialize_roundtrip_test(Product, product)


product_purchased = ProductPurchased(
    price=product.price,
    description=product.description,
    star_value=product.star_value,
    star_type=product.star_type,
    duration=product.duration)


def test_product_purchased():
    assert product_purchased


def test_product_purchased_from_json():
    assert ProductPurchased.from_json({
        'price': 12345,
        'description': 'yeahyeah',
        'star_value': 6,
        'star_type': 'red',
        'duration': 999,
        'name': 'product01'})


def test_product_purchased_roundtrip():
    generic_serialize_roundtrip_test(
        ProductPurchased,
        product_purchased)


recurrence_interval = RecurrenceInterval(unit='MONTH', length=1)


trial_info = TrialInfo(period=30, enabled=True, hold_setup_fee=True)


def test_recurrence_interval_equals():
    recurrence_interval_1 = RecurrenceInterval('MONTH', 1)
    recurrence_interval_2 = RecurrenceInterval('MONTH', 1)
    recurrence_interval_3 = RecurrenceInterval('DAY', 15)

    assert recurrence_interval_1 == recurrence_interval_2
    assert not recurrence_interval_2 == recurrence_interval_3


def test_recurrence_interval_roundtrip():
    generic_serialize_roundtrip_test(RecurrenceInterval, recurrence_interval)


def test_trial_info_roundtrip():
    generic_serialize_roundtrip_test(TrialInfo, trial_info)
