from django.db import models
import uuid
from django.utils.text import slugify


# from datatime import datetime,date
# Create your models here.


class ItemDetails(models.Model):
    ItemName = models.CharField(max_length=20, null=True)
    ItemID = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    ItemType = models.CharField(max_length=50)
    ItemPrice = models.IntegerField(null=True)
    #ItemImage = models.ImageField(upload_to="img/%y")
    ItemDescription = models.CharField(max_length=200, null=True, blank=True)
    ItemSlug = models.SlugField(max_length=40, unique=True, null=True, blank=True)

    def __str__(self):
        return f"ItemDetails(ItemName={self.ItemName}, ItemID={self.ItemID}, " \
               f"ItemPrice={self.ItemPrice}, ItemSlug={self.ItemSlug})"
        #return self.ItemName

    def save(self, *args, **kwargs):  # new
        if not self.ItemSlug:
            self.ItemSlug = slugify(self.ItemName)
        return super().save(*args, **kwargs)


class ItemColourOptions(models.Model):
    ItemColors = models.CharField(max_length=50)
    ItemAvailCount = models.IntegerField(default=0)
    ItemImage = models.ImageField(upload_to="media/product")
    Item = models.ForeignKey(ItemDetails, on_delete=models.CASCADE, related_name="Item_images")

    def __str__(self):
        return f"ItemColourOptions(ItemID={self.Item}, ItemAvailCount={self.ItemAvailCount}, " \
               f"ItemColors={self.ItemColors}, ItemImage={self.ItemImage})"

class Customer(models.Model):
    name = models.CharField(max_length=50, null=True)
    phone = models.CharField(max_length=50, null=True)
    instaid = models.CharField(max_length=50, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    address = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Out for delivery', 'Out for delivery'),
        ('Delivered', 'Delivered'),
    )

    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    item = models.ForeignKey(ItemDetails, null=True, on_delete=models.SET_NULL)
    date = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(max_length=50, null=True, choices=STATUS)


class Order(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Out for delivery', 'Out for delivery'),
        ('Delivered', 'Delivered'),
    )

    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    item = models.ForeignKey(ItemDetails, null=True, on_delete=models.SET_NULL)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField()
    address = models.CharField(max_length=200, default='', blank=True)
    phone = models.CharField(max_length=50, default='', blank=True)
    date = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(max_length=50, null=True, choices=STATUS)

    def placeOrder(self):
        self.save()

    @staticmethod
    def get_orders_by_customer(customer_id):
        return Order.objects.filter(customer=customer_id).order_by('-date')


class Expenses(models.Model):
    name = models.CharField(max_length=20, null=True)
    amount = models.IntegerField(null=True)
    month = models.CharField(max_length=20, null=True)
