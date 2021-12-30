from django.contrib import admin
from django.urls import path
from base import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.IndexListView.as_view()),
    path('items/<str:pk>/', views.ItemDetailView.as_view()),

    path('cart/', views.CartListView.as_view()),
    path('cart/add/', views.AddCartView.as_view()),
    path('cart/remove/<str:item_pk>/', views.remove_from_cart),

    path('payment/checkout/', views.PaymentWithStripe.as_view()),
    path('payment/success/', views.PaymentSuccessView.as_view()),
    path('payment/cancel/', views.PaymentCancelView.as_view()),

    path('login/', views.Login.as_view()),
    path('logout/', LogoutView.as_view()),
    path('signup/', views.SignUpView.as_view()),
    path('account/', views.AccountUpdateView.as_view()),
    path('profile/', views.ProfileUpdateView.as_view()),
]
