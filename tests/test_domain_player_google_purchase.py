from datetime import datetime
from playerstars_domain.player.google_purchase import GooglePurchase
from playerstars_domain.player.payment_log import PaymentLog
from playerstars_domain.player.player_subscription import \
    PlayerSubscription
from playerstars_domain.player.purchase import PaymentGateway
from playerstars_domain.utils.datetime_helper import aware_utc
from tests.util import generic_serialize_roundtrip_test

import ast


def mount_google_purchase_json():
    return {
        'acknowledged': False,
        'autoRenewing': True,
        'orderId': 'GPA.3379-9115-5973-92808',
        'packageName': 'br.com.playerstars',
        'productId': 'redstar_mensal',
        'purchaseState': 1,
        'purchaseTime': 1598652324781,
        'expirationDateTime': '2020-08-31T13:14:15+00:00',
        'purchaseToken': 'meacoclalfocbmknlpffckij.AO-J1Owi8nc4IA4kxnHRu1DN'
                         'w_3-FGYC0sEeLOVzp1RF2Fy5f2hUOWnnrWq_gQX87ZHW-fDaN'
                         'RLoGhAZPjxzDKaMFCdjBUQERbDlEwzyVtGLztnUEb85EmlJVy'
                         'K951772Terk3Pp0g8S'
    }


def mount_google_purchase():
    expiration_datetime = datetime(2020, 8, 31, 13, 14, 15)
    return GooglePurchase(
        orderId='GPA.3379-9115-5973-92808',
        acknowledged=False,
        autoRenewing=True,
        packageName='br.com.playerstars',
        productId='redstar_mensal',
        purchaseState=1,
        purchaseTime=1598652324781,
        expirationDateTime=aware_utc(expiration_datetime),
        purchaseToken='meacoclalfocbmknlpffckij.AO-J1Owi8nc4IA4kxnHRu1DNw_3-'
                      'FGYC0sEeLOVzp1RF2Fy5f2hUOWnnrWq_gQX87ZHW-fDaNRLoGhAZP'
                      'jxzDKaMFCdjBUQERbDlEwzyVtGLztnUEb85EmlJVyK951772Terk3'
                      'Pp0g8S')


def test_google_purchase_from_json():
    obj_to_compare = mount_google_purchase()
    obj = GooglePurchase.from_json(mount_google_purchase_json())
    assert obj == obj_to_compare


def test_google_purchase_roundtrip():
    generic_serialize_roundtrip_test(GooglePurchase, mount_google_purchase())


def test_mount_payment_log_from_google_purchase():
    purchase = mount_google_purchase()
    payment_log: PaymentLog = purchase.mount_payment_log()
    payment_log_to_compare = PaymentLog(
        transaction_date=aware_utc(datetime(2020, 8, 28, 19, 5, 24, 781000)),
        payment_gateway=PaymentGateway.GOOGLE,
        raw_sent_data=None,
        raw_received_data=str(mount_google_purchase_json()))
    assert payment_log.payment_gateway == payment_log_to_compare.payment_gateway
    assert ast.literal_eval(payment_log.raw_received_data) == \
        ast.literal_eval(payment_log_to_compare.raw_received_data)
    assert payment_log.raw_sent_data == payment_log_to_compare.raw_sent_data


def test_mount_player_subscription_from_google_purchase():
    purchase = mount_google_purchase()
    expiration_datetime = aware_utc(datetime(2020, 8, 31, 13, 14, 15))
    subscription: PlayerSubscription = purchase.mount_subscription()
    subscription_to_compare = PlayerSubscription(
        expiration_date=expiration_datetime,
        payment_gateway=PaymentGateway.GOOGLE,
        plan_name='redstar_mensal')
    assert subscription == subscription_to_compare
