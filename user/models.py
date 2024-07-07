from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
  STATUS_CHOICES = [
      ('Yes', 'Yes'),
      ('No', 'No'),
  ]
  staff = models.OneToOneField(User,on_delete = models.CASCADE, null = True)
  address = models.CharField(max_length=200,null=True)  
  phone = models.CharField(max_length=20,null=True)
  image = models.ImageField(default='../media/profile.jpg',upload_to='Profile_Image')
  issue_permission = models.CharField(max_length=10, choices=STATUS_CHOICES, default='No')

  def __str__(self):
    return f'{self.staff.username} - Profile'
  
  def save(self, *args, **kwargs):
      if self.staff.is_superuser:
        self.issue_permission = 'Yes'
      super().save(*args, **kwargs)

      