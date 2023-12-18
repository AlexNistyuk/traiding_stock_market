# from unittest import TestCase
#
# from faker import Faker
# from rest_framework.test import APIClient
#
# from brokers.models import Investment, InvestmentTypes
# from users.models import User
#
#
# class InvestmentPortfolioSetUp(TestCase):
#     def setUp(self) -> None:
#         self.client = APIClient()
#         self.fake = Faker()
#         self.investment = Investment.objects.create(
#             name=self.fake.name(),
#             price=self.fake.pyint(),
#             type=self.fake.random_element(InvestmentTypes.choices)[0],
#         )
#         self.investment_2 = Investment.objects.create(
#             name=self.fake.name(),
#             price=self.fake.pyint(),
#             type=self.fake.random_element(InvestmentTypes.choices)[0],
#         )
#         self.user = User.objects.create(
#             email=self.fake.email(),
#             username=self.fake.user_name(),
#             password=self.fake.password(),
#         )
#
# class InvestmentPortfolioCreateAPIViewTest(InvestmentPortfolioSetUp):
#     def setUp(self) -> None:
#         super().setUp()
#         self.path = "/api/portfolio/"
#
#     def test_create_portfolio(self):
#         response_1 = self.client.post(
#             path=self.path,
#             data={
#                 "owner": self.user.id,
#                 "investment": self.investment.id,
#                 "count": self.fake.pyint(),
#             }
#         )
#         response_2 = self.client.post(
#             path=self.path,
#             data={
#                 "owner": self.user.id,
#                 "investment": self.investment.id,
#                 "count": self.fake.pyint(),
#             }
#         )
#
#         self.assertEqual(response_1.status_code, 201)
#         self.assertEqual(response_2.status_code, 400)
#         self.assertIn("id", response_1.data)
#
#
# class InvestmentPortfolioRetrieveUpdateAPIViewTest(InvestmentPortfolioSetUp):
#     def setUp(self) -> None:
#         super().setUp()
#         portfolio = self.client.post(
#             path="/api/portfolio/",
#             data={
#                 "owner": self.user.id,
#                 "investment": self.investment_2.id,
#                 "count": self.fake.pyint(),
#             }
#         )
#         self.id = portfolio.data["id"]
#         self.path = f"/api/portfolio/{self.id}/"
#
#     def test_retrieve_portfolio(self):
#         response = self.client.get(path=self.path)
#
#         self.assertEqual(response.data["id"], self.id)
#         self.assertEqual(response.data["owner"], self.user.id)
#         self.assertEqual(response.data["investment"], self.investment_2.id)
#
#     def test_update_portfolio(self):
#         count = self.fake.pyint()
#
#         response_1 = self.client.put(
#             path=self.path,
#             data={
#                 "owner": self.user.id,
#                 "investment": self.investment_2.id,
#                 "count": count,
#             }
#         )
#
#         self.assertEqual(response_1.data["id"], self.id)
#         self.assertEqual(response_1.data["count"], count)
#         self.assertEqual(response_1.data["owner"], self.user.id)
#         self.assertEqual(response_1.data["investment"], self.investment_2.id)
#
#     def test_spend_amount(self):
#         response_1 = self.client.put(
#             path=self.path,
#             data={
#                 "owner": self.user.id,
#                 "investment": self.investment_2.id,
#             }
#         )
#         response_2 = self.client.put(
#             path=self.path,
#             data={
#                 "owner": self.user.id,
#                 "investment": self.investment_2.id,
#             }
#         )
#
#         self.assertEqual(response_1.status_code, 400)
#         self.assertEqual(response_2.status_code, 200)
