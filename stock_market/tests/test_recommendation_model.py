from brokers.factories import RecommendationFactory
from brokers.models import Recommendation
from django.db import IntegrityError
from django.test import TestCase


class RecommendationModelTest(TestCase):
    def setUp(self) -> None:
        self.new_recommendation = RecommendationFactory
        self.recommendation_count = lambda: Recommendation.objects.count()

    def test_create_recommendation_ok(self):
        recommendation_count = self.recommendation_count()

        recommendation = self.new_recommendation()

        self.assertEqual(recommendation_count + 1, self.recommendation_count())
        self.assertIsInstance(recommendation, Recommendation)

    def test_update_recommendation_with_duplicated_investment(self):
        recommendation_count = self.recommendation_count()

        recommendation_1 = self.new_recommendation()
        recommendation_2 = self.new_recommendation()

        recommendation_2.investment = recommendation_1.investment

        self.assertEqual(recommendation_count + 2, self.recommendation_count())
        self.assertRaises(IntegrityError, recommendation_2.save)
