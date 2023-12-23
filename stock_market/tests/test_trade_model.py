from brokers.factories import TradeFactory
from brokers.models import Trade
from django.db import IntegrityError
from django.db.models import QuerySet
from django.test import TestCase
from faker import Faker


class TradeModelTest(TestCase):
    def setUp(self) -> None:
        self.fake = Faker()
        self.new_trade = TradeFactory
        self.trade_count = lambda: Trade.objects.count()

    def test_create_trade_ok(self):
        trade_count = self.trade_count()

        trade = self.new_trade()

        self.assertEqual(trade_count + 1, self.trade_count())
        self.assertIsInstance(trade, Trade)

    def test_update_trade_with_negative_price(self):
        trade_count = self.trade_count()

        trade = self.new_trade()

        trade.price = -self.fake.pyint()

        self.assertEqual(trade_count + 1, self.trade_count())
        self.assertRaises(IntegrityError, trade.save)

    def test_update_trade_with_negative_quantity(self):
        trade_count = self.trade_count()

        trade = self.new_trade()

        trade.quantity = -self.fake.pyint()

        self.assertEqual(trade_count + 1, self.trade_count())
        self.assertRaises(IntegrityError, trade.save)

    def test_order_created_at_desc_ordering(self):
        trade_count = self.trade_count()

        trade_1 = self.new_trade()
        trade_2 = self.new_trade()

        order_list = [trade_1, trade_2]

        max_item = max(order_list, key=lambda x: x.created_at)
        min_item = min(order_list, key=lambda x: x.created_at)

        result = Trade.objects.all()

        self.assertEqual(trade_count + 2, self.trade_count())
        self.assertIsInstance(result, QuerySet)
        self.assertEqual(result[0], max_item)
        self.assertEqual(result[1], min_item)
