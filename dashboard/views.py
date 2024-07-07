from django.db.models import Case, When, Value, IntegerField
from django.shortcuts import render , redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Product,Order,Message
from user.models import Profile
from collections import defaultdict
from .forms import ProductForm,OrderForm,EditMessageForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from datetime import datetime, timedelta
import xlwt
from django.db.models import Q
from django.utils import timezone

def get_product_details(request):
    product_id = request.GET.get('product_id', None)
    if product_id:
        try:
            product = Product.objects.get(id=product_id)
            return JsonResponse({'valid': True, 'model_no': product.model_no, 'product_stock': product.quantity})
        except Product.DoesNotExist:
            return JsonResponse({'valid': False})
    return JsonResponse({'valid': False})

@login_required
def index(request):
    # Calculate 5 days ago from today
    five_days_ago = timezone.now().date() - timedelta(days=5)

    # Filter orders
    orders = Order.objects.filter(
        Q(status='Not Issued') | (Q(status='Issued') & Q(date__date__gte=five_days_ago))
    ).order_by('-status', '-date')

    search_query = request.GET.get('q')
    search_type = request.GET.get('search_type')
    order_by = request.GET.get('order_by', '-date')

    if search_query:
        if search_type == 'product_name':
            orders = orders.filter(
                Q(product__name__icontains=search_query) &
                Q(staff=request.user)
            )
        elif search_type == 'model_no':
            orders = orders.filter(
                Q(product__model_no__icontains=search_query) &
                Q(staff=request.user)
            )

    products = Product.objects.all()
    product_quantities = defaultdict(lambda: {"quantity": 0, "model_no": ""})

    order_count = orders.count()
    product_count = Product.objects.all().count()
    workers_count = User.objects.all().count()

    for order in orders:
        product_quantities[order.product.name]["quantity"] += order.order_quantity
        product_quantities[order.product.name]["model_no"] = order.product.model_no

    product_list = [{'name': name, 'quantity': details["quantity"], 'model_no': details["model_no"]} for name, details in product_quantities.items()]

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.staff = request.user
            product = instance.product
            if instance.order_quantity > product.quantity:
                messages.error(request, f"Order quantity for {product.name} exceeds available stock.")
            else:
                instance.save()
                messages.success(request, f"Order for {product.name} placed successfully.")
                product.quantity -= instance.order_quantity
                product.save()
                return redirect('dashboard-index')
    else:
        form = OrderForm()

    context = {
        'orders': orders,
        'products': products,
        'form': form,
        'product_list': product_list,
        'product_count': product_count,
        'workers_count': workers_count,
        'order_count': order_count,
    }
    return render(request, 'dashboard/index.html', context)

def export_orders_to_excel(request):
    
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="orders.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Orders')

    # Define headers
    row_num = 0
    columns = ['Product Name', 'Category', 'Model Number', 'Total Stock', 'Ordered Quantity','Order By', 'Date of Order']

    for col_num, column_title in enumerate(columns):
        ws.write(row_num, col_num, column_title)

    # Write data rows
    orders = Order.objects.all().order_by('-date')

    for order in orders:
        row_num += 1
        ws.write(row_num, 0, order.product.name)
        ws.write(row_num, 1, order.product.category)
        ws.write(row_num, 2, order.model_no)
        ws.write(row_num, 3, order.product.quantity)
        ws.write(row_num, 4, order.order_quantity)
        ws.write(row_num, 5, order.staff.username)
        ws.write(row_num, 6, order.date.strftime('%Y-%m-%d %H:%M:%S'))

    wb.save(response)
    return response

@login_required
def export_all_orders_to_excel_user(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="all-orders.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Orders')

    # Define headers
    row_num = 0
    columns = ['Product Name', 'Category', 'Model Number', 'Total Stock', 'Ordered Quantity', 'Order By', 'Order Date']

    for col_num, column_title in enumerate(columns):
        ws.write(row_num, col_num, column_title)

    # Fetch orders ordered by the current user
    orders = Order.objects.filter(staff=request.user).order_by('-date')

    for order in orders:
        row_num += 1
        ws.write(row_num, 0, order.product.name)
        ws.write(row_num, 1, order.product.category)
        ws.write(row_num, 2, order.model_no)
        ws.write(row_num, 3, order.product.quantity)
        ws.write(row_num, 4, order.order_quantity)
        ws.write(row_num, 5, order.staff.username)
        ws.write(row_num, 6, order.date.strftime('%Y-%m-%d %H:%M:%S'))

    wb.save(response)
    return response


@login_required 
def staff(request):
    workers = User.objects.all()

    # Order count code
    # Calculate 5 days ago from today
    five_days_ago = timezone.now().date() - timedelta(days=5)
    # Filter orders
    orders = Order.objects.filter(
        Q(status='Not Issued') | (Q(status='Issued') & Q(date__date__gte=five_days_ago))
    ).order_by('-status', '-date')
    order_count = orders.count()

    # order_count = Order.objects.all().count()
    product_count = Product.objects.all().count()
    workers_count = workers.count()
    context = {
        'workers':workers,
        'order_count': order_count,
        'product_count':product_count,
        'workers_count':workers_count,
    }
    return render(request, 'dashboard/staff.html',context)

@login_required
def staff_list(request):
    query = request.GET.get('q')
    search_type = request.GET.get('search_type', 'username')  # Default to 'username' if no search_type is provided
    # Order count code
    # Calculate 5 days ago from today
    five_days_ago = timezone.now().date() - timedelta(days=5)
    # Filter orders
    orders = Order.objects.filter(
        Q(status='Not Issued') | (Q(status='Issued') & Q(date__date__gte=five_days_ago))
    ).order_by('-status', '-date')
    order_count = orders.count()
    product_count = Product.objects.all().count()
    workers_count = User.objects.all().count()
    print(f"Query: {query}")
    print(f"Search Type: {search_type}")

    if query:
        if search_type == 'username':
            workers = User.objects.filter(username__icontains=query)
            print(f"Filtered by username: {workers}")
        elif search_type == 'email':
            workers = User.objects.filter(email__icontains=query)
            print(f"Filtered by email: {workers}")
        else:
            workers = User.objects.all()
            print("No valid search type, showing all workers")
    else:
        workers = User.objects.all()
        print("No query provided, showing all workers")

    print(f"Workers Count: {workers.count()}")

    context = {
        'workers': workers,
        'order_count': order_count,
        'product_count':product_count,
        'workers_count':workers_count,
    }
    return render(request, 'dashboard/staff.html', context)

@login_required
def update_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        if request.user.profile.issue_permission == 'Yes':
            status = request.POST.get('status')
            if status in dict(Order.STATUS_CHOICES):
                order.status = status
                order.save()
                messages.success(request, 'Order status updated successfully.')
            else:
                messages.error(request, 'Invalid status.')
        else:
            messages.error(request, 'You do not have permission to issue this order.')

    if request.user.is_superuser:
        return redirect('dashboard-order')
    else:
        return redirect('dashboard-index')


@login_required
def update_user_issue_permission(request, user_id):
    if request.user.is_superuser:  # Ensure only admin can update the permission
        user = get_object_or_404(User, id=user_id)
        if request.method == 'POST':
            permission = request.POST.get('issue_permission')
            if permission in dict(Profile.STATUS_CHOICES):
                user.profile.issue_permission = permission
                user.profile.save()
                messages.success(request, 'User issue permission updated successfully.')
            else:
                messages.error(request, 'Invalid permission.')
        return redirect('dashboard-staff-list')
    else:
        messages.error(request, 'You do not have permission to perform this action.')
        return redirect('dashboard-staff-list')


# @login_required
# def staff_order(request):
#     if request.user.profile.issue_permission == 'Yes':
#         return redirect(request,'dashboard/staff_orders.html')
#     else:
#         return redirect(request,'dashboard-index')

@login_required
def staff_detail(request,pk):
    # Order count code
    # Calculate 5 days ago from today
    five_days_ago = timezone.now().date() - timedelta(days=5)
    # Filter orders
    orders = Order.objects.filter(
        Q(status='Not Issued') | (Q(status='Issued') & Q(date__date__gte=five_days_ago))
    ).order_by('-status', '-date')
    order_count = orders.count()

    # order_count = Order.objects.all().count()
    product_count = Product.objects.all().count()
    workers_count = User.objects.all().count()
    workers = User.objects.get(id=pk)
    context = {
        'workers':workers,
        'order_count': order_count,
        'product_count':product_count,
        'workers_count':workers_count,
    }
    return render(request,'dashboard/staff_detail.html',context)

@login_required
def product(request):
    items = Product.objects.all() #USING ORM - Object Relational Mapping
    # items = Product.objects.raw('SELECT * FROM dashboard_product')
    product_count = items.count()
    workers_count = User.objects.all().count()
    # Order count code
    # Calculate 5 days ago from today
    five_days_ago = timezone.now().date() - timedelta(days=5)
    # Filter orders
    orders = Order.objects.filter(
        Q(status='Not Issued') | (Q(status='Issued') & Q(date__date__gte=five_days_ago))
    ).order_by('-status', '-date')
    order_count = orders.count()
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            product_name = form.cleaned_data.get('name')
            messages.success(request,f'{product_name} has been added')
            return redirect('dashboard-product')
    else:
        form = ProductForm()
    context = {
        'items': items,
        'order_count': order_count,
        'form':form,
        'workers_count':workers_count,
        'product_count':product_count,
    }
    return render(request, 'dashboard/product.html',context)

@login_required
def export_product_list_to_excel(request):
    item = Product.objects.all()
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="all-products.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Products')

    # Define headers
    row_num = 0
    columns = ['Product Name', 'Category', 'Model Number', 'Stock']

    for col_num, column_title in enumerate(columns):
        ws.write(row_num, col_num, column_title)

    # Write data rows
    orders = Order.objects.all().order_by('-date')

    for item in item:
        row_num += 1
        ws.write(row_num, 0, item.name)
        ws.write(row_num, 1, item.category)
        ws.write(row_num, 2, item.model_no)
        ws.write(row_num, 3, item.quantity)

    wb.save(response)
    return response


@login_required
def product_list(request):
    query = request.GET.get('q')
    search_type = request.GET.get('search_type', 'name')  # Default to 'name' if no search_type is provided
    # Order count code
    # Calculate 5 days ago from today
    five_days_ago = timezone.now().date() - timedelta(days=5)
    # Filter orders
    orders = Order.objects.filter(
        Q(status='Not Issued') | (Q(status='Issued') & Q(date__date__gte=five_days_ago))
    ).order_by('-status', '-date')
    order_count = orders.count()
    product_count = Product.objects.all().count()
    workers_count = User.objects.all().count()
    if query:
        if search_type == 'name':
            items = Product.objects.filter(name__icontains=query)
        elif search_type == 'model_no':
            items = Product.objects.filter(model_no__icontains=query)
        else:
            items = Product.objects.all()
    else:
        items = Product.objects.all()

    # ADD PRODUCTS FORM
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            product_name = form.cleaned_data.get('name')
            messages.success(request,f'{product_name} has been added')
            return redirect('dashboard-product')
    else:
        form = ProductForm()

    context = {
        'items': items,
        'form': form,
        'order_count': order_count,
        'product_count':product_count,
        'workers_count':workers_count,
    }
    return render(request, 'dashboard/product.html', context)


@login_required
def product_delete(request, pk):
    item = Product.objects.get(id=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('dashboard-product')
    return render(request,'dashboard/product_delete.html')

@login_required
def product_update(request, pk):
    item = Product.objects.get(id=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST,instance=item)
        if form.is_valid():
            form.save()
            return redirect('dashboard-product')
    else:
        form = ProductForm(instance=item)
    #     item.delete()
    #     return redirect('dashboard-product')
    context = {
        'form':form,
    }
    return render(request,'dashboard/product_update.html',context)


@login_required
def order(request):
    five_days_ago = timezone.now().date() - timedelta(days=5)
    query = request.GET.get('q')
    search_type = request.GET.get('search_type', 'product_name')
    order_by = request.GET.get('order_by', '-date')

    # Initial filter for issued within the last 5 days and not issued orders
    orders = Order.objects.filter(
        Q(status='Not Issued') | (Q(status='Issued') & Q(date__date__gte=five_days_ago))
    ).annotate(
        status_order=Case(
            When(status='Not Issued', then=Value(0)),
            When(status='Issued', then=Value(1)),
            output_field=IntegerField(),
        )
    ).order_by('status_order', order_by)

    # Apply search filtering
    if query:
        if search_type == 'product_name':
            orders = orders.filter(product__name__icontains=query)
        elif search_type == 'ordered_by':
            orders = orders.filter(staff__username__icontains=query)

    order_count = orders.count()
    product_count = Product.objects.all().count()
    workers_count = User.objects.all().count()
    
    context = {
        'orders': orders,
        'product_count': product_count,
        'workers_count': workers_count,
        'order_count': order_count,
    }
    return render(request, 'dashboard/order.html', context)
    
def edit_message(request):
    info, created = Message.objects.get_or_create(id=1)

    if request.method == 'POST':
        form = EditMessageForm(request.POST)
        if form.is_valid():
            info.message = form.cleaned_data['message']
            info.save()
            messages.success(request, 'Message updated successfully.')
            return redirect('dashboard-index')
    else:
        form = EditMessageForm(initial={'message': info.message})

    context = {
        'form': form,
    }
    return render(request, 'dashboard/edit_message.html', context)

def dashboard_information(request):
    return render(request,'dashboard/information.html')