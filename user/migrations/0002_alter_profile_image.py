# Generated by Django 5.0.6 on 2024-06-18 05:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='media\\profile.jpg', upload_to='Profile_Image'),
        ),
    ]
