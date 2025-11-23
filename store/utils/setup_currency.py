import stripe
from django.conf import settings


def setup_stripe_for_currency(currency: str):
    cfg = settings.STRIPE_CONFIG.get(currency)
    if not cfg or not cfg["secret"]:
        raise ValueError(f"No Stripe config for currency {currency}")
    stripe.api_key = cfg["secret"]
    return cfg["publishable"]
