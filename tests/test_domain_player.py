from copy import deepcopy
from datetime import date, datetime, timezone
from unittest import TestCase
from unittest.mock import MagicMock

from marshmallow.exceptions import ValidationError

from playerstars_domain import (
    CoinType, Console, CountryRegion, GamePoints, OperationType,
    PagSeguroPayment, PaymentGateway, Player,
    PlayerConsoles, PlayerStatus, PlayerSubscription,
    ProductPurchased, Purchase,
    SourceOperationType, StateRegion, StarReserve,
    StarTransaction, User)
from playerstars_domain.player import (
    CheckPlayerBalanceException,
    InsufficientGoldenStarsBalanceException,
    InsufficientRedStarsBalanceException,
    NegativeGoldenStarBalanceException,
    NegativeRedStarBalanceException,
    PaymentLog,
    PushNotificationData,
    StarReserveNotFoundException)
from playerstars_domain.player.elo import Elo
from playerstars_domain.utils.datetime_helper import aware_utc
from tests.util import (
    console_list, console_list_json, favorite_list, game_list,
    generic_serialize_roundtrip_test,
    player_with_consoles, player_without_consoles,
    player_with_star_transactions,
    star_transaction_list, star_transaction_list_json, user_data)
from uuid import uuid4

import pytest


def test_player():
    _user_data = User(
        name='Anselmo Lira',
        email='a.lira@stormsec',
        date_birth=date(1986, 12, 16),
        street='Avenida Brasil',
        street_number='500',
        street_complement='apt 607',
        neighborhood='pechinchão',
        city='Rio de Janeiro',
        state='Rio de Janeiro',
        country='Brasil',
        postal_code='25525-001',
        phone_number='(21) 2222-3333',
        cpf='123.456.789-01',
        nickname='zyzukab')

    player_data = Player(user=_user_data)
    assert player_data


def test_player_with_id():
    player_id = str(uuid4())
    player_data = Player(user=user_data(),
                         consoles=console_list(),
                         entity_id=player_id)
    assert player_data
    assert player_data.entity_id == player_id


def test_player_initial_data():
    player_data = Player(user=user_data())
    assert player_data.user is not None
    assert player_data.red_star_balance == 0
    assert player_data.golden_star_balance == 0

    assert player_data.consoles is not None
    assert len(player_data.consoles) == 0
    assert player_data.favorites is not None
    assert len(player_data.favorites) == 0


def test_player_repr():
    player_data = Player(user=user_data())
    assert str(player_data) == 'Anselmo Lira'


def test_update_stars_balance():
    player_data = player_without_consoles
    player_data.update_red_star_balance(30)
    assert player_data.red_star_balance == 30
    assert player_data.golden_star_balance == 0

    player_data.update_golden_star_balance(20)
    assert player_data.golden_star_balance == 20
    assert player_data.red_star_balance == 30


def test_invalid_red_star_balance():
    player_data = player_without_consoles
    with pytest.raises(NegativeRedStarBalanceException):
        player_data.update_red_star_balance(-1)


def test_invalid_golden_star_balance():
    player_data = player_without_consoles
    with pytest.raises(NegativeGoldenStarBalanceException):
        player_data.update_golden_star_balance(-1)


def test_add_console():
    player_data = player_without_consoles
    assert player_data.consoles is not None
    assert len(player_data.consoles) == 0

    console_1 = Console(name='Xbox One',
                        logo_path='/images/xbox_one.jpg',
                        tag_name='nick#1',
                        games=game_list())
    addiction_result_1 = player_data.add_console(console_1, 'schrubles')
    assert addiction_result_1
    assert len(player_data.consoles) == 1
    assert console_1.entity_id == player_data.consoles[0].console_id

    console_2 = Console(name='Master System',
                        logo_path='/images/master_system.jpg',
                        tag_name='nick#2',
                        games=game_list())
    addiction_result_2 = player_data.add_console(console_2, 'schrubles2')
    assert addiction_result_2
    assert len(player_data.consoles) == 2

    addiction_result_3 = player_data.add_console(console_1, 'schrubles3')
    assert not addiction_result_3
    assert len(player_data.consoles) == 2


def test_list_all_consoles():
    player_data = player_with_consoles
    _console_list = player_data.list_consoles()
    assert console_list is not None
    assert len(_console_list) == 4


def test_remove_console():
    player_data = player_without_consoles
    _console_list = console_list()
    player_data.consoles = _console_list
    assert player_data.consoles is not None
    assert len(player_data.consoles) == 4

    delete_result_1 = player_data.remove_console(_console_list[0].console_id)
    assert delete_result_1
    console_xbox_removed = \
        next((x for x in player_data.consoles
              if x.console_id == _console_list[0].console_id), None)
    assert console_xbox_removed is None

    delete_result_2 = player_data.remove_console(str(uuid4()))
    assert not delete_result_2


def test_premium_on():
    subscription = PlayerSubscription(
        payment_gateway=PaymentGateway.WIRECARD,
        plan_name='red_stars_monthly',
        expiration_date=aware_utc(datetime(2099, 12, 31, 23, 59, 59)))
    player_data = Player(user=user_data(), subscription=subscription)
    assert player_data.is_premium


def test_premium_off():
    subscription = PlayerSubscription(
        payment_gateway=PaymentGateway.WIRECARD,
        plan_name='red_stars_monthly',
        expiration_date=aware_utc(datetime(2012, 12, 31, 23, 59, 59)),)
    player_data = Player(user=user_data(), subscription=subscription)
    assert not player_data.is_premium


def test_initialize_with_favorites():
    player_data = Player(user=user_data(), favorites=favorite_list())
    assert player_data.favorites is not None
    assert len(player_data.favorites) == 3


def test_add_favorite():
    player_data = player_without_consoles
    assert player_data.favorites is not None
    assert len(player_data.favorites) == 0

    _favorite_list = favorite_list()
    player_data.add_favorite(_favorite_list[0])
    assert player_data.favorites is not None
    assert len(player_data.favorites) == 1
    assert player_data.favorites[0] == _favorite_list[0]

    player_data.add_favorite(_favorite_list[1])
    assert len(player_data.favorites) == 2

    player_data.add_favorite(_favorite_list[1])
    assert len(player_data.favorites) == 2


def test_player_find_favorite():
    player_duarte = favorite_list()
    player_data = Player(user=user_data(), favorites=player_duarte)
    assert player_data.favorites is not None
    assert len(player_data.favorites) == 3

    favorite_found_1 = player_data.find_favorite(player_duarte[0])
    assert favorite_found_1 is not None
    assert favorite_found_1 == player_duarte[0]

    favorite_found_2 = player_data.find_favorite('901823hjn1ed918238712ji12')
    assert favorite_found_2 is None


def test_player_list_all_favorites():
    favorite_list_orig = favorite_list()
    player_zero_orig = favorite_list_orig[0]
    player_one_orig = favorite_list_orig[1]
    player_data = Player(user=user_data(), favorites=favorite_list_orig)

    player_favorite_list = player_data.list_favorites()
    assert player_favorite_list is not None
    assert len(player_favorite_list) == 3
    assert player_zero_orig in player_favorite_list
    assert player_one_orig in player_favorite_list


def test_player_remove_favorite():
    player_duarte_orig = favorite_list()[0]
    player_data = Player(user=user_data(), favorites=favorite_list())

    player_data.remove_favorite(player_duarte_orig)
    assert len(player_data.favorites) == 3

    player_data.remove_favorite(str(uuid4()))
    assert len(player_data.favorites) == 3


def test_player_get_status():
    player_data = player_without_consoles
    assert player_data.get_status() == PlayerStatus.OFFLINE


def test_player_change_status():
    player_data = player_without_consoles
    assert player_data.get_status() == PlayerStatus.OFFLINE
    player_data.change_status('AVAILABLE')
    assert player_data.get_status() == PlayerStatus.AVAILABLE


def test_player_from_json():
    e_id = str(uuid4())
    json_data = dict(
        red_star_balance=0,
        golden_star_balance=0,
        player_status="OFFLINE",
        entity_id=e_id,
        countries_regions=[],
        states_regions=[],
        favorites=['alo'],
        consoles=console_list_json(),
        star_transactions=star_transaction_list_json(),
        points=2,
        subscription=dict(
            plan_name='red_stars_monthly',
            expiration_date='2099-12-31T00:00:00+00:00',
            payment_gateway='GOOGLE'),
        terms=True,
        star_reservations=[],
        user=dict(
            name='Anselmo Lira',
            email='alira@stormsec.com',
            date_birth='1986-10-12',
            street='Avenida Brasil',
            street_number='500',
            street_complement='apt 607',
            neighborhood='pechinchão',
            city="Rio de Janeiro",
            state="Rio de Janeiro",
            country="Brasil",
            postal_code="25525-001",
            phone_number='(21)2222-3333',
            cpf='11122233345',
            nickname='lerdinho'))
    entity = Player.from_json(json_data)
    assert entity
    assert entity.entity_id == e_id
    assert entity.user.name == 'Anselmo Lira'
    assert entity.red_star_balance == 0
    assert entity.favorites == ['alo']


def test_player_from_json_with_elo():
    e_id = str(uuid4())
    json_data = dict(
        red_star_balance=0,
        golden_star_balance=0,
        player_status="OFFLINE",
        entity_id=e_id,
        countries_regions=[],
        states_regions=[],
        favorites=['alo'],
        consoles=console_list_json(),
        star_transactions=star_transaction_list_json(),
        points=2,
        elo_rating=1500.5,
        subscription=dict(
            plan_name='red_stars_monthly',
            expiration_date='2099-12-31T00:00:00+00:00',
            payment_gateway='GOOGLE'),
        terms=True,
        star_reservations=[],
        user=dict(
            name='Anselmo Lira',
            email='alira@stormsec.com',
            date_birth='1986-10-12',
            street='Avenida Brasil',
            street_number='500',
            street_complement='apt 607',
            neighborhood='pechinchão',
            city="Rio de Janeiro",
            state="Rio de Janeiro",
            country="Brasil",
            postal_code="25525-001",
            phone_number='(21)2222-3333',
            cpf='11122233345',
            nickname='lerdinho'))
    entity = Player.from_json(json_data)
    assert entity
    assert entity.entity_id == e_id
    assert entity.user.name == 'Anselmo Lira'
    assert entity.red_star_balance == 0
    assert entity.favorites == ['alo']
    assert entity.elo_rating == 1500.5


def test_player_from_json_error():
    e_id = str(uuid4())
    with pytest.raises(ValidationError):
        json_data = dict(
            entity_id=e_id,
            name=000000,
            email='a.lira@stormsec',
            date_birth=date(1986, 12, 16),
            street='Avenida Brasil',
            street_number='500',
            street_complement='apt 607',
            neighborhood='pechinchão',
            city="Rio de Janeiro",
            state="Rio de Janeiro",
            country="Brasil",
            postal_code="25525-001",
            phone_number='(21)2222-3333',
            cpf='11122233345',
            nickname='lerdinho')
        Player.from_json(json_data)


def test_player_to_json():
    transaction_1 = StarTransaction(
        value=8,
        source_id='3a4b05bc-6fde-4936-bee1-e17162bc1048',
        operation_type=OperationType.CREDIT,
        coin_type=CoinType.RED_STAR,
        source=SourceOperationType.FINANCIAL_TRANSACTION,
        operation_date=datetime(2019, 2, 3, 13, 21, 45, tzinfo=timezone.utc))
    transaction_2 = StarTransaction(
        value=9,
        source_id='06f00cb9-304c-458b-9090-924e69eed5f4',
        operation_type=OperationType.CREDIT,
        coin_type=CoinType.GOLDEN_STAR,
        source=SourceOperationType.FINANCIAL_TRANSACTION,
        operation_date=datetime(2019, 2, 3, 13, 43, 21, tzinfo=timezone.utc))
    transaction_list = [transaction_1, transaction_2]

    payment_log_1 = PaymentLog(
        transaction_date=aware_utc(datetime(2020, 1, 1, 15, 16, 17)),
        payment_gateway=PaymentGateway.WIRECARD,
        raw_received_data="{'status': 'ACTIVE'}")
    payment_log_2 = PaymentLog(
        transaction_date=aware_utc(datetime(2020, 1, 1, 15, 16, 17)),
        payment_gateway=PaymentGateway.WIRECARD,
        raw_received_data="{'status': 'ACTIVE'}")
    payment_logs = [payment_log_1, payment_log_2]

    _user_data = User(
        name='Anselmo Lira',
        email='alira@stormsec.com',
        date_birth=date(1986, 12, 16),
        street='Avenida Brasil',
        street_number='500',
        street_complement='apt 607',
        neighborhood='pechinchão',
        city='Rio de Janeiro',
        state='Rio de Janeiro',
        country='Brasil',
        postal_code='25525-001',
        phone_number='(21) 2222-3333',
        cpf='123.456.789-01',
        nickname='lerdinho')
    country_region = CountryRegion(
        entity_id='65de565b-4395-4886-8e00-2314307e4e6b',
        name='regiao1',
        minimum_bet=3,
        countries=['Brasil', 'Argentina', 'Paraguai'])
    state_region = StateRegion(
        entity_id='36461459-b184-4316-b274-23316a7800c2',
        name='regiao2',
        minimum_bet=45,
        states=['Rio de Janeiro', 'São Paulo', 'Minas Gerais'])
    subscription = PlayerSubscription(
        expiration_date=aware_utc(datetime(2099, 12, 31, 0, 0, 0)),
        payment_gateway=PaymentGateway.WIRECARD,
        plan_name='red_stars_monthly')
    player_data = Player(
        entity_id='960710e9-eb92-43e4-9548-bf61b10cccf2',
        user=_user_data,
        red_star_balance=0,
        golden_star_balance=0,
        player_status=PlayerStatus.OFFLINE,
        countries_regions=[country_region.entity_id],
        states_regions=[state_region.entity_id],
        star_transactions=transaction_list,
        subscription=subscription,
        payment_logs=payment_logs,
        terms=True,
        star_reservations=[])
    expected_dict = dict(
        elo_rating=1500,
        red_star_balance=0,
        subscription=dict(plan_name='red_stars_monthly',
                          payment_gateway='WIRECARD',
                          expiration_date='2099-12-31T00:00:00+00:00'),
        golden_star_balance=0,
        points=0,
        player_status="OFFLINE",
        entity_id='960710e9-eb92-43e4-9548-bf61b10cccf2',
        consoles=[],
        favorites=[],
        purchases=[],
        star_reservations=[],
        terms=True,
        is_admin=False,
        is_blocked=False,
        countries_regions=['65de565b-4395-4886-8e00-2314307e4e6b'],
        states_regions=['36461459-b184-4316-b274-23316a7800c2'],
        star_transactions=[
            dict(value=8,
                 source_id='3a4b05bc-6fde-4936-bee1-e17162bc1048',
                 operation_type='CREDIT',
                 coin_type='RED_STAR',
                 source='FINANCIAL_TRANSACTION',
                 operation_date='2019-02-03T13:21:45+00:00'),
            dict(value=9,
                 source_id='06f00cb9-304c-458b-9090-924e69eed5f4',
                 operation_type='CREDIT',
                 coin_type='GOLDEN_STAR',
                 source='FINANCIAL_TRANSACTION',
                 operation_date='2019-02-03T13:43:21+00:00')],
        payment_logs=[
            dict(transaction_date='2020-01-01T15:16:17+00:00',
                 payment_gateway='WIRECARD',
                 raw_sent_data=None,
                 raw_received_data="{'status': 'ACTIVE'}"),
            dict(transaction_date='2020-01-01T15:16:17+00:00',
                 payment_gateway='WIRECARD',
                 raw_sent_data=None,
                 raw_received_data="{'status': 'ACTIVE'}")],
        user=dict(
            name='Anselmo Lira',
            email='alira@stormsec.com',
            date_birth='1986-12-16',
            street='Avenida Brasil',
            street_number='500',
            street_complement='apt 607',
            neighborhood='pechinchão',
            city="Rio de Janeiro",
            state="Rio de Janeiro",
            country="Brasil",
            postal_code="25525-001",
            phone_number='(21) 2222-3333',
            cpf='123.456.789-01',
            nickname='lerdinho',
            profile_image=None),
        push_notification_data=None)
    print('player_data.to_json: ' + str(player_data.to_json()))
    print('\n\n\n')
    print('expected_dict: ' + str(expected_dict))
    assert player_data.to_json() == expected_dict


def test_player_to_json_with_elo():
    transaction_1 = StarTransaction(
        value=8,
        source_id='3a4b05bc-6fde-4936-bee1-e17162bc1048',
        operation_type=OperationType.CREDIT,
        coin_type=CoinType.RED_STAR,
        source=SourceOperationType.FINANCIAL_TRANSACTION,
        operation_date=datetime(2019, 2, 3, 13, 21, 45, tzinfo=timezone.utc))
    transaction_2 = StarTransaction(
        value=9,
        source_id='06f00cb9-304c-458b-9090-924e69eed5f4',
        operation_type=OperationType.CREDIT,
        coin_type=CoinType.GOLDEN_STAR,
        source=SourceOperationType.FINANCIAL_TRANSACTION,
        operation_date=datetime(2019, 2, 3, 13, 43, 21, tzinfo=timezone.utc))
    transaction_list = [transaction_1, transaction_2]

    payment_log_1 = PaymentLog(
        transaction_date=aware_utc(datetime(2020, 1, 1, 15, 16, 17)),
        payment_gateway=PaymentGateway.WIRECARD,
        raw_received_data="{'status': 'ACTIVE'}")
    payment_log_2 = PaymentLog(
        transaction_date=aware_utc(datetime(2020, 1, 1, 15, 16, 17)),
        payment_gateway=PaymentGateway.WIRECARD,
        raw_received_data="{'status': 'ACTIVE'}")
    payment_logs = [payment_log_1, payment_log_2]

    _user_data = User(
        name='Anselmo Lira',
        email='alira@stormsec.com',
        date_birth=date(1986, 12, 16),
        street='Avenida Brasil',
        street_number='500',
        street_complement='apt 607',
        neighborhood='pechinchão',
        city='Rio de Janeiro',
        state='Rio de Janeiro',
        country='Brasil',
        postal_code='25525-001',
        phone_number='(21) 2222-3333',
        cpf='123.456.789-01',
        nickname='lerdinho')
    country_region = CountryRegion(
        entity_id='65de565b-4395-4886-8e00-2314307e4e6b',
        name='regiao1',
        minimum_bet=3,
        countries=['Brasil', 'Argentina', 'Paraguai'])
    state_region = StateRegion(
        entity_id='36461459-b184-4316-b274-23316a7800c2',
        name='regiao2',
        minimum_bet=45,
        states=['Rio de Janeiro', 'São Paulo', 'Minas Gerais'])
    subscription = PlayerSubscription(
        expiration_date=aware_utc(datetime(2099, 12, 31, 0, 0, 0)),
        payment_gateway=PaymentGateway.WIRECARD,
        plan_name='red_stars_monthly')
    player_data = Player(
        entity_id='960710e9-eb92-43e4-9548-bf61b10cccf2',
        user=_user_data,
        red_star_balance=0,
        golden_star_balance=0,
        player_status=PlayerStatus.OFFLINE,
        countries_regions=[country_region.entity_id],
        states_regions=[state_region.entity_id],
        star_transactions=transaction_list,
        subscription=subscription,
        payment_logs=payment_logs,
        terms=True,
        star_reservations=[],
        elo_rating=1500.5)
    expected_dict = dict(
        elo_rating=1500.5,
        red_star_balance=0,
        subscription=dict(plan_name='red_stars_monthly',
                          payment_gateway='WIRECARD',
                          expiration_date='2099-12-31T00:00:00+00:00'),
        golden_star_balance=0,
        points=0,
        player_status="OFFLINE",
        entity_id='960710e9-eb92-43e4-9548-bf61b10cccf2',
        consoles=[],
        favorites=[],
        purchases=[],
        star_reservations=[],
        terms=True,
        is_admin=False,
        is_blocked=False,
        countries_regions=['65de565b-4395-4886-8e00-2314307e4e6b'],
        states_regions=['36461459-b184-4316-b274-23316a7800c2'],
        star_transactions=[
            dict(value=8,
                 source_id='3a4b05bc-6fde-4936-bee1-e17162bc1048',
                 operation_type='CREDIT',
                 coin_type='RED_STAR',
                 source='FINANCIAL_TRANSACTION',
                 operation_date='2019-02-03T13:21:45+00:00'),
            dict(value=9,
                 source_id='06f00cb9-304c-458b-9090-924e69eed5f4',
                 operation_type='CREDIT',
                 coin_type='GOLDEN_STAR',
                 source='FINANCIAL_TRANSACTION',
                 operation_date='2019-02-03T13:43:21+00:00')],
        payment_logs=[
            dict(transaction_date='2020-01-01T15:16:17+00:00',
                 payment_gateway='WIRECARD',
                 raw_sent_data=None,
                 raw_received_data="{'status': 'ACTIVE'}"),
            dict(transaction_date='2020-01-01T15:16:17+00:00',
                 payment_gateway='WIRECARD',
                 raw_sent_data=None,
                 raw_received_data="{'status': 'ACTIVE'}")],
        user=dict(
            name='Anselmo Lira',
            email='alira@stormsec.com',
            date_birth='1986-12-16',
            street='Avenida Brasil',
            street_number='500',
            street_complement='apt 607',
            neighborhood='pechinchão',
            city="Rio de Janeiro",
            state="Rio de Janeiro",
            country="Brasil",
            postal_code="25525-001",
            phone_number='(21) 2222-3333',
            cpf='123.456.789-01',
            nickname='lerdinho',
            profile_image=None),
        push_notification_data=None)
    print('player_data.to_json: ' + str(player_data.to_json()))
    print('\n\n\n')
    print('expected_dict: ' + str(expected_dict))
    assert player_data.to_json() == expected_dict


user = User(
    name='Anselmo Lira',
    email='alira@stormsec.com',
    date_birth=date(1986, 12, 16),
    street='Avenida Brasil',
    street_number='500',
    street_complement='apt 607',
    neighborhood='pechinchão',
    city='Rio de Janeiro',
    state='Rio de Janeiro',
    country='Brasil',
    postal_code='25525-001',
    phone_number='(21) 2222-3333',
    cpf='123.456.789-01',
    nickname='lerdinho'
)
player = Player(user=user,
                golden_star_balance=0,
                red_star_balance=0,
                terms=True,
                player_status=PlayerStatus.OFFLINE,
                star_reservations=[])


def test_player_without_balance():
    player_id = player.to_json()['entity_id']
    assert player.red_star_balance == 0
    assert player.to_json() == dict(
        elo_rating=1500,
        red_star_balance=0,
        golden_star_balance=0,
        points=0,
        player_status="OFFLINE",
        entity_id=player_id,
        consoles=[],
        favorites=[],
        countries_regions=[],
        states_regions=[],
        star_transactions=[],
        payment_logs=[],
        purchases=[],
        terms=True,
        is_admin=False,
        is_blocked=False,
        subscription=None,
        star_reservations=[],
        push_notification_data=None,
        user=dict(
            name='Anselmo Lira',
            email='alira@stormsec.com',
            date_birth='1986-12-16',
            street='Avenida Brasil',
            street_number='500',
            street_complement='apt 607',
            neighborhood='pechinchão',
            city="Rio de Janeiro",
            state="Rio de Janeiro",
            country="Brasil",
            postal_code="25525-001",
            phone_number='(21) 2222-3333',
            cpf='123.456.789-01',
            nickname='lerdinho',
            profile_image=None))


def test_add_star_transaction():
    player_data = player_with_star_transactions
    transaction_1 = StarTransaction(
        value=5,
        source_id=str(uuid4()),
        operation_type=OperationType.CREDIT,
        coin_type=CoinType.RED_STAR,
        source=SourceOperationType.DUEL,
        operation_date=datetime(2019, 8, 1, 11, 15, 2, tzinfo=timezone.utc))
    player_data.add_star_transaction(transaction_1)
    assert player_data.red_star_balance == 10
    assert len(player_data.star_transactions) == 7

    transaction_2 = StarTransaction(
        value=3,
        source_id=str(uuid4()),
        operation_type=OperationType.DEBIT,
        coin_type=CoinType.GOLDEN_STAR,
        source=SourceOperationType.DUEL,
        operation_date=datetime(2019, 8, 1, 13, 22, 35, tzinfo=timezone.utc)
    )
    player_data.add_star_transaction(transaction_2)
    assert player_data.golden_star_balance == 4
    assert len(player_data.star_transactions) == 8

    player_data.add_star_transaction(transaction_1)
    assert len(player_data.star_transactions) == 9


def test_add_golden_star_transaction_error():
    player_data = player_with_consoles
    transaction = StarTransaction(
        value=1,
        source_id=str(uuid4()),
        operation_type=OperationType.DEBIT,
        coin_type=CoinType.GOLDEN_STAR,
        source=SourceOperationType.DUEL,
        operation_date=datetime(2019, 2, 4, 19, 2, 35, tzinfo=timezone.utc))

    with pytest.raises(CheckPlayerBalanceException) as exc:
        player_data.add_star_transaction(transaction)
    assert 'Transaction with golden stars not allowed: ' \
           'final negative balance' in str(exc.value)


def test_add_red_star_transaction_error():
    player_data = player_with_consoles
    transaction = StarTransaction(
        value=5,
        source_id=str(uuid4()),
        operation_type=OperationType.DEBIT,
        coin_type=CoinType.RED_STAR,
        source=SourceOperationType.DUEL,
        operation_date=datetime(2019, 2, 7, 7, 15, 2, tzinfo=timezone.utc))

    with pytest.raises(CheckPlayerBalanceException) as exc:
        player_data.add_star_transaction(transaction)
    assert 'Transaction with red stars not allowed: ' \
           'final negative balance' in str(exc.value)


def test_find_star_transaction_by_source():
    player_data = player_with_star_transactions

    found_transactions_1 = player_data.find_star_transactions_by_source(
        SourceOperationType.TEAM_DUEL)
    assert found_transactions_1 is not None
    assert len(found_transactions_1) == 1

    found_transactions_2 = player_data.find_star_transactions_by_source(
        SourceOperationType.FINANCIAL_TRANSACTION)
    assert found_transactions_2 is not None
    assert len(found_transactions_2) == 3

    found_transactions_3 = player_data.find_star_transactions_by_source(
        SourceOperationType.CHAMPIONSHIP)
    assert found_transactions_3 == []

    found_transactions_4 = player_data.find_star_transactions_by_source(
        SourceOperationType.FINANCIAL_TRANSACTION,
        '53a36c3d-091b-4855-8fa1-1c13ada7941b')
    assert found_transactions_4 is not None
    assert len(found_transactions_4) == 1

    found_transactions_5 = player_data.find_star_transactions_by_source(
        SourceOperationType.DUEL,
        str(uuid4()))
    assert found_transactions_5 == []


def test_remove_star_transaction():
    player_data = player_with_star_transactions
    delete_result_1 = player_data.remove_star_transaction(
        star_transaction_list[4].entity_id)

    assert delete_result_1
    assert len(player_data.star_transactions) == 8
    assert player_data.red_star_balance == 10

    delete_result_2 = player_data.remove_star_transaction(str(uuid4()))
    assert not delete_result_2


def test_list_last_2_transactions():
    player_data = player_with_star_transactions
    last_2_transactions = player_data.list_star_transactions(2)
    assert len(last_2_transactions) == 2


def test_recalculate_balance():
    player_data = player_with_star_transactions
    assert player_data.recalcule_star_balance(CoinType.GOLDEN_STAR) == 4
    assert player_data.recalcule_star_balance(CoinType.RED_STAR) == 20


def test_user_roundtrip():
    generic_serialize_roundtrip_test(Player, player_with_star_transactions)


def test_push_notification_data_roundtrip():
    push_data = PushNotificationData('arn', 'd_t')
    generic_serialize_roundtrip_test(PushNotificationData, push_data)


payment = PagSeguroPayment(code='HAIAU281481HASDJ112')
product = ProductPurchased(
    price=1234,
    star_value=12,
    description='teste',
    star_type='gold',
    duration=0
)
purchase = Purchase(product=product, payment=payment)


def test_add_purchase():

    player_with_star_transactions.add_purchase(purchase)
    assert len(player_with_star_transactions.purchases) == 1
    player_with_star_transactions.add_purchase(purchase)
    assert len(player_with_star_transactions.purchases) == 2


def test_get_purchase_by_code():
    player_with_star_transactions.add_purchase(purchase)
    assert len(player_with_star_transactions.purchases) == 3
    found_purchase = \
        player_with_star_transactions.\
        find_purchase_by_payment_code('HAIAU281481HASDJ112')
    assert found_purchase
    found_purchase2 = \
        player_with_star_transactions.\
        find_purchase_by_payment_code('HAIAU2814811111HASDJ112')
    assert not found_purchase2


def test_purchase_add_purchase_status():
    player_with_star_transactions.add_purchase(purchase)
    assert len(player_with_star_transactions.purchases) == 4
    player_with_star_transactions.add_purchase_status(
        'HAIAU281481HASDJ112',
        'PAYED',
        None,
        'YRQU124ASA2325'
    )
    found_purchase = \
        player_with_star_transactions. \
        find_purchase_by_payment_code('HAIAU281481HASDJ112')
    assert found_purchase
    assert len(found_purchase.payment.transactions) == 1
    player_with_star_transactions.add_purchase_status(
        'HAIAU281481HASDJ112',
        'SCHRUBLES',
        None,
        'YRQU124121212ASA2325'
    )
    found_purchase = \
        player_with_star_transactions. \
        find_purchase_by_payment_code('HAIAU281481HASDJ112')
    assert found_purchase
    assert len(found_purchase.payment.transactions) == 2
    with pytest.raises(Exception) as excinfo:
        player_with_star_transactions.add_purchase_status(
            'HAIAU281481HAS1111DJ112',
            'SCHRUBLES',
            None,
            'YRQU124121212ASA2325'
        )
    assert 'Purchase HAIAU281481HAS1111DJ112 not found' in str(excinfo.value)


def test_purchase_list():
    player_with_star_transactions.add_purchase(purchase)
    assert len(player_with_star_transactions.purchases) == 5
    player_with_star_transactions.add_purchase(purchase)
    assert len(player_with_star_transactions.purchases) == 6
    purchases = player_with_star_transactions.list_purchases()
    assert len(purchases) == 6


def test_list_last_2_purchases():
    last_2_transactions = player_with_star_transactions.list_star_transactions(2)
    assert len(last_2_transactions) == 2


def test_list_last_purchases():
    last_2_transactions = player_with_star_transactions.list_star_transactions()
    assert len(last_2_transactions) == 8


def test_purchase_from_json():
    player_json = {
        "entity_id": '',
        "red_star_balance": 15,
        "consoles": [{
            "console_id": "123",
            "game_points": [{
                "game_id": "1",
                "victories": 20}]}],
        "countries_regions": ["id123"],
        "states_regions": ["id123"],
        "favorites": ["ght232141-3a12-5t67-19ehdufasuu"],
        "golden_star_balance": 0,
        "star_transactions": [{
            "value": 2,
            "operation_date": "2019-08-21T13:11:07+00:00",
            "coin_type": "GOLDEN_STAR",
            "operation_type": "DEBIT",
            "source": "DUEL",
            "source_id": "68dc45c5-43eb-4351-bead-4319aba7af85"
        }],
        "purchases": [{
            "product": {
                "price": 1050,
                "star_value": "3",
                "description": "teste teste teste",
                "star_type": "red",
                "duration": 3
            },
            "purchase_type": "GOLDEN_STAR_PURCHASE",
            "purchase_datetime": "2017-11-21T09:58:00+00:00",
            "payment": {
                "code": "schrubles1241",
                "payment_datetime": "2017-11-22T09:58:00+00:00",
                "payment_type": "PAGSEGURO",
                "transactions": []
            }
        }],
        "user": {
            "name": "Anselmo Lira",
            "email": "playerstars@playerstars.com.br",
            "date_birth": "2018-11-11",
            "street": 'Avenida Brasil',
            "street_number": '500',
            "street_complement": 'apt 607',
            "neighborhood": 'pechinchão',
            "city": "Rio de Janeiro",
            "state": "Rio de Janeiro",
            "country": "Brasil",
            "postal_code": "22333-000",
            "phone_number": "(21) 99663-6963",
            "cpf": "123.456.789-00",
            "nickname": "anselmo.lira",
            "profile_image": "iVBORw0KGgoAAAANSUhEUgAA"
        },
        "points": 300,
        "terms": True,
        "player_status": "OFFLINE",
        "star_reservations": []
    }
    player_from_json = Player.from_json(player_json)
    assert player_from_json.purchases[0].product.duration == 3


red_star_reserve = StarReserve(
    event_id='123',
    star_type=CoinType.RED_STAR,
    star_value=2)


golden_star_reserve = StarReserve(
    event_id='a1b2c3',
    star_type=CoinType.GOLDEN_STAR,
    star_value=1)


def test_star_reserve_repr():
    assert golden_star_reserve.__repr__() == 'GOLDEN_STAR - 1'


def test_star_reserve_call():
    assert red_star_reserve() == red_star_reserve.to_json()


def test_add_red_star_reserve():
    player_data: Player = player_with_star_transactions
    player_data.red_star_balance = 5
    player_data.star_reservations = []
    assert player_data.red_star_balance == 5

    player_data.reserve_star(CoinType.RED_STAR, 2, 'q1w2e3')
    assert player_data.red_star_balance == 3
    assert player_data.star_reservations
    assert len(player_data.star_reservations) == 1


def test_add_red_star_reserve_without_enought_balance():
    player_data: Player = player_with_consoles
    assert player_data.red_star_balance == 0

    with pytest.raises(InsufficientRedStarsBalanceException) as exc:
        player_data.reserve_star(CoinType.RED_STAR, 3, 'q1w2e3')
    assert "You haven't enough red star to reserve. " \
           "Event requires 3 star(s) but you have 0 star(s)" in str(exc.value)


def test_add_golden_star_reserve():
    player_data: Player = player_with_star_transactions
    player_data.golden_star_balance = 4
    player_data.star_reservations = []
    assert player_data.golden_star_balance == 4

    player_data.reserve_star(CoinType.GOLDEN_STAR, 4, '1a2b3c')
    assert player_data.golden_star_balance == 0
    assert player_data.star_reservations
    assert len(player_data.star_reservations) == 1


def test_add_golden_star_reserve_without_enougth_balance():
    player_data: Player = player_with_consoles
    assert player_data.golden_star_balance == 0

    with pytest.raises(InsufficientGoldenStarsBalanceException) as exc:
        player_data.reserve_star(CoinType.GOLDEN_STAR, 2, 'abc')
    assert "You haven't enough golden star to reserve. " \
           "Event requires 2 star(s) but you have 0 star(s)" in str(exc.value)


def test_get_total_red_star_in_reserve():
    player_data: Player = player_with_star_transactions
    player_data.red_star_balance = 15
    player_data.golden_star_balance = 21
    player_data.star_reservations = []
    assert player_data.get_total_star_in_reserve(CoinType.GOLDEN_STAR) == 0
    assert player_data.get_total_star_in_reserve(CoinType.RED_STAR) == 0

    player_data.reserve_star(CoinType.GOLDEN_STAR, 2, '123')
    player_data.reserve_star(CoinType.GOLDEN_STAR, 4, 'abc')
    player_data.reserve_star(CoinType.RED_STAR, 7, '2w3')
    player_data.reserve_star(CoinType.RED_STAR, 3, 'a2kk')

    assert player_data.get_total_star_in_reserve(CoinType.RED_STAR) == 10
    assert player_data.get_total_star_in_reserve(CoinType.GOLDEN_STAR) == 6


def test_find_star_reserve():
    player_data: Player = player_with_star_transactions
    player_data.star_reservations = []
    player_data.star_reservations.append(red_star_reserve)
    found_reserve = player_data.find_reserve('123')

    star_reserve_to_compare = StarReserve(
        event_id='123',
        star_value=2,
        star_type=CoinType.RED_STAR)
    assert found_reserve
    assert found_reserve == star_reserve_to_compare


def test_find_star_reserve_not_found():
    player_data: Player = player_with_star_transactions
    player_data.star_reservations.append(red_star_reserve)
    found_reserve = player_data.find_reserve('a12ff')
    assert not found_reserve


def test_cancel_golden_star_reserve():
    player_data: Player = player_with_star_transactions
    player_data.star_reservations = []
    player_data.golden_star_balance = 7
    player_data.star_reservations.append(golden_star_reserve)
    assert player_data.star_reservations
    assert len(player_data.star_reservations) == 1
    assert player_data.golden_star_balance == 7

    player_data.cancel_reserve('a1b2c3')
    assert len(player_data.star_reservations) == 0
    assert player_data.get_total_star_in_reserve(CoinType.GOLDEN_STAR) == 0
    assert player_data.golden_star_balance == 8


def test_cancel_red_star_reserve():
    player_data: Player = player_with_star_transactions
    player_data.star_reservations = []
    player_data.red_star_balance = 5
    player_data.star_reservations.append(red_star_reserve)
    assert player_data.star_reservations
    assert len(player_data.star_reservations) == 1
    assert player_data.red_star_balance == 5

    player_data.cancel_reserve('123')
    assert len(player_data.star_reservations) == 0
    assert player_data.get_total_star_in_reserve(CoinType.RED_STAR) == 0
    assert player_data.red_star_balance == 7


def test_cancel_unknow_star_reserve():
    player_data = player_with_star_transactions
    player_data.star_reservations = []
    assert len(player_data.star_reservations) == 0

    with pytest.raises(StarReserveNotFoundException) as exc:
        player_data.cancel_reserve('wqc')
    assert "Reserve for event wqc doesn't exist" in str(exc.value)


def test_star_reserve_roundtrip():
    generic_serialize_roundtrip_test(StarReserve, red_star_reserve)


def test_get_game_victories_by_id():
    player_data = player_with_consoles
    assert player_data.get_game_victories_by_id('3c8fffe3-b137-4a16-bdea-4d942d08d979') == 0

    assert not player_data.get_game_victories_by_id('3c8fffe3-b137-4a16-bdea-4d942d08d989')


def test_get_game_elo_rating_by_id():
    player_data = player_with_consoles
    assert player_data.get_game_elo_rating_by_id(
        '3c8fffe3-b137-4a16-bdea-4d942d08d979') == 1500


def make_game_points_data():
    return GamePoints(game_id='1234', victories=0)


def test_game_points():
    assert make_game_points_data()


player_consoles = PlayerConsoles(
    console_id='abcd',
    game_points=[make_game_points_data()],
    tag_name='oieoieoie')


def test_player_consoles():
    assert player_consoles


def test_get_tag_name():
    assert player_with_consoles.get_tag_name('308995bd-6c03-4a60-be06-c599df86a384') == 'oie'
    assert player_with_consoles.get_tag_name('oie') is None


def test_game_exists():
    assert not player_with_consoles.game_exists('schrubles')
    assert player_with_consoles.game_exists(
        'bdbc658d-8850-41e5-9df8-e6e461f6eba6')


def test_subscription_detail_from_json():
    assert PaymentLog.from_json({
        'transaction_date': '2020-08-10T09:10:15+00:00',
        'payment_gateway': 'GOOGLE',
        'raw_received_data': "{'status': 'ACTIVATED'}"})


def test_cancel_subscription():
    subscription = PlayerSubscription(
        expiration_date=aware_utc(datetime(2099, 12, 31, 23, 59, 59)),
        plan_name='red_star_century',
        payment_gateway=PaymentGateway.GOOGLE)
    player = Player(user=user_data(), subscription=subscription)
    assert player.is_premium

    player.cancel_subscription()
    assert not player.is_premium
    assert player.subscription.expiration_date == \
        aware_utc(datetime(2012, 12, 31, 23, 59, 59))


def test_add_payment_log():
    payment_log = PaymentLog(
        transaction_date=aware_utc(datetime(2020, 8, 20, 13, 14, 15)),
        payment_gateway=PaymentGateway.GOOGLE)
    player = Player(user=user_data())
    assert len(player.payment_logs) == 0

    player.add_payment_log(payment_log)
    assert len(player.payment_logs) == 1
    assert player.payment_logs[0].payment_gateway == PaymentGateway.GOOGLE


def test_payment_log_from_json():
    payment_log_json = {
        'transaction_date': '2020-08-20T13:14:15+00:00',
        'payment_gateway': 'GOOGLE'}
    payment_log: PaymentLog = PaymentLog.from_json(payment_log_json)
    assert payment_log
    assert payment_log.payment_gateway == PaymentGateway.GOOGLE


def test_player_from_json_no_elo():
    user = User(name='name',
                email='email@dom.com',
                date_birth=datetime(1971, 7, 19),
                street='street',
                street_number='number',
                street_complement='sc',
                neighborhood='neig',
                city='city',
                state='state',
                country='country',
                postal_code='postal',
                phone_number='555-5555',
                cpf='12345678909',
                nickname='sky')
    player = Player(user=user)
    json_data = player.to_json()
    assert json_data['elo_rating'] == 1500
    del json_data['elo_rating']
    loaded = Player.from_json(json_data)

    assert loaded.elo_rating == 1500


def test_update_elo_rating(player):
    player1: Player = deepcopy(player)
    player2: Player = deepcopy(player)

    player2.elo_rating = 1510.0

    mock_adapter1 = MagicMock()
    mock_adapter2 = MagicMock()
    mock_json1 = MagicMock()
    mock_json2 = MagicMock()

    player1.set_adapter(mock_adapter1)
    player1.to_json = MagicMock(return_value=mock_json1)
    player2.set_adapter(mock_adapter2)
    player2.to_json = MagicMock(return_value=mock_json2)

    elo = Elo()

    player1.update_elo_ratings(player2, elo)

    TestCase().assertAlmostEqual(player1.elo_rating, 1508.2301, 3)
    TestCase().assertAlmostEqual(player2.elo_rating, 1501.7698, 3)

    mock_adapter1.save.assert_called_with(mock_json1)
    mock_adapter2.save.assert_called_with(mock_json2)
