from brokers.factories import InvestmentPortfolioFactory, LimitOrderFactory
from brokers.models import OrderActivatedStatuses, OrderStatuses
from django.test import TestCase
from faker import Faker
from tests.utils import TestUser


class LimitOrderViewSetTest(TestCase):
    def setUp(self) -> None:
        self.path = "/v1/orders/limit/"
        self.fake = Faker()
        self.new_order = LimitOrderFactory
        self.new_portfolio = InvestmentPortfolioFactory
        self.test_user = TestUser()

    def test_list_order_ok(self):
        _ = self.new_order()
        token = self.test_user.get_admin_token()

        response = self.client.get(
            self.path, headers={"Authorization": f"Bearer {token}"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, list)
        self.assertIsInstance(response.data[0], dict)

    def test_list_order_permission_denied(self):
        _ = self.new_order()
        token = self.test_user.get_user_token()

        response = self.client.get(
            self.path, headers={"Authorization": f"Bearer {token}"}
        )

        self.assertEqual(response.status_code, 403)

    def test_create_order_ok(self):
        portfolio = self.new_portfolio()
        token = self.test_user.get_admin_token()

        response = self.client.post(
            path=self.path,
            data={
                "price": self.fake.pyint(),
                "activated_status": self.fake.random_choices(
                    elements=OrderActivatedStatuses.choices
                )[0][0],
                "quantity": portfolio.quantity,
                "portfolio": portfolio.id,
            },
            headers={"Authorization": f"Bearer {token}"},
        )

        self.assertEqual(response.status_code, 201)
        self.assertIsInstance(response.data, dict)
        self.assertIsInstance(response.data, dict)

    def test_create_order_with_incorrect_activated_status(self):
        portfolio = self.new_portfolio()
        token = self.test_user.get_admin_token()

        response = self.client.post(
            path=self.path,
            data={
                "price": self.fake.pyint(),
                "activated_status": self.fake.name(),
                "quantity": portfolio.quantity,
                "portfolio": portfolio.id,
            },
            headers={"Authorization": f"Bearer {token}"},
        )

        self.assertEqual(response.status_code, 400)

    def test_create_order_with_zero_quantity(self):
        portfolio = self.new_portfolio()
        token = self.test_user.get_admin_token()

        response = self.client.post(
            path=self.path,
            data={
                "price": self.fake.pyint(),
                "activated_status": self.fake.random_choices(
                    elements=OrderActivatedStatuses.choices
                )[0][0],
                "quantity": 0,
                "portfolio": portfolio.id,
            },
            headers={"Authorization": f"Bearer {token}"},
        )

        self.assertEqual(response.status_code, 400)

    def test_retrieve_order_ok(self):
        order = self.new_order()
        path = f"{self.path}{order.id}/"
        token = self.test_user.get_admin_token()

        response = self.client.get(path, headers={"Authorization": f"Bearer {token}"})

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, dict)
        self.assertEqual(response.data["id"], order.id)

    def test_retrieve_order_permission_denied(self):
        order = self.new_order()
        path = f"{self.path}{order.id}/"
        token = self.test_user.get_user_token()

        response = self.client.get(path, headers={"Authorization": f"Bearer {token}"})

        self.assertEqual(response.status_code, 403)

    def test_update_order_ok(self):
        order = self.new_order()
        path = f"{self.path}{order.id}/"
        token = self.test_user.get_admin_token()

        response = self.client.put(
            path=path,
            data={
                "price": self.fake.pyint(),
                "activated_status": self.fake.random_choices(
                    elements=OrderActivatedStatuses.choices
                )[0][0],
                "quantity": self.fake.pyint(),
                "status": self.fake.random_choices(elements=OrderStatuses.choices)[0][
                    0
                ],
                "portfolio": order.portfolio.id,
            },
            content_type="application/json",
            headers={"Authorization": f"Bearer {token}"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, dict)
        self.assertEqual(response.data["id"], order.id)

    def test_update_order_with_negative_quantity(self):
        order = self.new_order()
        path = f"{self.path}{order.id}/"
        token = self.test_user.get_admin_token()

        response = self.client.put(
            path=path,
            data={
                "price": self.fake.pyint(),
                "activated_status": self.fake.random_choices(
                    elements=OrderActivatedStatuses.choices
                )[0][0],
                "quantity": -self.fake.pyint(),
                "status": self.fake.random_choices(elements=OrderStatuses.choices)[0][
                    0
                ],
                "portfolio": order.portfolio.id,
            },
            content_type="application/json",
            headers={"Authorization": f"Bearer {token}"},
        )

        self.assertEqual(response.status_code, 400)

    def test_update_order_with_negative_price(self):
        order = self.new_order()
        path = f"{self.path}{order.id}/"
        token = self.test_user.get_admin_token()

        response = self.client.put(
            path=path,
            data={
                "price": -self.fake.pyint(),
                "activated_status": self.fake.random_choices(
                    elements=OrderActivatedStatuses.choices
                )[0][0],
                "quantity": self.fake.pyint(),
                "status": self.fake.random_choices(elements=OrderStatuses.choices)[0][
                    0
                ],
                "portfolio": order.portfolio.id,
            },
            content_type="application/json",
            headers={"Authorization": f"Bearer {token}"},
        )

        self.assertEqual(response.status_code, 400)

    def test_update_order_with_incorrect_activated_status(self):
        order = self.new_order()
        path = f"{self.path}{order.id}/"
        token = self.test_user.get_admin_token()

        response = self.client.put(
            path=path,
            data={
                "price": self.fake.pyint(),
                "activated_status": self.fake.name(),
                "quantity": self.fake.pyint(),
                "status": self.fake.random_choices(elements=OrderStatuses.choices)[0][
                    0
                ],
                "portfolio": order.portfolio.id,
            },
            content_type="application/json",
            headers={"Authorization": f"Bearer {token}"},
        )

        self.assertEqual(response.status_code, 400)

    def test_update_order_with_incorrect_status(self):
        order = self.new_order()
        path = f"{self.path}{order.id}/"
        token = self.test_user.get_admin_token()

        response = self.client.put(
            path=path,
            data={
                "price": self.fake.pyint(),
                "activated_status": self.fake.random_choices(
                    elements=OrderActivatedStatuses.choices
                )[0][0],
                "quantity": self.fake.pyint(),
                "status": self.fake.name(),
                "portfolio": order.portfolio.id,
            },
            content_type="application/json",
            headers={"Authorization": f"Bearer {token}"},
        )

        self.assertEqual(response.status_code, 400)
