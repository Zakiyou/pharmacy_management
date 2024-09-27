from django import forms
from .models import Category
from domaine.models import Domain

class CategoryForm(forms.ModelForm):
    domain = forms.ModelChoiceField(queryset=Domain.objects.all(), empty_label="Sélectionner un domaine")

    class Meta:
        model = Category
        fields = ['name', 'description', 'icon', 'domain']

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if len(name) > 100:
            raise forms.ValidationError('Le nom ne doit pas dépasser 100 caractères.')
        if Category.objects.filter(name=name).exists():
            raise forms.ValidationError('Une catégorie avec ce nom existe déjà.')
        return name

    def clean_icon(self):
        icon = self.cleaned_data.get('icon')
        if icon:
            max_size = 2 * 1024 * 1024  # 2 MB
            if icon.size > max_size:
                raise forms.ValidationError("L'image ne doit pas dépasser 2 Mo.")
        return icon
