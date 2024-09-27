from django.shortcuts import render, get_object_or_404, redirect
from .models import Medicament
from .forms import MedicamentForm

def medicament_list(request):
    medicaments = Medicament.objects.all()
    return render(request, 'medicaments/medicament_list.html', {'medicaments': medicaments})

def medicament_add(request):
    if request.method == 'POST':
        form = MedicamentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('medicament_list')
    else:
        form = MedicamentForm()
    return render(request, 'medicaments/medicament_form.html', {'form': form})

def medicament_edit(request, pk):
    medicament = get_object_or_404(Medicament, pk=pk)
    if request.method == 'POST':
        form = MedicamentForm(request.POST, request.FILES, instance=medicament)
        if form.is_valid():
            form.save()
            return redirect('medicament_list')
    else:
        form = MedicamentForm(instance=medicament)
    return render(request, 'medicaments/medicament_form.html', {'form': form})

def medicament_delete(request, pk):
    medicament = get_object_or_404(Medicament, pk=pk)
    medicament.delete()
    return redirect('medicament_list')

def medicament_history(request):
    history = Medicament.history.all().order_by('-history_date')
    return render(request, 'medicaments/medicament_history.html', {'history': history})
