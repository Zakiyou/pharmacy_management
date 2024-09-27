from django import forms
from django.core.exceptions import ValidationError
from .models import StockEntry, StockOut

class StockEntryForm(forms.ModelForm):
    class Meta:
        model = StockEntry
        fields = ['medicament', 'quantity_received', 'received_date', 'supplier', 'invoice_number', 'invoice_file',]
        """widgets = {
            'received_date': forms.DateInput(attrs={'type': 'date'}),
        }"""

    def clean_invoice_number(self):
        invoice_number = self.cleaned_data.get('invoice_number')
        if StockEntry.objects.filter(invoice_number=invoice_number).exclude(pk=self.instance.pk).exists():
            raise ValidationError("Le numéro de facture existe déjà pour une entrée de stock.")
        return invoice_number

class StockOutForm(forms.ModelForm):
    class Meta:
        model = StockOut
        fields = ['medicament', 'quantity_sold', 'sold_date', 'customer', 'invoice_number', 'invoice_file']
        """widgets = {
            'sold_date': forms.DateInput(attrs={'type': 'date'}),
        }"""

    def clean_invoice_number(self):
        invoice_number = self.cleaned_data.get('invoice_number')
        if StockOut.objects.filter(invoice_number=invoice_number).exclude(pk=self.instance.pk).exists():
            raise ValidationError("Le numéro de facture existe déjà pour une sortie de stock.")
        return invoice_number



class ExportForm(forms.Form):
    DATA_CHOICES = [
        ('entry', 'Entrées de Stock'),
        ('out', 'Sorties de Stock'),
    ]
    start_date = forms.DateField(label="Date de début", widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(label="Date de fin", widget=forms.DateInput(attrs={'type': 'date'}))
    data_type = forms.ChoiceField(label="Type de données", choices=DATA_CHOICES)
    format = forms.ChoiceField(label="Format", choices=[('csv', 'CSV'), ('excel', 'Excel'), ('pdf', 'PDF')])
