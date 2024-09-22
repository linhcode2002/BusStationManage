from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, ValidationError, PrimaryKeyRelatedField
from .models import *
from django.contrib.auth import authenticate
from .models import Customer


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password', 'email', 'avatar']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        data = validated_data.copy()
        user = User(**data)
        user.set_password(data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        # Kiểm tra nếu mật khẩu được thay đổi thì băm lại mật khẩu
        if 'password' in validated_data:
            instance.set_password(validated_data.pop('password'))
        return super().update(instance, validated_data)


class ReviewSerializer(ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'rating', 'created_date', 'updated_date', 'customer_email']  # Thêm customer_email


class RevenueStatisticsSerializer(ModelSerializer):
    class Meta:
        model = RevenueStatistics
        fields = '__all__'


class BusRouteSerializer(ModelSerializer):
    class Meta:
        model = BusRoute
        fields = ['id', 'route_name', 'start_location', 'end_location', 'distance']


class TripSerializer(ModelSerializer):
    bus_route = BusRouteSerializer()

    class Meta:
        model = Trip
        fields = '__all__'


class BookingSerializer(ModelSerializer):  # Thay đổi từ TicketSerializer sang BookingSerializer
    trip = PrimaryKeyRelatedField(queryset=Trip.objects.all())
    seat = PrimaryKeyRelatedField(queryset=Seat.objects.all())

    class Meta:
        model = Booking
        fields = ['id', 'trip', 'seat', 'customer_email', 'customer_name', 'customer_phone', 'booking_time']


class CustomerSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Customer
        fields = ['email', 'password']

    # def validate(self, attrs):
    #     email = attrs.get('email')
    #     password = attrs.get('password')
    #
    #     if email and password:
    #         user = authenticate(username=email, password=password)
    #         if user is None:
    #             raise serializers.ValidationError('Email hoặc mật khẩu không đúng.')
    #         attrs['user'] = user
    #         return attrs
    #
    #     raise serializers.ValidationError('Vui lòng nhập email và mật khẩu.')
