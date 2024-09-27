from django.shortcuts import render, get_object_or_404, redirect
from .models import Category
from .forms import CategoryForm

def category_list(request):
    categories = Category.objects.all().select_related('domain')
    return render(request, 'categories/category_list.html', {'categories': categories})

def category_add(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm()
    return render(request, 'categories/category_form.html', {'form': form})

def category_edit(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'categories/category_form.html', {'form': form})

def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('category_list')
    return render(request, 'categories/category_confirm_delete.html', {'category': category})

def category_history(request):
    history = Category.history.all().order_by('-history_date')
    return render(request, 'categories/category_history.html', {'history': history})
