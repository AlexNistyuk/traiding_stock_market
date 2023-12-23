from brokers.factories import InvestmentFactory, RecommendationFactory
from django.test import TestCase
from faker import Faker


class RecommendationViewSetTest(TestCase):
    def setUp(self) -> None:
        self.fake = Faker()
        self.path = "/v1/recommendations/"
        self.new_recommendation = RecommendationFactory
        self.new_investment = InvestmentFactory

    # TODO: create list recommendation negative using permissions
    def test_list_recommendation_ok(self):
        _ = self.new_recommendation()

        response = self.client.get(self.path)

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, list)
        self.assertIsInstance(response.data[0], dict)

    def test_create_recommendation_ok(self):
        investment = self.new_investment()

        response = self.client.post(
            path=self.path,
            data={
                "counter": self.fake.pyint(),
                "investment": investment.id,
            },
        )

        self.assertEqual(response.status_code, 201)
        self.assertIsInstance(response.data, dict)

    def test_create_recommendation_with_duplicated_investment(self):
        investment = self.new_investment()

        response_1 = self.client.post(
            path=self.path,
            data={
                "counter": -self.fake.pyint(),
                "investment": investment.id,
            },
        )
        response_2 = self.client.post(
            path=self.path,
            data={
                "counter": self.fake.pyint(),
                "investment": investment.id,
            },
        )

        self.assertEqual(response_1.status_code, 201)
        self.assertEqual(response_2.status_code, 400)

    # TODO: create retrieve recommendation negative using permissions

    def test_retrieve_recommendation_ok(self):
        recommendation = self.new_recommendation()
        path = f"{self.path}{recommendation.id}/"

        response = self.client.get(path)

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, dict)
        self.assertEqual(response.data["id"], recommendation.id)

    def test_update_recommendation_ok(self):
        recommendation = self.new_recommendation()
        path = f"{self.path}{recommendation.id}/"

        response = self.client.put(
            path=path,
            data={
                "counter": -self.fake.pyint(),
                "investment": recommendation.investment.id,
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, dict)
        self.assertEqual(response.data["id"], recommendation.id)

    def test_update_recommendation_with_duplicated_investment(self):
        recommendation_1 = self.new_recommendation()
        recommendation_2 = self.new_recommendation()
        path = f"{self.path}{recommendation_2.id}/"

        response = self.client.put(
            path=path,
            data={
                "quantity": -self.fake.pyint(),
                "investment": recommendation_1.investment.id,
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)
