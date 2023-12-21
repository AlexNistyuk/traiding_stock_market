from brokers.factories import LimitOrderFactory
from brokers.models import OrderActivatedStatuses, OrderStatuses
from django.test import TestCase
from faker import Faker


class LimitOrderViewSetTest(TestCase):
    def setUp(self) -> None:
        self.path = "/v1/orders/limit/"
        self.fake = Faker()
        self.new_order = LimitOrderFactory

    # TODO: create list order negative using permissions
    def test_list_order_ok(self):
        _ = self.new_order()

        response = self.client.get(self.path)

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, list)
        self.assertIsInstance(response.data[0], dict)

    # TODO: create create order when creating logic will be written
    # TODO: create create order negative when creating logic will be written
    # TODO: create retrieve order negative using permissions

    def test_retrieve_order_ok(self):
        order = self.new_order()
        path = f"{self.path}{order.id}/"

        response = self.client.get(path)

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, dict)
        self.assertEqual(response.data["id"], order.id)

    def test_update_order_ok(self):
        order = self.new_order()
        path = f"{self.path}{order.id}/"

        response = self.client.put(
            path=path,
            data={
                "price": self.fake.pyint(),
                "activated_status": self.fake.random_choices(
                    elements=OrderActivatedStatuses.choices
                )[0][0],
                "count": self.fake.pyint(),
                "status": self.fake.random_choices(elements=OrderStatuses.choices)[0][
                    0
                ],
                "is_sell": False,
                "portfolio": order.portfolio.id,
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, dict)
        self.assertEqual(response.data["id"], order.id)

    def test_update_order_with_negative_count(self):
        order = self.new_order()
        path = f"{self.path}{order.id}/"

        response = self.client.put(
            path=path,
            data={
                "price": self.fake.pyint(),
                "activated_status": self.fake.random_choices(
                    elements=OrderActivatedStatuses.choices
                )[0][0],
                "count": -self.fake.pyint(),
                "status": self.fake.random_choices(elements=OrderStatuses.choices)[0][
                    0
                ],
                "is_sell": False,
                "portfolio": order.portfolio.id,
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)

    def test_update_order_with_negative_price(self):
        order = self.new_order()
        path = f"{self.path}{order.id}/"

        response = self.client.put(
            path=path,
            data={
                "price": -self.fake.pyint(),
                "activated_status": self.fake.random_choices(
                    elements=OrderActivatedStatuses.choices
                )[0][0],
                "count": self.fake.pyint(),
                "status": self.fake.random_choices(elements=OrderStatuses.choices)[0][
                    0
                ],
                "is_sell": False,
                "portfolio": order.portfolio.id,
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)

    def test_update_order_with_incorrect_activated_status(self):
        order = self.new_order()
        path = f"{self.path}{order.id}/"

        response = self.client.put(
            path=path,
            data={
                "price": self.fake.pyint(),
                "activated_status": self.fake.name(),
                "count": self.fake.pyint(),
                "status": self.fake.random_choices(elements=OrderStatuses.choices)[0][
                    0
                ],
                "is_sell": False,
                "portfolio": order.portfolio.id,
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)

    def test_update_order_with_incorrect_status(self):
        order = self.new_order()
        path = f"{self.path}{order.id}/"

        response = self.client.put(
            path=path,
            data={
                "price": self.fake.pyint(),
                "activated_status": self.fake.random_choices(
                    elements=OrderActivatedStatuses.choices
                )[0][0],
                "count": self.fake.pyint(),
                "status": self.fake.name(),
                "is_sell": False,
                "portfolio": order.portfolio.id,
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)
