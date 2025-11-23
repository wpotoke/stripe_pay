from django.urls import path

from store.views import (
    create_order_payment_intent,
    get_item,
    get_session,
    order_detail,
    stripe_success,
    update_status_order,
)

urlpatterns = [
    path("buy/<int:item_id>/", get_session, name="get_session"),
    path("item/<int:item_id>/", get_item, name="get_item"),
    path("orders/<int:order_id>/", order_detail, name="order_detail"),
    path(
        "orders/<int:order_id>/mark-paid/",
        update_status_order,
        name="order_mark_paid",
    ),
    path(
        "orders/<int:order_id>/create-intent/",
        create_order_payment_intent,
        name="order_create_intent",
    ),
    path("success/", stripe_success, name="stripe_success"),
]
