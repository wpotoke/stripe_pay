from django.contrib import admin

from store.models import Item


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    pass
