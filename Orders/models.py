from django.db import models
import uuid


# Create your models here.
class Person(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()


class BaseModel(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class ColourCode(BaseModel):
    colour_code = models.CharField(max_length=100)


class Customer(BaseModel):
    name = models.CharField(max_length=50)
    cust_id = models.IntegerField()
    cust_number = models.IntegerField()


class CustomerAddress(BaseModel):
    cust = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="cust_add")
    cust_add = models.TextField()


class Items(BaseModel):
    item_name = models.CharField(max_length=100)
    item_price = models.IntegerField()


class StockDetails(BaseModel):
    item_id = models.ForeignKey(Items, on_delete=models.CASCADE)
    item_photo = models.ImageField


class Orders(BaseModel):
    stock_id = models.ForeignKey(StockDetails, on_delete=models.CASCADE, default="")
    cust = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order_val = models.IntegerField()
    num_of_items = models.IntegerField()