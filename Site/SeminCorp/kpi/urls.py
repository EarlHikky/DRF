from django.urls import path
from .views import *

urlpatterns = [
    path('', SalesHome.as_view(), name='home'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('sales/', SalesView.as_view(), name='sales'),
    path('staff/', StaffView.as_view(), name='staff'),
    path('sale/<int:sale_id>/', s, name='sale'),
    path('add_sale/', AddSale.as_view(), name='add_sale'),
    path('add_staff/', AddStaff.as_view(), name='add_staff'),
    path('api/v1/saleslist/', SalesAPIView.as_view()),
    path('api/v1/saleslist/<int:pk>/', SalesAPIView.as_view()),

    ]