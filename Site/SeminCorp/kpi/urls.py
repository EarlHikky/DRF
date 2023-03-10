from django.urls import path, include
from rest_framework import routers
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

router = routers.DefaultRouter()
# router = routers.SimpleRouter()
router.register(r'sales', SalesViewSet)
print(router.urls)

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
    path('api/v1/', include(router.urls)),
    path('api/v1/drf-auth/', include('rest_framework.urls')),
    path('api/v1/auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    # path('api/v1/saleslist/', SalesViewSet.as_view({'get': 'list'})),
    # path('api/v1/saleslist/<int:pk>/', SalesViewSet.as_view({'put': 'update'})),
    # path('api/v1/saleslist/', SalesAPIView.as_view()),
    # path('api/v1/saleslist/<int:pk>/', SalesAPIView.as_view()),

    ]