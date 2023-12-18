# from unittest import TestCase
#
# from faker import Faker
# from rest_framework.test import APIClient
#
# from users.models import User
#
#
# class LimitOrderSetUp(TestCase):
#     def setUp(self) -> None:
#         self.client = APIClient()
#         self.fake = Faker()
#         investment = Investment.objects.create(
#             name=self.fake.name(),
#             price=self.fake.pyint(),
#             type="stock",
#         )
#         user = User.objects.create(
#             email=self.fake.email(),
#             username=self.fake.user_name(),
#             password=self.fake.password(),
#         )
#         self.owner_id = InvestmentPortfolio.objects.create(
#             owner=user,
#             investment=investment,
#             spend_amount=self.fake.pyint(),
#             count=self.fake.pyint(),
#         ).id
#
#
# class LimitOrderListCreateAPIViewTest(LimitOrderSetUp):
#     def setUp(self) -> None:
#         super().setUp()
#         self.path = "/api/orders/limit/"
#
#     def test_create_order(self):
#         response_1 = self.client.post(
#             path=self.path,
#             data={
#                 "price": self.fake.pyint(),
#        "activated_status": self.fake.random_element(OrderActivatedStatuses.choices)[0],
#                 "count": self.fake.pyint(),
#                 "owner": self.owner_id,
#             }
#         )
#         response_2 = self.client.post(
#             path=self.path,
#             data={
#                 "price": -self.fake.pyint(),
#                 "activated_status": "gte",
#                 "count": self.fake.pyint(),
#                 "owner": self.owner_id,
#             }
#         )
#
#         self.assertEqual(response_1.status_code, 201)
#         self.assertEqual(response_2.status_code, 400)
#
#     def test_list_order(self):
#         response = self.client.get(self.path)
#
#         self.assertIsInstance(response.data, list)
#         self.assertIsInstance(response.data[0], dict)
#
#
# class LimitOrderRetrieveUpdateAPIViewTest(LimitOrderSetUp):
#     def setUp(self) -> None:
#         super().setUp()
#         self.id = LimitOrder.objects.create(
#             price=self.fake.pyint(),
#             activated_status="gte",
#             count=self.fake.pyint(),
#             owner=self.owner_id,
#         ).id
#         self.path = f"/api/orders/limit/{self.id}/"
#
#     def test_retrieve_order(self):
#         response = self.client.get(self.path)
#
#         self.assertEqual(response.status_code, 200)
#         self.assertIsInstance(response.data, dict)
#         self.assertEqual(response.data["id"], self.id)
#
#     def test_update_order(self):
#         response = self.client.put(
#             path=self.path,
#             data={
#                 "price": self.fake.pyint(),
#                 "activated_status": "lte",
#                 "count": self.fake.pyint(),
#                 "status": "canceled",
#             }
#         )
#
