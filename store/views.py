import stripe
from django.conf import settings
from django.shortcuts import redirect, render

# from store.models import Item

stripe.api_key = settings.STRIPE_SECRET_KEY


def get_session(request):
    # item_model = get_object_or_404(Item, id=id)
    checkout_session = stripe.checkout.Session.create(
        line_items=[
            {
                "price_data": {
                    "currency": "usd",
                    "product_data": {
                        "name": "test product name",
                    },
                    "unit_amount": 2000,
                },
                "quantity": 1,
            },
        ],
        mode="payment",
        success_url="http://127.0.0.1:8000/success",
    )
    return redirect(checkout_session.url)


def index(request):
    return render(request, "stripe/success.html")
