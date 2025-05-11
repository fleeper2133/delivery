from django.shortcuts import render

# views.py
from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Sum
from main.models import Delivery
from reference_books.models import (
    TransportModel,
    PackagingType,
    Service,
    DeliveryStatus,
    CargoType,
)
from .serializers import *
from datetime import datetime, timedelta
import pytz

class TransportModelViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TransportModel.objects.all()
    serializer_class = TransportModelSerializer
    # permission_classes = [IsAuthenticated]

class PackagingTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PackagingType.objects.all()
    serializer_class = PackagingTypeSerializer
    #permission_classes = [IsAuthenticated]

class ServiceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    #permission_classes = [IsAuthenticated]

class DeliveryStatusViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DeliveryStatus.objects.all()
    serializer_class = DeliveryStatusSerializer
    #permission_classes = [IsAuthenticated]

class CargoTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CargoType.objects.all()
    serializer_class = CargoTypeSerializer
    #permission_classes = [IsAuthenticated]

class DeliveryViewSet(viewsets.ModelViewSet):
    queryset = Delivery.objects.all()
    serializer_class = DeliverySerializer
    # permission_classes = [IsAuthenticated]
    # filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'services', 'cargo_type']

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        
        # Фильтр по дате доставки
        date_from = self.request.query_params.get('date_from')
        date_to = self.request.query_params.get('date_to')
        
        if date_from:
            date_from = datetime.strptime(date_from, '%Y-%m-%d').replace(tzinfo=pytz.UTC)
            queryset = queryset.filter(scheduled_delivery__gte=date_from)
        
        if date_to:
            date_to = datetime.strptime(date_to, '%Y-%m-%d').replace(tzinfo=pytz.UTC) + timedelta(days=1)
            queryset = queryset.filter(scheduled_delivery__lte=date_to)
        
        # Для обычных пользователей показываем только их доставки
        # if not user.is_staff:
        #     queryset = queryset.filter(customer=user)
        
        return queryset

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        delivery = self.get_object()
        completed_status = DeliveryStatus.objects.get(code='DELIVERED')
        delivery.status = completed_status
        delivery.actual_delivery = datetime.now()
        delivery.save()
        return Response({'status': 'delivery completed'})

class StatisticsView(generics.GenericAPIView):
    #permission_classes = [IsAuthenticated]

    def get(self, request):
        # Фильтры
        date_from = request.query_params.get('date_from')
        date_to = request.query_params.get('date_to')
        service_id = request.query_params.get('service_id')
        cargo_type_id = request.query_params.get('cargo_type_id')

        queryset = Delivery.objects.all()
        
        if not request.user.is_staff:
            queryset = queryset.filter(customer=request.user)

        if date_from:
            date_from = datetime.strptime(date_from, '%Y-%m-%d').replace(tzinfo=pytz.UTC)
            queryset = queryset.filter(scheduled_delivery__gte=date_from)
        
        if date_to:
            date_to = datetime.strptime(date_to, '%Y-%m-%d').replace(tzinfo=pytz.UTC) + timedelta(days=1)
            queryset = queryset.filter(scheduled_delivery__lte=date_to)
        
        if service_id:
            queryset = queryset.filter(services__id=service_id)
        
        if cargo_type_id:
            queryset = queryset.filter(cargo_type__id=cargo_type_id)

        # Статистика
        total_deliveries = queryset.count()
        total_distance = queryset.aggregate(total=Sum('distance_km'))['total'] or 0
        total_revenue = queryset.aggregate(total=Sum('total_price'))['total'] or 0

        # Группировка по статусам
        by_status = (
            queryset.values('status__name')
            .annotate(count=Count('id'))
        )
        
        # Группировка по услугам
        by_service = (
            queryset.values('services__name')
            .annotate(count=Count('id'))
        )
        
        return Response({
            'total_deliveries': total_deliveries,
            'total_distance_km': total_distance,
            'total_revenue': total_revenue,
            'by_status': list(by_status),
            'by_service': list(by_service),
        })
