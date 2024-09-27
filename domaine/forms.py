from django import forms
from .models import Domain

class DomainForm(forms.ModelForm):
    class Meta:
        model = Domain
        fields = ['name', 'description', 'icon']

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if len(name) > 50:
            raise forms.ValidationError('Le nom ne doit pas dépasser 50 caractères.')
        # Exclure l'instance actuelle de la vérification d'unicité
        if Domain.objects.filter(name=name).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('Un domaine avec ce nom existe déjà.')
        return name

    def clean_icon(self):
        icon = self.cleaned_data.get('icon')
        if icon:
            max_size = 2 * 1024 * 1024  # 2 MB
            if icon.size > max_size:
                raise forms.ValidationError("L'image ne doit pas dépasser 2 Mo.")
        return icon
