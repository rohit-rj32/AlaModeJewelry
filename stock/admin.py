from django.contrib import admin
from .models import ItemDetails,Customer,Order

# Register your models here.
admin.site.register(ItemDetails)
admin.site.register(Customer)
admin.site.register(Order)


