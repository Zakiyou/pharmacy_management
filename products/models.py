from django.db import models
from categories.models import Category
from simple_history.models import HistoricalRecords

class Medicament(models.Model):
    TYPE_CHOICES = [
        ('tablet', 'Comprimé'),
        ('syrup', 'Sirop'),
        ('capsule', 'Capsule'),
        ('ointment', 'Pommade'),
        ('injection', 'Injection'),
        ('drop', 'Goutte'),
        ('cream', 'Crème'),
        ('suppository', 'Suppositoire'),
    ]
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    code = models.CharField(max_length=50, unique=True)  # Code-barres ou identifiant unique
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='medicaments')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.PositiveIntegerField(default=0)
    expiration_date = models.DateField(null=True, blank=True)
    history = HistoricalRecords()  # Ajoutez ceci pour l'historique
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='tablet')
    icon = models.ImageField(upload_to='medicaments/icons/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)  # Ajoutez ce champ
    def __str__(self):
        return self.name