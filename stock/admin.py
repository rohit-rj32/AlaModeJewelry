from django.contrib import admin
from .models import ItemDetails, ItemColourOptions

# Register your models here.


class ItemColourOptionsAdmin(admin.StackedInline):
    model = ItemColourOptions


class ItemDetailsAdmin(admin.ModelAdmin):
    inlines = [ItemColourOptionsAdmin]


admin.site.register(ItemDetails, ItemDetailsAdmin)
admin.site.register(ItemColourOptions)


