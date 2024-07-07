from django.contrib import admin
from .models import Product, Order
from django.contrib.auth.models import Group

admin.site.site_header = 'MyInventory'

class ProductAdmin(admin.ModelAdmin):
  list_display = ('name','quantity','model_no' ,'category')
  list_filter = ['category']

  class Meta:
    verbose_name_plural = 'Staff Products'

# Register your models here.
admin.site.register(Product,ProductAdmin)
admin.site.register(Order)