from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Plan, Vertical

User = get_user_model()

class VerticalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vertical
        fields = ['id', 'name', 'description', 'created_at', 'updated_at']

class PlanSerializer(serializers.ModelSerializer):
    verticais = VerticalSerializer(many=True, read_only=True)
    verticais_ids = serializers.PrimaryKeyRelatedField(
        queryset=Vertical.objects.all(),
        many=True,
        write_only=True,
        required=False
    )

    class Meta:
        model = Plan
        fields = ['id', 'name', 'plan_type', 'description', 'price', 'verticais', 'verticais_ids', 'created_at', 'updated_at']

    def create(self, validated_data):
        verticais = validated_data.pop('verticais_ids', [])
        plan = Plan.objects.create(**validated_data)
        if verticais:
            plan.verticais.set(verticais)
        return plan

    def update(self, instance, validated_data):
        verticais = validated_data.pop('verticais_ids', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if verticais is not None:
            instance.verticais.set(verticais)
        instance.save()
        return instance

class UserSerializer(serializers.ModelSerializer):
    plan = PlanSerializer(read_only=True)
    plan_id = serializers.PrimaryKeyRelatedField(
        queryset=Plan.objects.all(),
        write_only=True,
        required=False,
        source='plan'
    )

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 
                 'user_type', 'plan', 'plan_id', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = User.objects.create(**validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance 