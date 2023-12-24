from decimal import Decimal

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import F


class InvestmentTypes(models.TextChoices):
    STOCK = ("stock", "stock")
    CRYPTOCURRENCY = ("cryptocurrency", "cryptocurrency")


class OrderActivatedStatuses(models.TextChoices):
    GTE = ("gte", "greater than or equal")
    LTE = ("lte", "less than or equal")
    GT = ("gt", "greater then")
    LT = ("lt", "less than")
    EQUAL = ("equal", "equal")


class OrderStatuses(models.TextChoices):
    ACTIVE = ("active", "active")
    CANCELED = ("canceled", "canceled")
    DELETED = ("deleted", "deleted")
    COMPLETED = ("completed", "completed")


class Investment(models.Model):
    name = models.CharField(max_length=128, unique=True, db_index=True, null=False)
    image = models.ImageField(null=True, upload_to="logos/", blank=True)
    price = models.DecimalField(
        null=False,
        max_digits=settings.DECIMAL_MAX_DIGITS,
        decimal_places=settings.DECIMAL_PLACES,
        validators=[MinValueValidator(Decimal("0"))],
    )
    quantity = models.PositiveIntegerField(default=0)
    type = models.CharField(choices=InvestmentTypes.choices, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "investment"
        constraints = [
            models.CheckConstraint(
                check=models.Q(price__gte=Decimal("0")),
                name="investment_price_non_negative",
            ),
        ]

    def __str__(self):
        return self.name


class Order(models.Model):
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    status = models.CharField(
        choices=OrderStatuses.choices, default=OrderStatuses.ACTIVE
    )
    is_sell = models.BooleanField(default=False)
    portfolio = models.ForeignKey("InvestmentPortfolio", on_delete=models.CASCADE)
    investment = models.ForeignKey("Investment", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class MarketOrder(Order):
    class Meta:
        db_table = "market_order"
        ordering = ["created_at"]
        constraints = [
            models.CheckConstraint(
                check=models.Q(quantity__gte=1),
                name="market_order_quantity_greater_than_0",
            ),
        ]


class LimitOrder(Order):
    price = models.DecimalField(
        null=False,
        max_digits=settings.DECIMAL_MAX_DIGITS,
        decimal_places=settings.DECIMAL_PLACES,
        validators=[MinValueValidator(Decimal("0"))],
    )
    activated_status = models.CharField(
        choices=OrderActivatedStatuses.choices, default=OrderActivatedStatuses.LTE
    )

    class Meta:
        db_table = "limit_order"
        ordering = ["created_at"]
        constraints = [
            models.CheckConstraint(
                check=models.Q(price__gte=Decimal("0")),
                name="limit_order_price_non_negative",
            ),
            models.CheckConstraint(
                check=models.Q(quantity__gte=1),
                name="limit_order_quantity_greater_than_0",
            ),
        ]


class InvestmentPortfolio(models.Model):
    quantity = models.PositiveIntegerField(default=0)
    spend_amount = models.DecimalField(
        null=False,
        max_digits=settings.DECIMAL_MAX_DIGITS,
        decimal_places=settings.DECIMAL_PLACES,
        validators=[MinValueValidator(Decimal("0"))],
    )
    owner = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="portfolio"
    )
    investment = models.ForeignKey("Investment", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "investment_portfolio"
        ordering = ["-quantity"]
        unique_together = ("owner", "investment")
        constraints = [
            models.CheckConstraint(
                check=models.Q(spend_amount__gte=Decimal("0")),
                name="investment_portfolio_spend_amount_non_negative",
            ),
        ]


class Trade(models.Model):
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    price = models.DecimalField(
        null=False,
        max_digits=settings.DECIMAL_MAX_DIGITS,
        decimal_places=settings.DECIMAL_PLACES,
        validators=[MinValueValidator(Decimal("0"))],
    )
    seller = models.ForeignKey(
        "InvestmentPortfolio", on_delete=models.DO_NOTHING, related_name="seller"
    )
    buyer = models.ForeignKey(
        "InvestmentPortfolio", on_delete=models.DO_NOTHING, related_name="buyer"
    )
    investment = models.ForeignKey("Investment", on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "trade"
        ordering = ["-created_at"]
        constraints = [
            models.CheckConstraint(
                check=models.Q(price__gte=Decimal("0")), name="trade_price_non_negative"
            ),
            models.CheckConstraint(
                check=models.Q(quantity__gte=1),
                name="trade_quantity_greater_than_0",
            ),
            models.CheckConstraint(
                check=~models.Q(seller=F("buyer")),
                name="trade_seller_not_equal_buyer",
            ),
        ]


class Recommendation(models.Model):
    counter = models.IntegerField(default=0)
    investment = models.OneToOneField(
        "Investment", on_delete=models.CASCADE, db_index=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "recommendation"
