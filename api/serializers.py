import json
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from drf_yasg import openapi

from activity.models import *
from conf.models import *
from system.models import (
    Clan,
    Cooperative,
    FarmerGroup,
    Farmer,
    Collection
)
from sales.models import *


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=128)
    password = serializers.CharField(max_length=128)


class JsonSerializer(serializers.JSONField):
    class Meta:
        swagger_schema_fields = {
            "type": openapi.TYPE_OBJECT,
            "title": "Response",
            "properties": {
                "token": openapi.Schema(
                    title="Token",
                    type=openapi.TYPE_STRING,
                ),
                "user": openapi.Schema(
                    title="User",
                    type=openapi.TYPE_OBJECT,
                    properties={
                            "name": "string",
                            "gender": "string",
                            "email": "string",
                            "phone_number": "string",
                            "employee_number": "string",
                            "farm_assigned_to": openapi.Schema(type=openapi.TYPE_OBJECT,),
                            "designation": openapi.Schema(type=openapi.TYPE_OBJECT,)
                        }

                ),
            },
            "required": ["token", "user"],
        }


class AuthenticationShemaSerialiser(serializers.Serializer):
    status = serializers.CharField(max_length=255)
    response = JsonSerializer()
    class Meta:
        swagger_schema_fields = {
            "status": "error",
            "response": {
                "token": "4a11ececebbb32be3ef0622dd605b9f9a9ae9ba4",
                "user": {
                    "name": "",
                    "gender": "M",

                }
            }
        }


class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = '__all__'


class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = '__all__'


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = '__all__'


class CountySerializer(serializers.ModelSerializer):
    class Meta:
        model = County
        fields = '__all__'


class SubCountySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCounty
        fields = '__all__'


class ParishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parish
        fields = '__all__'


class VillageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Village
        fields = '__all__'


class CropSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crop
        fields = '__all__'


class ClanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clan
        fields = '__all__'


class CooperativeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cooperative
        fields = '__all__'


class FarmerGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = FarmerGroup
        fields = '__all__'


class ProfessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profession
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ProductVariationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariation
        fields = '__all__'


class ProductVariationPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariationPrice
        fields = '__all__'


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image:
            return request.build_absolute_uri(obj.image.url)
        return None


class OrderItemSerializer(serializers.ModelSerializer):
    item_id = serializers.PrimaryKeyRelatedField(
        source='item', queryset=Item.objects.all(), write_only=True, allow_null=True, required=False
    )
    class Meta:
        model = OrderItem
        fields = ['item_id', 'quantity', 'unit_price', 'total_price', 'order_reference']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    farmer_reference = serializers.CharField(write_only=True)

    class Meta:
        model = Order
        fields = ['farmer_reference', 'order_reference', 'total_amount', 'order_date','gps_coordinates', 'items']

    def create(self, validated_data):
        items_data = validated_data.pop('items')

        with transaction.atomic():
            # 1. Save or Update the Order based on the reference
            # Use update_or_create to allow "pushing later" without duplicates
            farmer = Farmer.objects.get(uuid=validated_data.get('farmer_reference'))
            validated_data['farmer'] = farmer
            validated_data.pop('farmer_reference')
            print(validated_data)
            order, created = Order.objects.update_or_create(
                order_reference=validated_data.get('order_reference'),
                defaults=validated_data
            )

            # 2. If it's an update, clear old items to avoid duplicates
            if not created:
                order.items.all().delete()
            print(items_data)
            # 3. Create the items
            for item_data in items_data:
                OrderItem.objects.create(order=order, **item_data)

        return order


class CollectionSerializer(serializers.ModelSerializer):
    farmer_reference = serializers.CharField(write_only=True)

    class Meta:
        model = Collection
        fields = '__all__'
        extra_kwargs = {
            'farmer': {'required': False},  # we will set it manually
        }

    def create(self, validated_data):
        farmer_ref = validated_data.pop('farmer_reference', None)

        # Ignore farmer if passed directly
        validated_data.pop('farmer', None)

        # Resolve farmer using reference
        farmer = None
        if farmer_ref:
            farmer = Farmer.objects.filter(uuid=farmer_ref).first()

        validated_data['farmer'] = farmer

        return super().create(validated_data)


class ThematicAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThematicArea
        fields = '__all__'


class TrainingSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingSession
        fields = '__all__'


class TrainingAttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingAttendance
        fields = '__all__'
        validators = []  # optional (prevents unique_together crash)



class ExternalTrainerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExternalTrainer
        fields = '__all__'


class FarmerSerializer(serializers.ModelSerializer):
    # crop = serializers.CharField(required=False, allow_blank=True)
    crop = serializers.SerializerMethodField()
    # Map Android _id fields to actual objects
    clan_id = serializers.PrimaryKeyRelatedField(
        source='clan', queryset=Clan.objects.all(), write_only=True, allow_null=True, required=False
    )
    district_id = serializers.PrimaryKeyRelatedField(
        source='district', queryset=District.objects.all(), write_only=True, allow_null=True, required=False
    )
    county_id = serializers.PrimaryKeyRelatedField(
        source='county', queryset=County.objects.all(), write_only=True, allow_null=True, required=False
    )
    sub_county_id = serializers.PrimaryKeyRelatedField(
        source='sub_county', queryset=SubCounty.objects.all(), write_only=True, allow_null=True, required=False
    )
    parish_id = serializers.PrimaryKeyRelatedField(
        source='parish', queryset=Parish.objects.all(), write_only=True, allow_null=True, required=False
    )
    cooperative_id = serializers.PrimaryKeyRelatedField(
        source='cooperative', queryset=Cooperative.objects.all(), write_only=True, allow_null=True, required=False
    )
    farmer_group_id = serializers.PrimaryKeyRelatedField(
        source='farmer_group', queryset=FarmerGroup.objects.all(), write_only=True, allow_null=True, required=False
    )

    class Meta:
        model = Farmer
        fields = '__all__'

    def to_internal_value(self, data):
        data = data.copy()

        choice_fields = ['id_type', 'title', 'marital_status', 'gender']

        for field_name in choice_fields:
            if field_name in data:
                field = Farmer._meta.get_field(field_name)
                choices = dict(field.choices)
                reverse_choices = {v: k for k, v in choices.items()}

                value = data[field_name]

                if value not in choices:
                    data[field_name] = reverse_choices.get(value, value)

        return super().to_internal_value(data)

    def validate_id_type(self, value):
        field = Farmer._meta.get_field('id_type')
        choices = dict(field.choices)

        # If already valid key (nin, dl, etc.)
        if value in choices:
            return value

        # Reverse lookup: label → key
        reverse_choices = {v: k for k, v in choices.items()}

        # Convert label to key
        if value in reverse_choices:
            return reverse_choices[value]

        # If still not valid → raise error
        raise serializers.ValidationError(f'"{value}" is not a valid choice.')

    def get_crop(self, obj):
        crops = obj.crop.all()

        if not crops.exists():
            return ""

        return ", ".join([crop.name for crop in crops])

    def create(self, validated_data):
        crops_str = validated_data.pop('crop', '')
        farmer = Farmer.objects.create(**validated_data)
        if crops_str:
            crop_names = [name.strip() for name in crops_str.split(',')]
            crops = Crop.objects.filter(name__in=crop_names)
            farmer.crop.set(crops)
        return farmer

    def update(self, instance, validated_data):
        crops_str = validated_data.pop('crop', '')
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if crops_str:
            crop_names = [name.strip() for name in crops_str.split(',')]
            crops = Crop.objects.filter(name__in=crop_names)
            instance.crop.set(crops)
        return instance