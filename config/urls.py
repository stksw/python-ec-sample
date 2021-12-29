from django.contrib import admin
from django.urls import path
from base import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.IndexListView.as_view()),
    path('items/<str:pk>/', views.ItemDetailView.as_view()),
    path('cart/', views.CartListView.as_view()),
    path('cart/add/', views.AddCartView.as_view()),
    path('cart/remove/<str:item_pk>/', views.remove_from_cart),
]
