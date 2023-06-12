from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
import os


# Order status, stored in Order Info
STATUS_CHOICE = (
    ("Pending", "Pending"),
    ("Delivered", "Delivered"),
)

PAYMENT_CHOICE = (
    # ("Jazzcash", "Jazzcash"),
    ("Online", "Online"),
    ("COD", "COD"),
)

def get_image_path(instance, filename):
    return os.path.join('media',  filename)


# Cylinder table
class Cylinder(models.Model):
    name = models.CharField(max_length=64)
    image = models.ImageField('Image',upload_to=get_image_path)
    description = models.TextField(max_length=200)
    price = models.PositiveIntegerField()
    weight = models.PositiveIntegerField()
    size = models.FloatField()
    availability = models.BooleanField()

    def __str__(self):
        return self.name


# Order table
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)


# from location_field.models.spatial import LocationField
from location_field.models.plain import PlainLocationField
from phonenumber_field.modelfields import PhoneNumberField

# from geoposition.fields import GeopositionField
class Distributor(models.Model):
    name = models.CharField(max_length=64)
    email = models.EmailField()
    # location = GeopositionField()
    location = PlainLocationField()
    # address = LocationField()
    phone_number = PhoneNumberField(default='+92', region='PK')

    def __str__(self):
        return self.name
    

# Order Info table
class OrderInfo(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    distributor = models.ForeignKey(Distributor, on_delete=models.CASCADE)
    status = models.CharField(choices=STATUS_CHOICE,
                              default="Pending",
                              max_length=30)
    total_items_qty = models.PositiveIntegerField(default=1)
    address = models.CharField(max_length=500)
    total_price = models.PositiveIntegerField()

    def __str__(self) -> str:
        return f"Order ID {self.orderid} of {self.total_items_qty} cylinders on {self.date}"


# Order Items info table
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    cylinder = models.ForeignKey(Cylinder, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} x {self.cylinder.__str__} in order {self.order.id}"


# Payment table
class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment_method = models.CharField(choices=PAYMENT_CHOICE, max_length=64)
    transaction_id = models.CharField(max_length=200,  null=True, blank=True)
    payment_date = models.DateTimeField(auto_now_add=True)
    amount = models.PositiveIntegerField()

    def __str__(self):
        return f"Payment for order {self.order} by {self.payment_method} on {self.payment_date}"


# Ratings table
class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cylinder = models.ForeignKey(Cylinder, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    comment = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.rating} on {self.cylinder} by {self.user}"

# Address table
class AddressInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    area = models.CharField(max_length=200)
    city = models.CharField(max_length=64)
    house_number = models.CharField(max_length=64)
    phone_number = PhoneNumberField(default='+92', region='PK')
    postal_code = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.user} address:  {self.house_number} {self.area}, {self.city}"
    