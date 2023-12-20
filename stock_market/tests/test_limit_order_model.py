from brokers.factories import LimitOrderFactory
from brokers.models import LimitOrder
from django.db import IntegrityError
from django.db.models import QuerySet
from django.test import TestCase
from faker import Faker


class LimitOrderModelTest(TestCase):
    def setUp(self) -> None:
        self.fake = Faker()
        self.new_order = LimitOrderFactory
        self.order_count = lambda: LimitOrder.objects.count()

    def test_create_order_ok(self):
        order_count = self.order_count()

        order = self.new_order()

        self.assertEqual(order_count + 1, self.order_count())
        self.assertIsInstance(order, LimitOrder)

    def test_update_order_with_negative_price(self):
        order_count = self.order_count()

        order = self.new_order()

        order.price = -self.fake.pyint()

        self.assertEqual(order_count + 1, self.order_count())
        self.assertRaises(IntegrityError, order.save)

    def test_update_order_with_negative_count(self):
        order_count = self.order_count()

        order = self.new_order()

        order.count = -self.fake.pyint()

        self.assertEqual(order_count + 1, self.order_count())
        self.assertRaises(IntegrityError, order.save)

    def test_order_created_at_asc_ordering(self):
        order_count = self.order_count()

        order_1 = self.new_order()
        order_2 = self.new_order()

        order_list = [order_1, order_2]

        max_item = max(order_list, key=lambda x: x.created_at)
        min_item = min(order_list, key=lambda x: x.created_at)

        result = LimitOrder.objects.all()

        self.assertEqual(order_count + 2, self.order_count())
        self.assertIsInstance(result, QuerySet)
        self.assertEqual(result[0], min_item)
        self.assertEqual(result[1], max_item)
