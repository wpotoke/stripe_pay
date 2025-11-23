from django.db import models


class Item(models.Model):
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
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество товара(-ов)")

    def __str__(self) -> str:
        return f"{self.name} ({self.price} {self.currency})"
