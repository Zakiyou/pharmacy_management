from django.contrib import admin
from .models import StockEntry, StockOut

@admin.register(StockEntry)
class StockEntryAdmin(admin.ModelAdmin):
    list_display = ('medicament', 'quantity_received', 'received_date', 'supplier', 'invoice_number', 'created_at')

@admin.register(StockOut)
class StockOutAdmin(admin.ModelAdmin):
    list_display = ('medicament', 'quantity_sold', 'sold_date', 'customer', 'invoice_number', 'created_at')
