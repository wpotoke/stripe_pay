from django.urls import path

from store.views import get_item, get_session, stripe_success

urlpatterns = [
    path("buy/<int:item_id>/", get_session, name="get_session"),
    path("item/<int:item_id>/", get_item, name="get_item"),
    path("success/", stripe_success, name="stripe_success"),
]
