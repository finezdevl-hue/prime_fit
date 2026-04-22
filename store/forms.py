from django import forms
from .models import Category, Product, SiteSettings


class CategoryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            css_class = 'admin-input'
            if isinstance(field.widget, forms.Textarea):
                css_class = 'admin-textarea'
            elif isinstance(field.widget, forms.Select):
                css_class = 'admin-select'
            elif isinstance(field.widget, forms.ClearableFileInput):
                css_class = 'admin-file'
            field.widget.attrs['class'] = css_class

    class Meta:
        model = Category
        fields = ['name', 'slug', 'description', 'image', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }


class ProductForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            css_class = 'admin-input'
            if isinstance(field.widget, forms.Textarea):
                css_class = 'admin-textarea'
            elif isinstance(field.widget, forms.Select):
                css_class = 'admin-select'
            elif isinstance(field.widget, forms.ClearableFileInput):
                css_class = 'admin-file'
            field.widget.attrs['class'] = css_class

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


class SiteSettingsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            css_class = 'admin-input'
            if isinstance(field.widget, forms.Textarea):
                css_class = 'admin-textarea'
            elif isinstance(field.widget, forms.ClearableFileInput):
                css_class = 'admin-file'
            field.widget.attrs['class'] = css_class

    class Meta:
        model = SiteSettings
        fields = [
            'hero_image', 'hero_title_line1', 'hero_title_line2', 'hero_title_line3', 'hero_title_line4',
            'hero_subtitle', 'hero_eyebrow', 'hero_btn1_text', 'hero_btn1_link', 'hero_btn2_text', 'hero_btn2_link',
            'stat1_num', 'stat1_label', 'stat2_num', 'stat2_label', 'stat3_num', 'stat3_label'
        ]
        widgets = {
            'hero_subtitle': forms.Textarea(attrs={'rows': 3}),
        }
