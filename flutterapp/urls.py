"""flutterapp_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from flutterapp import views
from flutterapp_backend import settings
from django.conf.urls.static import static

urlpatterns = [
    path('products/', views.products, name='products_list'),
    path('products/<int:pk>/', views.products, name='products_detail'),
    # path('products/search/', views.search_products, name='products_search'),
    # path('send_cart/', views.cart, name="cart"), 
    # path('checkout/', views.checkout, name="checkout"),        
    # path('address/', views.address, name="address"),
    path('distributor/', views.distributor, name="distributor"),
    path('order/', views.order, name="order"),
    path('history/', views.history, name="history"),
    path('order/<int:pk>', views.order, name="order_detail"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)#imp for what you want to achieve.