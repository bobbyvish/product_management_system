import imp
from unicodedata import name
from django.urls import path
from . import views
from django.conf.urls.static import static


urlpatterns = [
    path('',views.demoPage,name='admin_home'),
    path('admin/login', views.AdminLoginView.as_view(),name='admin_login'),
    path('admin/logout', views.AdminLogoutView,name='admin_logout'),

    # categories
    path('category_list',views.CategoryListView.as_view(),name='category_list'),
    path('category_create',views.CategoryCreateView.as_view(),name='category_create'),
    path('category_Update/<slug:pk>',views.CategoryUpdateView.as_view(),name='category_update'),

    #Sub_Categories
    path('sub_category_list',views.SubCategoryListView.as_view(),name='sub_category_list'),
    path('sub_category_create',views.SubCategoryCreateView.as_view(),name='sub_category_create'),
    path('sub_category_Update/<slug:pk>',views.SubCategoryUpdateView.as_view(),name='sub_category_update'),

    #MErchant
    path('merchant_create',views.MerchantUserCreateView.as_view(),name='merchant_create'),
    path('merchant_list',views.MerchantUserListView.as_view(),name='merchant_list'),
    path('merchant_update/<slug:pk>',views.MerchantUserUpdateView.as_view(),name='merchant_update'),

    #product
    path('product_create',views.ProductCreateView.as_view(),name="product_create"),
    path('product_list',views.ProductListView.as_view(),name="product_list"),
    path('product_update/<str:product_id>',views.ProductUpdateView.as_view(),name="product_update"),
    path('product_add_media/<str:product_id>',views.ProductAddMediaView.as_view(),name="product_add_media"),
    path('product_edit_media/<str:product_id>',views.ProductEditMediaView.as_view(),name="product_edit_media"),
    path('product_delete_media/<str:id>',views.ProductDeleteMediaView.as_view(),name="product_delete_media"),
    path('product_add_stock/<str:product_id>',views.ProductAddStockView.as_view(),name="product_add_stock"),
    
    #StaffUser
    path('staff_create',views.StaffUserCreateView.as_view(),name='staff_create'),
    path('staff_list',views.StaffUserListView.as_view(),name='staff_list'),
    path('staff_update/<slug:pk>',views.StaffUserUpdateView.as_view(),name='staff_update'),



    #fileupload
    path("file_upload",views.File_Upload,name="file_upload")
]   



