from django.urls import path

from store.views import get_session, index

urlpatterns = [
    path("start/", get_session, name="start"),
    path("success/", index, name="index"),
]
