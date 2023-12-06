from django.db import models
import uuid
#from datatime import datetime,date
# Create your models here.


class ItemDetails(models.Model):
    ItemName = models.CharField(max_length=20, null=True)
    ItemID = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    ItemType = models.CharField(max_length=50)
    ItemPrice = models.IntegerField(5, null=True)
    ItemImage = models.ImageField(upload_to="img/%y")
    ItemDescription = models.CharField(max_length=200, null=True, blank=True)
    ItemAvailCount = models.IntegerField(10, default=0)

    def __str__(self):
        return self.ItemName


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
    item = models.ForeignKey(ItemDetails,null=True, on_delete=models.SET_NULL)
    date = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(max_length=50,null=True, choices=STATUS)
