from django.db import models
from domaine.models import Domain
from simple_history.models import HistoricalRecords

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.ImageField(upload_to='categories/icons/', blank=True, null=True)
    domain = models.ForeignKey(Domain, related_name='categories', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"
