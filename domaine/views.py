from django.shortcuts import render, get_object_or_404, redirect
from .models import Domain
from .forms import DomainForm

def domain_list(request):
    domains = Domain.objects.all().prefetch_related('categories')
    return render(request, 'domaine/domain_list.html', {'domains': domains})

def domain_add(request):
    if request.method == 'POST':
        form = DomainForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('domain_list')
    else:
        form = DomainForm()
    return render(request, 'domaine/domain_form.html', {'form': form})

def domain_edit(request, pk):
    domain = get_object_or_404(Domain, pk=pk)
    if request.method == 'POST':
        form = DomainForm(request.POST, request.FILES, instance=domain)
        if form.is_valid():
            form.save()
            return redirect('domain_list')
    else:
        form = DomainForm(instance=domain)
    return render(request, 'domaine/domain_form.html', {'form': form})

def domain_delete(request, pk):
    domain = get_object_or_404(Domain, pk=pk)
    domain.delete()
    return redirect('domain_list')

def domain_history(request):
    history = Domain.history.all().order_by('-history_date')
    return render(request, 'domaine/domain_history.html', {'history': history})
