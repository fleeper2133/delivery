from rest_framework import serializers
from django.contrib.auth.models import User
from main.models import Delivery, DeliveryMedia
from reference_books.models import (
    TransportModel,
    PackagingType,
    Service,
    DeliveryStatus,
    CargoType,
)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')

class TransportModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransportModel
        fields = '__all__'

class PackagingTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackagingType
        fields = '__all__'

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'

class DeliveryStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryStatus
        fields = '__all__'

class CargoTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CargoType
        fields = '__all__'

class DeliveryMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryMedia
        fields = ('id', 'file', 'file_type', 'created_at')

class DeliverySerializer(serializers.ModelSerializer):
    transport = TransportModelSerializer(read_only=True)
    transport_id = serializers.PrimaryKeyRelatedField(
        queryset=TransportModel.objects.all(),
        source='transport',
        write_only=True
    )
    packaging_type = PackagingTypeSerializer(read_only=True)
    packaging_type_id = serializers.PrimaryKeyRelatedField(
        queryset=PackagingType.objects.all(),
        source='packaging_type',
        write_only=True
    )
    status = DeliveryStatusSerializer(read_only=True)
    status_id = serializers.PrimaryKeyRelatedField(
        queryset=DeliveryStatus.objects.all(),
        source='status',
        write_only=True,
        required=False
    )
    cargo_type = CargoTypeSerializer(read_only=True, required=False)
    cargo_type_id = serializers.PrimaryKeyRelatedField(
        queryset=CargoType.objects.all(),
        source='cargo_type',
        write_only=True,
        required=False,
        allow_null=True
    )
    services = ServiceSerializer(many=True, read_only=True)
    service_ids = serializers.PrimaryKeyRelatedField(
        queryset=Service.objects.all(),
        source='services',
        write_only=True,
        many=True
    )
    media_files = DeliveryMediaSerializer(many=True, read_only=True)
    customer = UserSerializer(read_only=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Delivery
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'customer')

    def create(self, validated_data):
        services = validated_data.pop('services', [])
        media_files = self.context.get('request').FILES.getlist('media_files', [])
        
        # Автоматически назначаем статус "В ожидании" если не указан
        if 'status' not in validated_data:
            pending_status = DeliveryStatus.objects.get(code='PENDING')
            validated_data['status'] = pending_status
        
        # Назначаем текущего пользователя как клиента
        validated_data['customer'] = self.context['request'].user
        
        delivery = Delivery.objects.create(**validated_data)
        delivery.services.set(services)
        
        # Сохраняем медиафайлы
        for file in media_files:
            DeliveryMedia.objects.create(
                delivery=delivery,
                file=file,
                file_type=file.content_type
            )
        
        return delivery

    def update(self, instance, validated_data):
        services = validated_data.pop('services', [])
        media_files = self.context.get('request').FILES.getlist('media_files', [])
        
        # Обновляем поля доставки
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Обновляем связанные услуги
        if services:
            instance.services.set(services)
        
        # Добавляем новые медиафайлы
        for file in media_files:
            DeliveryMedia.objects.create(
                delivery=instance,
                file=file,
                file_type=file.content_type
            )
        
        return instance