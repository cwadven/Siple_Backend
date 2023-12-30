from django.contrib import admin

from order.models import (
    Order,
    OrderItem,
    OrderItemDiscount,
    OrderItemRefund,
    OrderItemStatusLog,
    OrderStatusLog,
)


class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'guest_id',
        'member_id',
        'order_number',
        'tid',
        'status',
        'canceled_at',
        'succeeded_at',
        'refunded_at',
        'request_at',
    ]


class OrderStatusLogAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'order',
        'status',
        'request_at',
    ]


class OrderItemAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'product_id',
        'product_type',
        'product_price',
        'discounted_price',
        'paid_price',
        'item_quantity',
        'status',
        'canceled_at',
        'succeeded_at',
        'refunded_at',
    ]


class OrderItemRefundAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'order_item',
        'refunded_price',
        'refunded_quantity',
        'is_deleted',
        'request_at',
    ]


class OrderItemStatusLogAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'order_item',
        'status',
        'request_at',
    ]


class OrderItemDiscountAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'order_item',
        'discount_pk',
        'discount_type',
        'discounted_price',
    ]


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderStatusLog, OrderStatusLogAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(OrderItemRefund, OrderItemRefundAdmin)
admin.site.register(OrderItemStatusLog, OrderItemStatusLogAdmin)
admin.site.register(OrderItemDiscount, OrderItemDiscountAdmin)
