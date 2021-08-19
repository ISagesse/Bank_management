from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('overview', views.overview),
    path('add_fund', views.add_fund),
    path('activity', views.activity),
    path('stock', views.stock),
    path('stock/search', views.add_stock),
    path('sell/<int:id>', views.sell_stock),
    path('benefit', views.benefit),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
]