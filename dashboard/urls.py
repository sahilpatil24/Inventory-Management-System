from django.urls import path
from . import views
# from .views import get_product_details

urlpatterns = [
  path('dashboard/', views.index, name = 'dashboard-index'),
  # path('validate-model-no/', views.validate_model_no, name='validate_model_no'),
  path('staff/', views.staff, name = 'dashboard-staff'),  
  path('update-permission/<int:user_id>/', views.update_user_issue_permission, name='update_user_issue_permission'),
  path('staff/detail/<int:pk>/', views.staff_detail, name = 'dashboard-staff-detail'),
  # path('staff/order/', views.staff_order, name='dashboard-staff-orders'),
  path('product/', views.product, name = 'dashboard-product'),
  path('product/delete/<int:pk>/', views.product_delete, name = 'dashboard-product-delete'),
  path('product/update/<int:pk>/', views.product_update, name = 'dashboard-product-update'),
  path('order/', views.order, name = 'dashboard-order'),
    path('dashboard/export-orders/', views.export_orders_to_excel, name='export-orders'),
    path('dashboard/export-all-orders/', views.export_all_orders_to_excel_user, name='export-all-orders-user'),
    path('edit-message/',views.edit_message, name = 'edit-message'),
    path('dashboard/export-all-products/', views.export_product_list_to_excel, name='export-all-products'),
    path('update-order-status/<int:order_id>/', views.update_order_status, name='update_order_status'),
      path('get-product-details/', views.get_product_details, name='get_product_details'),
      path('products/', views.product_list, name='dashboard-product-list'),
        path('staff/list/', views.staff_list, name='dashboard-staff-list'),
        path('dashboard/information/', views.dashboard_information, name='dashboard-information'),
  
  
  
]

