# Generated by Django 5.0.6 on 2024-06-27 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0006_order_model_no'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Issued', 'Issued'), ('Not Issued', 'Not Issued')], default='Not Issued', max_length=10),
        ),
    ]
