from decimal import Decimal

import stripe
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from store.models import Item

stripe.api_key = settings.STRIPE_SECRET_KEY


def get_item(request, item_id: int):
    """Страница товара с кнопкой Buy."""
    item = get_object_or_404(Item, id=item_id)
    context = {
        "item": item,
        "stripe_publish_key": settings.STRIPE_PUBLISH_KEY,
    }
    return render(request, "store/item_detail.html", context)


def get_session(request, item_id: int):
    """Получить сессию(id)"""
    item = get_object_or_404(Item, id=item_id)
    amount = int(item.price.quantize(Decimal("0.01")) * 100)
    checkout_session = stripe.checkout.Session.create(
        line_items=[
            {
                "price_data": {
                    "currency": item.currency.lower(),
                    "product_data": {
                        "name": item.name,
                        "description": item.description or "item description",
                    },
                    "unit_amount": amount,
                },
                "quantity": 1,
            },
        ],
        mode="payment",
        success_url=request.build_absolute_uri(
            reverse("stripe_success"),
        ),
        cancel_url=request.build_absolute_uri(reverse("get_item", kwargs={"item_id": item.id})),
    )
    return JsonResponse({"session_id": checkout_session.id})


def stripe_success(request):
    """Страница успешной оплаты."""
    return render(request, "stripe/success.html")
