# Generated by Django 5.0.6 on 2024-08-03 19:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_historicalmedicament_icon_historicalmedicament_type_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalmedicament',
            name='created_at',
            field=models.DateTimeField(blank=True, editable=False, null=True),
        ),
        migrations.AddField(
            model_name='medicament',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
