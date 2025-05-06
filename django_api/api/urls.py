# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import *

router = DefaultRouter()
router.register(r'transport-models', TransportModelViewSet)
router.register(r'packaging-types', PackagingTypeViewSet)
router.register(r'services', ServiceViewSet)
router.register(r'delivery-statuses', DeliveryStatusViewSet)
router.register(r'cargo-types', CargoTypeViewSet)
router.register(r'deliveries', DeliveryViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('statistics/', StatisticsView.as_view(), name='statistics'),
]