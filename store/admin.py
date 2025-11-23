from django.contrib import admin

from store.models import Discount, Item, Order, OrderItem, Tax


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price", "currency")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "currency", "status", "created_at")
    list_filter = ("status", "currency")


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin): ...


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin): ...


@admin.register(Tax)
class TaxAdmin(admin.ModelAdmin): ...
