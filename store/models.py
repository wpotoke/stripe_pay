# store/models.py
from django.db import models
from django.utils import timezone


class Item(models.Model):
    """Исходная модель какого то товара"""

    CURRENCY = (("RUB", "рубль"), ("USD", "доллар"))

    name = models.CharField(max_length=100, verbose_name="Название товара")
    description = models.TextField(max_length=7000, blank=True, null=True, verbose_name="Описание товара")
    price = models.DecimalField(
        max_digits=9,
        decimal_places=2,
        verbose_name="Стоимость",
    )
    currency = models.CharField(
        choices=CURRENCY,
        max_length=3,
        default="RUB",
        verbose_name="Валюта",
    )

    def __str__(self) -> str:
        return f"{self.name} ({self.price} {self.currency})"


class Discount(models.Model):
    """Процентная или фиксированная скидка, которую можно повесить на заказ."""

    name = models.CharField(max_length=100, verbose_name="Название скидки")
    percent = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name="Процент скидки",
    )

    def __str__(self):
        return f"{self.name} ({self.percent}%)"


class Tax(models.Model):
    """Налог в процентах от суммы заказа."""

    name = models.CharField(max_length=100, verbose_name="Название налога")
    percent = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name="Ставка налога",
    )

    def __str__(self):
        return f"{self.name} ({self.percent}%)"


class Order(models.Model):
    """Заказ из нескольких Item, в одной валюте."""

    class Status(models.TextChoices):
        NEW = "new", "Новый"
        PAID = "paid", "Оплачен"
        CANCELED = "canceled", "Отменён"

    currency = models.CharField(
        max_length=3,
        choices=Item.CURRENCY,
        verbose_name="Валюта заказа",
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.NEW,
        verbose_name="Статус",
    )
    discount = models.ForeignKey(
        Discount,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Скидка",
    )
    tax = models.ForeignKey(
        Tax,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Налог",
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    items = models.ManyToManyField(
        Item,
        through="OrderItem",
        related_name="orders",
        verbose_name="Товары",
    )

    def __str__(self):
        return f"Order #{self.id} ({self.currency}, {self.status})"

    def calculate_totals(self):
        """
        Возвращает словарь с:
        - subtotal: сумма по товарам
        - discount_amount: сумма скидки
        - tax_amount: сумма налога
        - total: итоговая сумма
        Все значения — Decimal в валюте заказа.
        """
        from decimal import ROUND_HALF_UP, Decimal

        subtotal = Decimal("0.00")
        order_items = self.orderitem_set.select_related("item")

        for oi in order_items:
            subtotal += oi.item.price * oi.quantity

        discount_amount = Decimal("0.00")
        if self.discount:
            discount_amount = (subtotal * self.discount.percent / Decimal("100")).quantize(
                Decimal("0.01"), rounding=ROUND_HALF_UP
            )

        base_for_tax = subtotal - discount_amount
        tax_amount = Decimal("0.00")
        if self.tax:
            tax_amount = (base_for_tax * self.tax.percent / Decimal("100")).quantize(
                Decimal("0.01"), rounding=ROUND_HALF_UP
            )

        total = base_for_tax + tax_amount

        return {
            "subtotal": subtotal,
            "discount_amount": discount_amount,
            "tax_amount": tax_amount,
            "total": total,
        }


class OrderItem(models.Model):
    """Связь Order – Item с количеством."""

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")

    def __str__(self):
        return f"Order #{self.order_id}: {self.item.name} x {self.quantity}"
