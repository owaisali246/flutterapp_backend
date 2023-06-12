from django.contrib import admin
from .models import Cylinder, Order, OrderInfo, OrderItem, Payment, AddressInfo, Rating, Distributor
from .forms import DistributorInfoForm

@admin.register(Cylinder)
class CylinderAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'image', 'description',
                    'price', 'weight', 'size', 'availability']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user']


@admin.register(OrderInfo)
class OrderInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'date', 'status',
                    'total_items_qty', 'address', 'total_price']


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'cylinder', 'quantity', 'price']


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'payment_method',
                    'transaction_id', 'payment_date', 'amount']


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'cylinder', 'rating', 'comment', 'date']


@admin.register(AddressInfo)
class AddressInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'area', 'city', 'house_number','phone_number', 'postal_code']

@admin.register(Distributor)
class DistributorAdmin(admin.ModelAdmin):
    # form = DistributorInfoForm
    list_display = ['id', 'name', 'email', 'location', 'phone_number']

