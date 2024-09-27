from django.db import models
from products.models import Medicament

class StockEntry(models.Model):
    medicament = models.ForeignKey(Medicament, on_delete=models.CASCADE, related_name='stock_entries')
    quantity_received = models.PositiveIntegerField()
    received_date = models.DateField()
    supplier = models.CharField(max_length=100)
    invoice_number = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    invoice_file = models.FileField(upload_to='invoices/entries/', blank=True, null=True)  # Champ pour le fichier

    def __str__(self):
        return f"{self.medicament.name} - {self.quantity_received}"

class StockOut(models.Model):
    medicament = models.ForeignKey(Medicament, on_delete=models.CASCADE, related_name='stock_outs')
    quantity_sold = models.PositiveIntegerField()
    sold_date = models.DateField()
    customer = models.CharField(max_length=100)
    invoice_number = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    invoice_file = models.FileField(upload_to='invoices/entries/', blank=True, null=True)  # Champ pour le fichier

    def __str__(self):
        return f"{self.medicament.name} - {self.quantity_sold}"
