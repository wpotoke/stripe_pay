# pylint:disable=broad-exception-caught,import-error
from decimal import Decimal

import stripe
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.decorators.http import require_POST

from store.models import Item, Order

from .utils.setup_currency import setup_stripe_for_currency


@require_POST
def create_order_payment_intent(request, order_id: int):
    order = get_object_or_404(Order, id=order_id)

    totals = order.calculate_totals()
    total = totals["total"]

    amount_cents = int((total * Decimal("100")).quantize(Decimal("1")))

    setup_stripe_for_currency(order.currency)

    try:
        intent = stripe.PaymentIntent.create(
            amount=amount_cents,
            currency=order.currency.lower(),
            metadata={
                "order_id": str(order.id),
            },
        )
    except Exception as exc:
        return JsonResponse({"error": str(exc)}, status=400)

    return JsonResponse({"client_secret": intent["client_secret"]})


def order_detail(request, order_id: int):
    order = get_object_or_404(Order, id=order_id)
    totals = order.calculate_totals()

    publishable_key = setup_stripe_for_currency(order.currency)

    context = {
        "order": order,
        "items": order.orderitem_set.select_related("item"),
        "totals": totals,
        "stripe_publishable_key": publishable_key,
    }
    return render(request, "store/order_detail.html", context)


def get_item(request, item_id: int):
    """Страница товара с кнопкой Buy."""
    item = get_object_or_404(Item, id=item_id)
    publishable_key = setup_stripe_for_currency(item.currency)
    context = {
        "item": item,
        "stripe_publish_key": publishable_key,
    }
    return render(request, "store/item_detail.html", context)


def get_session(request, item_id: int):
    """Получить сессию(id)"""
    item = get_object_or_404(Item, id=item_id)
    publishable_key = setup_stripe_for_currency(item.currency)
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
    return JsonResponse({"session_id": checkout_session.id, "stripe_publishable_key": publishable_key})


def stripe_success(request):
    """Страница успешной оплаты."""
    return render(request, "stripe/success.html")


@require_POST
def update_status_order(request, order_id: int):
    order = get_object_or_404(Order, id=order_id)
    order.status = Order.Status.PAID
    order.save(update_fields=["status"])
    return JsonResponse({"ok": True})
