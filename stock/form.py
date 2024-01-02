from django import forms
from .models import ItemDetails


class ItemsForm(forms.ModelForm):
    class Meta:
        model = ItemDetails
        fields = ("ItemName", "ItemPrice")