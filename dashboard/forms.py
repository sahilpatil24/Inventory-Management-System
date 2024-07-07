from django import forms
from .models import Product, Order, Message

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'model_no', 'quantity']

class OrderForm(forms.ModelForm):
    product_name = forms.CharField(max_length=100, required=False, widget=forms.HiddenInput())

    class Meta:
        model = Order
        fields = ['product', 'model_no', 'order_quantity']

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['product'].queryset = Product.objects.all()
        self.fields['product'].widget.attrs.update({'id': 'id_product'})
        self.fields['model_no'].widget.attrs.update({'id': 'id_model_no'})
        self.fields['product_name'].widget.attrs.update({'id': 'id_product_name'})

class OrderStatusForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status']

class EditMessageForm(forms.ModelForm):
    message = forms.CharField(widget=forms.Textarea, label="Edit Message")
    
    class Meta:
        model = Message
        fields = ['message']