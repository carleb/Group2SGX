from django import forms
from .models import Product
from django.utils.text import slugify

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'title', 'brand', 'description', 'price', 'quantity','image']

    def clean_title(self):
        title = self.cleaned_data.get('title')
        # Check if a product with the same title already exists
        if Product.objects.filter(title=title).exists():
            raise forms.ValidationError("This name already exists, please use another name")
        return title

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price < 0:
            raise forms.ValidationError("Cannot be negative.")
        return price

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity is not None and quantity < 0:
            raise forms.ValidationError("Cannot be negative.")
        return quantity

    def save(self, commit=True):
        instance = super(ProductForm, self).save(commit=False)
        instance.slug = slugify(instance.title)
        if commit:
            instance.save()
        return instance