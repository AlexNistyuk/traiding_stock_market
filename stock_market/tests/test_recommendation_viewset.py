from brokers.factories import InvestmentFactory, RecommendationFactory
from django.test import TestCase
from faker import Faker
from tests.utils import TestUser


class RecommendationViewSetTest(TestCase):
    def setUp(self) -> None:
        self.fake = Faker()
        self.path = "/v1/recommendations/"
        self.new_recommendation = RecommendationFactory
        self.new_investment = InvestmentFactory
        self.test_user = TestUser()

    def test_list_recommendation_ok(self):
        recommedation = self.new_recommendation()
        recommedation.percentage = -100
        recommedation.save()

        token = self.test_user.get_admin_token()

        response = self.client.get(
            self.path, headers={"Authorization": f"Bearer {token}"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, list)
        self.assertIsInstance(response.data[0], dict)

    def test_create_recommendation_ok(self):
        investment = self.new_investment()
        token = self.test_user.get_admin_token()

        response = self.client.post(
            path=self.path,
            data={
                "percentage": self.fake.pyint(),
                "investment": investment.id,
            },
            headers={"Authorization": f"Bearer {token}"},
        )

        self.assertEqual(response.status_code, 201)
        self.assertIsInstance(response.data, dict)

    def test_create_recommendation_with_duplicated_investment(self):
        investment = self.new_investment()
        token = self.test_user.get_admin_token()

        response_1 = self.client.post(
            path=self.path,
            data={
                "percentage": -self.fake.pyint(),
                "investment": investment.id,
            },
            headers={"Authorization": f"Bearer {token}"},
        )
        response_2 = self.client.post(
            path=self.path,
            data={
                "percentage": self.fake.pyint(),
                "investment": investment.id,
            },
            headers={"Authorization": f"Bearer {token}"},
        )

        self.assertEqual(response_1.status_code, 201)
        self.assertEqual(response_2.status_code, 400)

    def test_retrieve_recommendation_ok(self):
        recommendation = self.new_recommendation()
        recommendation.percentage = -100
        recommendation.save()

        path = f"{self.path}{recommendation.id}/"
        token = self.test_user.get_admin_token()

        response = self.client.get(path, headers={"Authorization": f"Bearer {token}"})

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, dict)
        self.assertEqual(response.data["id"], recommendation.id)

    def test_retrieve_recommendation_permission_denied(self):
        recommendation = self.new_recommendation()
        recommendation.percentage = -100
        recommendation.save()

        path = f"{self.path}{recommendation.id}/"
        token = self.test_user.get_user_token()

        response = self.client.get(path, headers={"Authorization": f"Bearer {token}"})

        self.assertEqual(response.status_code, 403)

    def test_update_recommendation_ok(self):
        recommendation = self.new_recommendation()
        recommendation.percentage = -100
        recommendation.save()

        path = f"{self.path}{recommendation.id}/"
        token = self.test_user.get_admin_token()

        response = self.client.put(
            path=path,
            data={
                "percentage": -self.fake.pyint(),
            },
            content_type="application/json",
            headers={"Authorization": f"Bearer {token}"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, dict)
        self.assertEqual(response.data["id"], recommendation.id)
