from django import forms
from .models import Medicament
from django.core.exceptions import ValidationError
from datetime import date

class MedicamentForm(forms.ModelForm):
    class Meta:
        model = Medicament
        fields = ['name', 'description', 'code', 'category', 'price', 'stock_quantity', 'expiration_date', 'type', 'icon']
        """widgets = {
            'expiration_date': forms.DateInput(attrs={'type': 'date'}),
        }
             """
    def clean_name(self):
        name = self.cleaned_data.get('name')
        # Exclude the current instance from the uniqueness check
        if Medicament.objects.filter(name=name).exclude(pk=self.instance.pk).exists():
            raise ValidationError("Un médicament avec ce nom existe déjà.")
        return name

    def clean_code(self):
        code = self.cleaned_data.get('code')
        # Exclude the current instance from the uniqueness check
        if Medicament.objects.filter(code=code).exclude(pk=self.instance.pk).exists():
            raise ValidationError("Un médicament avec ce code-barres existe déjà.")
        return code

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price <= 0:
            raise ValidationError("Le prix doit être un nombre positif.")
        return price

    def clean_stock_quantity(self):
        stock_quantity = self.cleaned_data.get('stock_quantity')
        if stock_quantity < 0:
            raise ValidationError("La quantité en stock ne peut pas être négative.")
        return stock_quantity

    def clean_expiration_date(self):
        expiration_date = self.cleaned_data.get('expiration_date')
        if expiration_date and expiration_date <= date.today():
            raise ValidationError("La date d'expiration doit être postérieure à aujourd'hui.")
        return expiration_date
