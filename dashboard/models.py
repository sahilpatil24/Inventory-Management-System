from django.db import models
from django.contrib.auth.models import User

# Create your models here.
CATEGORY = (
  ('Hardware','Hardware'),
  ('Software','Software'),
  ('Consumable','Consumable'),
)

class Product(models.Model):
  name = models.CharField(max_length = 100, null = True)
  model_no = models.CharField(max_length = 200, null = True)
  category = models.CharField(max_length = 20,choices = CATEGORY, null = True)
  quantity = models.PositiveIntegerField(null = True)

  def __str__(self):
    return f'{self.name}--{self.model_no}'

class Order(models.Model):
  STATUS_CHOICES = [
      ('Not Issued', 'Not Issued'),
      ('Issued', 'Issued'),
  ]

  product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
  staff = models.ForeignKey(User, models.CASCADE, null=True)
  model_no = models.CharField(max_length=200, null=True)
  order_quantity = models.PositiveIntegerField(null=True)
  date = models.DateTimeField(auto_now_add=True)
  status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Not Issued')

  def __str__(self):
    return f'{self.product} ordered by {self.staff.username}'

class Message(models.Model):
  message = models.TextField()

  def __str__(self):
    return f'{self.message}'