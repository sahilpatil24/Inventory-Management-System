# Generated by Django 5.0.6 on 2024-06-18 06:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_alter_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='../media/profile.jpg', upload_to='Profile_Image'),
        ),
    ]
