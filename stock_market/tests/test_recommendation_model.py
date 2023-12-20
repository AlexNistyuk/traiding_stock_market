from brokers.factories import RecommendationFactory
from brokers.models import Recommendation
from django.db import IntegrityError
from django.test import TestCase


class RecommendationModelTest(TestCase):
    def setUp(self) -> None:
        self.new_recommendation = RecommendationFactory

    def test_create_recommendation_ok(self):
        recommendation = self.new_recommendation()

        self.assertIsInstance(recommendation, Recommendation)

    def test_update_recommendation_with_duplicated_investment(self):
        recommendation_1 = self.new_recommendation()
        recommendation_2 = self.new_recommendation()

        recommendation_2.investment = recommendation_1.investment

        self.assertRaises(IntegrityError, recommendation_2.save)
