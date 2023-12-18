# from unittest import TestCase
#
# from faker import Faker
# from rest_framework.test import APIClient
#
#
# class MarketOrderListCreateAPIViewTest(TestCase):
#     def setUp(self) -> None:
#         self.client = APIClient()
#         self.fake = Faker()
#         self.path = "/api/orders/market/"
#
#     def test_create_order(self):
#         response = self.client.post(
#             path=self.path,
#             data={
#                 "count": "3",
#                 "owner": "1",
#             })
#
#         print(response.data)
#         self.assertEqual(response.status_code, 201)
