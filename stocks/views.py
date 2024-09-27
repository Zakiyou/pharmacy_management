import csv
import pandas as pd
from django.http import HttpResponse
from django.shortcuts import render, redirect,get_object_or_404
from .models import StockEntry, StockOut
from .forms import ExportForm, StockEntryForm, StockOutForm
from io import BytesIO
from reportlab.pdfgen import canvas
from django.contrib import messages

def stock_entry_list(request):
    entries = StockEntry.objects.all().order_by('-received_date')
    return render(request, 'stocks/stock_entry_list.html', {'entries': entries})

def stock_out_list(request):
    outs = StockOut.objects.all().order_by('-sold_date')
    return render(request, 'stocks/stock_out_list.html', {'outs': outs})

def add_stock_entry(request):
    if request.method == 'POST':
        form = StockEntryForm(request.POST, request.FILES)
        if form.is_valid():
            entry = form.save()
            entry.medicament.stock_quantity += entry.quantity_received
            entry.medicament.save()
            messages.success(request, 'Entrée de stock ajoutée avec succès.')
            return redirect('stock_entry_list')
    else:
        form = StockEntryForm()
    return render(request, 'stocks/stock_entry_form.html', {'form': form})

def add_stock_out(request):
    if request.method == 'POST':
        form = StockOutForm(request.POST, request.FILES)
        if form.is_valid():
            out = form.save(commit=False)
            if out.quantity_sold <= out.medicament.stock_quantity:
                out.save()
                out.medicament.stock_quantity -= out.quantity_sold
                out.medicament.save()
                messages.success(request, 'Sortie de stock ajoutée avec succès.')
                return redirect('stock_out_list')
            else:
                messages.error(request, "La quantité vendue dépasse le stock disponible.")
    else:
        form = StockOutForm()
    return render(request, 'stocks/stock_out_form.html', {'form': form})

def edit_stock_entry(request, pk):
    entry = get_object_or_404(StockEntry, pk=pk)
    if request.method == 'POST':
        form = StockEntryForm(request.POST, request.FILES, instance=entry)
        if form.is_valid():
            entry = form.save()
            entry.medicament.stock_quantity += entry.quantity_received
            entry.medicament.save()
            messages.success(request, 'Entrée de stock modifiée avec succès.')
            return redirect('stock_entry_list')
    else:
        form = StockEntryForm(instance=entry)
    return render(request, 'stocks/stock_entry_form.html', {'form': form})

def edit_stock_out(request, pk):
    out = get_object_or_404(StockOut, pk=pk)
    if request.method == 'POST':
        form = StockOutForm(request.POST, request.FILES, instance=out)
        if form.is_valid():
            previous_quantity_sold = out.quantity_sold
            out = form.save(commit=False)
            if out.quantity_sold <= out.medicament.stock_quantity + previous_quantity_sold:
                out.save()
                out.medicament.stock_quantity -= (out.quantity_sold - previous_quantity_sold)
                out.medicament.save()
                messages.success(request, 'Sortie de stock modifiée avec succès.')
                return redirect('stock_out_list')
            else:
                messages.error(request, "La quantité vendue dépasse le stock disponible.")
    else:
        form = StockOutForm(instance=out)
    return render(request, 'stocks/stock_out_form.html', {'form': form})
def delete_stock_entry(request, pk):
    entry = get_object_or_404(StockEntry, pk=pk)
    medicament = entry.medicament
    medicament.stock_quantity -= entry.quantity_received
    medicament.save()
    entry.delete()
    messages.success(request, 'Entrée de stock supprimée avec succès.')
    return redirect('stock_entry_list')

def delete_stock_out(request, pk):
    out = get_object_or_404(StockOut, pk=pk)
    medicament = out.medicament
    medicament.stock_quantity += out.quantity_sold
    medicament.save()
    out.delete()
    messages.success(request, 'Sortie de stock supprimée avec succès.')
    return redirect('stock_out_list')

def export_stock_data(request):
    if request.method == 'POST':
        form = ExportForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            export_format = form.cleaned_data['format']
            data_type = form.cleaned_data['data_type']

            # Filtrer les données en fonction du type
            if data_type == 'entry':
                records = StockEntry.objects.filter(received_date__range=[start_date, end_date])
                file_prefix = "stock_entries"
                columns = ['Médicament', 'Quantité reçue', 'Date de réception', 'Fournisseur', 'Numéro de facture']
                values = ['medicament__name', 'quantity_received', 'received_date', 'supplier', 'invoice_number']
            else:
                records = StockOut.objects.filter(sold_date__range=[start_date, end_date])
                file_prefix = "stock_outs"
                columns = ['Médicament', 'Quantité vendue', 'Date de vente', 'Client', 'Numéro de facture']
                values = ['medicament__name', 'quantity_sold', 'sold_date', 'customer', 'invoice_number']

            # Définir le nom du fichier
            filename = f"{file_prefix}_{start_date}_to_{end_date}.{export_format}"

            if export_format == 'csv':
                response = HttpResponse(content_type='text/csv')
                response['Content-Disposition'] = f'attachment; filename="{filename}"'

                writer = csv.writer(response)
                writer.writerow(columns)

                for record in records:
                    writer.writerow([getattr(record, field) for field in values])

                return response

            elif export_format == 'excel':
                response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                response['Content-Disposition'] = f'attachment; filename="{filename}"'

                # Utiliser Pandas pour créer le fichier Excel
                df = pd.DataFrame(list(records.values(*values)))
                df.columns = columns

                with pd.ExcelWriter(response, engine='xlsxwriter') as writer:
                    df.to_excel(writer, index=False, sheet_name='Stock Data')

                return response

            elif export_format == 'pdf':
                response = HttpResponse(content_type='application/pdf')
                response['Content-Disposition'] = f'attachment; filename="{filename}"'

                buffer = BytesIO()
                p = canvas.Canvas(buffer)

                p.drawString(100, 800, f"Données de stock du {start_date} au {end_date}")

                y = 750
                for record in records:
                    data_line = ", ".join([f"{col}: {getattr(record, field)}" for col, field in zip(columns, values)])
                    p.drawString(100, y, data_line)
                    y -= 20
                    if y < 50:
                        p.showPage()
                        y = 800

                p.save()
                pdf = buffer.getvalue()
                buffer.close()
                response.write(pdf)

                return response
    else:
        form = ExportForm()

    return render(request, 'stocks/export_stock_data.html', {'form': form})