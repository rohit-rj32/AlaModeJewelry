from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('alamode', views.alamode, name="alamode"),
    path('orders', views.orders, name="orders"),
    path('reports', views.reports, name="reports"),
    path('addstock', views.addstock, name="addstock"),
    path('stockdetails', views.stockdetails, name="stockdetails"),
    path('dashboard', views.dashboard, name="dashboard"),
    path('pagedetails/<slug:slug>/', views.pagedetails, name="pagedetails"),
    path('cartdetails', views.cartdetails, name="cartdetails"),
    path('checkout', views.checkout, name="checkout"),
    path('ordercompleted', views.ordercompleted, name="ordercompleted"),
    path('processorder', views.processorder, name="processorder"),



]
