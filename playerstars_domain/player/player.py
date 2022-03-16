from datetime import datetime
from enum import Enum
from typing import List

from clapy_basic_classes import BasicEntity, BasicValue
from marshmallow import fields, post_load
from marshmallow_enum import EnumField

from playerstars_domain.console import Console
from playerstars_domain.player.game_points import GamePoints
from playerstars_domain.player.payment_log import PaymentLog
from playerstars_domain.player.player_subscription import PlayerSubscription
from playerstars_domain.player.purchase import Purchase
from playerstars_domain.player.star_reserve import StarReserve
from playerstars_domain.player.star_transaction import (
    CoinType, OperationType, StarTransaction)
from playerstars_domain.user import User
from playerstars_domain.utils.datetime_helper import aware_utc


class PlayerStatus(Enum):
    OFFLINE = 'OFFLINE'
    BUSY = 'BUSY'
    AVAILABLE = 'AVAILABLE'


class CheckPlayerBalanceException(BaseException):
    pass


class InsufficientGoldenStarsBalanceException(BaseException):
    pass


class InsufficientRedStarsBalanceException(BaseException):
    pass


class NegativeRedStarBalanceException(BaseException):
    pass


class NegativeGoldenStarBalanceException(BaseException):
    pass


class StarReserveNotFoundException(BaseException):
    pass


class PlayerConsoles(BasicValue):
    def __init__(self, console_id, tag_name, game_points):
        super(PlayerConsoles, self).__init__()
        self.console_id = console_id
        self.tag_name = tag_name
        self.game_points = game_points

    class Schema(BasicValue.Schema):
        console_id = fields.String(required=True, allow_none=False)
        game_points = fields.Nested(
            GamePoints.Schema, many=True, default=[], missing=[])
        tag_name = fields.String(default=None, missing=None)

        @post_load
        def post_load(self, data, many, partial):
            return PlayerConsoles(**data)


class PushNotificationData(BasicValue):
    def __init__(self, endpoint_arn: str,
                 device_token: str):
        self.endpoint_arn = endpoint_arn
        self.device_token = device_token

    class Schema(BasicValue.Schema):
        endpoint_arn = fields.String(required=True, allow_none=False)
        device_token = fields.String(required=True, allow_none=False)

        @post_load
        def post_load(self, data, many, partial):
            return PushNotificationData(**data)


class Player(BasicEntity):
    def __init__(self,
                 user: User,
                 consoles: List[PlayerConsoles] = None,
                 favorites: List[str] = None,
                 points: int = 0,
                 red_star_balance: int = 0,
                 golden_star_balance: int = 0,
                 player_status: PlayerStatus = PlayerStatus.OFFLINE,
                 entity_id: str = None,
                 states_regions: List[str] = None,
                 countries_regions: List[str] = None,
                 star_transactions: List[StarTransaction] = None,
                 purchases: List[Purchase] = None,
                 star_reservations: List[StarReserve] = None,
                 terms: bool = False,
                 is_blocked: bool = False,
                 is_admin: bool = False,
                 subscription: PlayerSubscription = None,
                 payment_logs: List[PaymentLog] = None,
                 push_notification_data: PushNotificationData = None,
                 elo_rating: float = 1500):
        super(Player, self).__init__(entity_id=entity_id)
        self.user = user
        self.consoles = consoles or []
        self.favorites: List[str] = favorites or []
        self.red_star_balance = red_star_balance
        self.golden_star_balance = golden_star_balance
        self.points = points
        self.player_status = player_status
        self.states_regions = states_regions or []
        self.countries_regions = countries_regions or []
        self.star_transactions = star_transactions or []
        self.star_reservations = star_reservations or []
        self.subscription = subscription
        self.payment_logs = payment_logs or []
        self.purchases = purchases or []
        self.terms = terms
        self.is_blocked = is_blocked
        self.is_admin = is_admin
        self.elo_rating = elo_rating
        self.push_notification_data = push_notification_data

    def __repr__(self):
        return self.user.name

    @property
    def is_premium(self):
        return self.subscription is not None and \
               self.subscription.is_active()

    def update_elo_ratings(self, loser, elo):
        elo.set_ratings(self.elo_rating, loser.elo_rating)
        elo.update_ratings()
        self.elo_rating = elo.wr
        loser.elo_rating = elo.lr
        self.save()
        loser.save()

    def update_red_star_balance(self, new_balance):
        if new_balance < 0:
            raise NegativeRedStarBalanceException(
                "Red star balance can't be negative")
        self.red_star_balance = new_balance

    def update_golden_star_balance(self, new_balance):
        if new_balance < 0:
            raise NegativeGoldenStarBalanceException(
                "Golden star balance can't be negative")
        self.golden_star_balance = new_balance

    def get_total_star_in_reserve(self, coin_type: CoinType):
        return sum(r.star_value for r in self.star_reservations
                   if r.star_type == coin_type)

    def get_game_victories_by_id(self, game_id):
        for console in self.consoles:
            for game in console.game_points:
                if game.game_id == game_id:
                    return game.victories

    def get_game_elo_rating_by_id(self, game_id):
        for console in self.consoles:
            for game in console.game_points:
                if game.game_id == game_id:
                    return game.elo_rating

    def console_list(self):
        return [x.console_id for x in self.consoles]

    def add_console(self, console: Console, tag_name):
        if self.console_exists(console.entity_id):
            return False
        gamelist = [x.entity_id for x in console.games]
        _game_points = []
        for game in gamelist:
            _game_points.append(GamePoints(game, 0))
        self.consoles.append(PlayerConsoles(
            console_id=console.entity_id, game_points=_game_points,
            tag_name=tag_name))
        return True

    def console_exists(self, console_id: str):
        return True if console_id in self.console_list() else False

    def game_exists(self, game_id: str):
        for console in self.consoles:
            if game_id in [x.game_id for x in console.game_points]:
                return True
        return False

    def list_consoles(self):
        return self.consoles

    def remove_console(self, console_id: str):
        if console_id in self.console_list():
            new_console_list = [x for x in self.consoles
                                if x.console_id != console_id]
            self.consoles = new_console_list
            return True
        return False

    def check_balance_before_add_debit_transaction(self, coin_type, value):
        if coin_type == CoinType.RED_STAR:
            future_balance = self.red_star_balance - value
            if future_balance < 0:
                raise CheckPlayerBalanceException(
                    'Transaction with red stars not allowed: '
                    'final negative balance')

        if coin_type == CoinType.GOLDEN_STAR:
            future_balance = self.golden_star_balance - value
            if future_balance < 0:
                raise CheckPlayerBalanceException(
                    'Transaction with golden stars not allowed: '
                    'final negative balance')

    def update_star_transaction_balance(self,
                                        operation_type: OperationType,
                                        coin_type: CoinType,
                                        value):
        if coin_type == CoinType.RED_STAR:
            self.red_star_balance = self.red_star_balance + value \
                if operation_type == OperationType.CREDIT \
                else self.red_star_balance - value

        if coin_type == CoinType.GOLDEN_STAR:
            self.golden_star_balance = self.golden_star_balance + value \
                if operation_type == OperationType.CREDIT \
                else self.golden_star_balance - value

    def add_star_transaction(self, transaction: StarTransaction):
        if transaction.operation_type == OperationType.DEBIT:
            self.check_balance_before_add_debit_transaction(
                transaction.coin_type,
                transaction.value)
        self.star_transactions.append(transaction)
        self.update_star_transaction_balance(transaction.operation_type,
                                             transaction.coin_type,
                                             transaction.value)

    def find_star_transaction_by_id(self, transaction_id):
        for transaction in self.star_transactions:
            if transaction.entity_id == transaction_id:
                return transaction
        return None

    @staticmethod
    def _is_source(transaction, source, source_id):
        if not source_id:
            return transaction.source == source
        return (transaction.source == source and
                transaction.source_id == source_id)

    def find_star_transactions_by_source(self, source, source_id=None):
        return [x for x in self.star_transactions
                if self._is_source(x, source, source_id)]

    def sorted_star_transation(self):
        return sorted(
            self.star_transactions,
            key=lambda x: x.operation_date,
            reverse=True)

    def list_star_transactions(self, last_item=None):
        if not last_item:
            last_item = len(self.star_transactions)
        return self.sorted_star_transation()[0:last_item]

    def recalcule_star_balance(self, coin_type):
        star_transactions = [x for x in self.star_transactions
                             if x.coin_type == coin_type]
        sorted_transactions = sorted(star_transactions,
                                     key=lambda x: x.operation_date)

        balance = 0
        for transaction in sorted_transactions:
            if transaction.operation_type == OperationType.CREDIT:
                balance = balance + transaction.value
            elif transaction.operation_type == OperationType.DEBIT:
                balance = balance - transaction.value

        return balance

    def remove_star_transaction(self, transaction_id: str):
        found_item = self.find_star_transaction_by_id(transaction_id)
        if found_item:
            new_transaction_list = [x for x in self.star_transactions
                                    if x.entity_id != transaction_id]
            self.star_transactions = new_transaction_list

            operation_to_execute = found_item.operation_type
            self.update_star_transaction_balance(
                operation_to_execute, found_item.coin_type, found_item.value)
            return True
        return False

    def find_reserve(self, event_id):
        return next((x for x in self.star_reservations
                     if x.event_id == event_id),
                    None)

    def reserve_star(self,
                     star_type: CoinType,
                     star_value: int,
                     event_id: str):
        if star_type == CoinType.GOLDEN_STAR:
            self.reserve_star_golden(star_value, event_id)
        else:
            self.reserve_star_red(star_value, event_id)

    def reserve_star_red(self, star_value, event_id):
        if self.red_star_balance < star_value:
            raise InsufficientRedStarsBalanceException(
                f"You haven't enough red star to reserve. "
                f"Event requires {star_value} star(s) but you have "
                f"{self.red_star_balance} star(s)")
        reserve = StarReserve(
            event_id=event_id, star_type=CoinType.RED_STAR,
            star_value=star_value)
        self.star_reservations.append(reserve)
        self.red_star_balance = self.red_star_balance - star_value

    def reserve_star_golden(self, star_value, event_id):
        if self.golden_star_balance < star_value:
            raise InsufficientGoldenStarsBalanceException(
                f"You haven't enough golden star to reserve. "
                f"Event requires {star_value} star(s) but you have "
                f"{self.golden_star_balance} star(s)")
        reserve = StarReserve(
            event_id=event_id, star_type=CoinType.GOLDEN_STAR,
            star_value=star_value)
        self.star_reservations.append(reserve)
        self.golden_star_balance = self.golden_star_balance - star_value

    def cancel_reserve(self, event_id):
        reserve: StarReserve = self.find_reserve(event_id)
        if not reserve:
            raise StarReserveNotFoundException(
                f"Reserve for event {event_id} doesn't exist")

        if reserve.star_type == CoinType.GOLDEN_STAR:
            self.golden_star_balance += reserve.star_value
        else:
            self.red_star_balance += reserve.star_value

        new_star_reservations = [x for x in self.star_reservations
                                 if x.event_id != event_id]
        self.star_reservations = new_star_reservations

    def add_purchase(self, purchase: Purchase):
        self.purchases.append(purchase)

    def find_purchase_by_payment_code(self, code):
        for purchase in self.purchases:
            if purchase.payment.code == code:
                return purchase
        return None

    def list_purchases(self, last_item=None):
        if not last_item:
            last_item = len(self.purchases)
        list_to_return = sorted(self.purchases,
                                key=lambda x: x.payment.payment_datetime,
                                reverse=True)
        return list_to_return[0:last_item]

    def add_purchase_status(self,
                            purchase_code,
                            purchase_status,
                            transaction_datetime,
                            code):
        purchase_found = self.find_purchase_by_payment_code(purchase_code)
        if not purchase_found:
            raise Exception('Purchase {0} not found'.format(purchase_code))

        purchase_found.payment.add_transaction(purchase_status,
                                               transaction_datetime,
                                               code)

    def add_favorite(self, favorite):
        self.favorites.append(favorite)
        self.favorites = list(set(self.favorites))

    def find_favorite(self, favorite_id):
        for favorite in self.favorites:
            if favorite == favorite_id:
                return favorite
        return None

    def list_favorites(self):
        return self.favorites

    def remove_favorite(self, favorite_id):
        new_favorite_list = [x for x in self.favorites
                             if x != favorite_id]
        self.favorites = new_favorite_list

    def get_status(self):
        return PlayerStatus(self.player_status)

    def change_status(self, new_status):
        self.player_status = new_status

    def get_tag_name(self, console_id):
        for item in self.consoles:
            if item.console_id == console_id:
                return item.tag_name
        return None

    def add_payment_log(self, log_item: PaymentLog):
        self.payment_logs.append(log_item)

    def cancel_subscription(self):
        cancel_datetime = datetime(2012, 12, 31, 23, 59, 59)
        self.subscription.expiration_date = aware_utc(cancel_datetime)

    class Schema(BasicEntity.Schema):
        user = fields.Nested(User.Schema, required=True)
        consoles = fields.Nested(
            PlayerConsoles.Schema, many=True, default=[], missing=[])
        states_regions = fields.List(
            fields.String, many=True, allow_none=True, default=[], missing=[])
        countries_regions = fields.List(
            fields.String, many=True, allow_none=True, default=[], missing=[])
        favorites = fields.List(
            fields.String, many=True, allow_none=True, default=[], missing=[])
        star_transactions = fields.Nested(
            StarTransaction.Schema, many=True, allow_none=True,
            default=[], missing=[])
        payment_logs = fields.Nested(
            PaymentLog.Schema,
            many=True,
            allow_none=True,
            default=[],
            missing=[])
        red_star_balance = fields.Integer(
            required=True, allow_none=False, default=0)
        points = fields.Integer(required=True, allow_none=False, default=0)
        golden_star_balance = fields.Integer(
            required=True, allow_none=False, default=0)
        player_status = EnumField(
            PlayerStatus, required=True, allow_none=False,
            default=PlayerStatus.OFFLINE)
        purchases = fields.Nested(
            Purchase.Schema, required=False, many=True, default=[])
        star_reservations = fields.Nested(
            StarReserve.Schema, required=False, many=True, default=[])
        terms = fields.Boolean(
            required=True, default=False)
        is_admin = fields.Boolean(
            required=False, default=False, missing=False)
        is_blocked = fields.Boolean(
            required=False, default=False, missing=False)
        subscription = fields.Nested(
            PlayerSubscription.Schema,
            required=False,
            allow_none=True)
        elo_rating = fields.Float(required=False,
                                  allow_none=False,
                                  default=1500,
                                  missing=1500)
        push_notification_data = fields.Nested(
            PushNotificationData.Schema,
            required=False,
            allow_none=True)

        @post_load
        def post_load(self, data, many, partial):
            return Player(**data)
