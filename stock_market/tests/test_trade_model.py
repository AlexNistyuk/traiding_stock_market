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

    def test_create_trade_ok(self):
        trade = self.new_trade()

        self.assertIsInstance(trade, Trade)

    def test_update_trade_with_negative_price(self):
        trade = self.new_trade()

        trade.price = -self.fake.pyint()

        self.assertRaises(IntegrityError, trade.save)

    def test_update_trade_with_negative_count(self):
        trade = self.new_trade()

        trade.count = -self.fake.pyint()

        self.assertRaises(IntegrityError, trade.save)

    def test_order_created_at_desc_ordering(self):
        trade_1 = self.new_trade()
        trade_2 = self.new_trade()

        order_list = [trade_1, trade_2]

        max_item = max(order_list, key=lambda x: x.created_at)
        min_item = min(order_list, key=lambda x: x.created_at)

        result = Trade.objects.all()

        self.assertIsInstance(result, QuerySet)
        self.assertEqual(result[0], max_item)
        self.assertEqual(result[1], min_item)
