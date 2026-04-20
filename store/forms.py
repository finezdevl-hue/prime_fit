from django import forms
from .models import Category, Product


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'slug', 'description', 'image', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'category', 'name', 'slug', 'description', 'price', 'sale_price',
            'image', 'image2', 'image3', 'gender', 'available_sizes',
            'stock', 'is_active', 'is_featured', 'is_new_arrival'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'available_sizes': forms.TextInput(attrs={'placeholder': 'XS,S,M,L,XL,XXL'}),
        }
