from django import forms
from .models import *
class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        # fields = '__all__'
        fields = ['name','country']
        widgets = {
            'name':forms.TextInput(attrs={"class":"form-control"}),
            'country':forms.TextInput(attrs={"class":"form-control"}),
        }
class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        # fields = '__all__'
        fields = ['name','year','price','photo','brand']
        widgets = {
            'name':forms.TextInput(attrs={"class":"form-control"}),
            'year': forms.NumberInput(attrs={"class": "form-control"}),
            'price': forms.NumberInput(attrs={"class": "form-control"}),
            'brand':forms.Select(attrs={"class":"form-control"})
        }

class SearchForm(forms.Form):
    name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Search by model"})
    )